# VoyagerTempoMPGen Validation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add automatic validation to `VoyagerTempoMPGen.__init__` that checks required columns per file and cross-file consistency against the tracker, reporting all violations at once via `ValueError`.

**Architecture:** A new `_validate` method is added to `VoyagerTempoMPGen` and called from `__init__` after `_load_files`. It checks required columns for each of the 5 DataFrames, then checks that all sample IDs in child files exist in `tracker.CMO_Sample_ID`. All violations are collected into a list before raising a single `ValueError`.

**Tech Stack:** Python, pandas, unittest, tempfile/shutil for test isolation.

---

## File Structure

- Modify: `cohort_utils/model/voyager_tracker.py` — add module-level constants `REQUIRED_COLUMNS` and `CROSS_FILE_CHECKS`, add `_validate` method, call `_validate` from `__init__`
- Modify: `tests/test_voyagertempompgen.py` — add `TestVoyagerValidation` class with 8 test cases

---

### Task 1: Required column validation

**Files:**
- Modify: `cohort_utils/model/voyager_tracker.py`
- Modify: `tests/test_voyagertempompgen.py`

- [ ] **Step 1: Write failing test for required column check (and valid-data sanity test)**

Replace the full contents of `tests/test_voyagertempompgen.py`:

```python
import unittest
import os
import shutil
import tempfile
import cohort_utils
from utils import run_test

VOYAGER1  = "./data/voyager1/"
VOYAGER2  = "./data/voyager2/"

class TestVoyager(unittest.TestCase):
    @run_test
    def test_voyager_compare(self):
        voyager1 = cohort_utils.model.VoyagerTempoMPGen(folderPath = VOYAGER1)
        voyager2 = cohort_utils.model.VoyagerTempoMPGen(folderPath = VOYAGER2)
        compare_result = voyager1.compare(voyager2)
        print(compare_result[["primaryId","CMO_Sample_ID_new","CMO_Sample_ID_old","dropped","added","bait_change"]])


class TestVoyagerValidation(unittest.TestCase):
    def _make_temp_voyager(self, overrides):
        """Copy voyager1 data into a fresh temp dir, overriding specified files."""
        tmpdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmpdir)
        for fname in os.listdir(VOYAGER1):
            shutil.copy(os.path.join(VOYAGER1, fname), os.path.join(tmpdir, fname))
        for fname, content in overrides.items():
            with open(os.path.join(tmpdir, fname), 'w') as f:
                f.write(content)
        return tmpdir

    def test_valid_data_passes(self):
        cohort_utils.model.VoyagerTempoMPGen(folderPath=VOYAGER1)

    def test_missing_required_column_raises(self):
        tmpdir = self._make_temp_voyager({
            "sample_tracker.txt": "CMO_Sample_ID\nA_T\nB_T\n"
        })
        with self.assertRaises(ValueError) as ctx:
            cohort_utils.model.VoyagerTempoMPGen(folderPath=tmpdir)
        self.assertIn("tracker", str(ctx.exception))
        self.assertIn("primaryId", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to confirm current state**

```bash
cd tests && python -m pytest test_voyagertempompgen.py::TestVoyagerValidation::test_valid_data_passes test_voyagertempompgen.py::TestVoyagerValidation::test_missing_required_column_raises -v
```

Expected: `test_valid_data_passes` PASSES, `test_missing_required_column_raises` FAILS (no `ValueError` raised yet).

- [ ] **Step 3: Add constants and `_validate` to `voyager_tracker.py`**

Replace the full contents of `cohort_utils/model/voyager_tracker.py`:

```python
import pandas as pd
import os

REQUIRED_COLUMNS = {
    "tracker": ["CMO_Sample_ID", "primaryId"],
    "conflict": ["ciTag", "cmoPatientId", "primaryId", "sampleClass", "runMode", "sampleType", "baitSet", "runDate", "Conflict Reason"],
    "unpaired": ["ciTag", "cmoPatientId", "primaryId", "sampleClass", "runMode", "sampleType", "baitSet", "runDate", "Possible Reason?"],
    "mapping": ["SAMPLE", "TARGET", "FASTQ_PE1", "FASTQ_PE2"],
    "pairing": ["TUMOR_ID", "NORMAL_ID"],
}

CROSS_FILE_CHECKS = [
    ("mapping", "SAMPLE"),
    ("pairing", "TUMOR_ID"),
    ("pairing", "NORMAL_ID"),
    ("conflict", "ciTag"),
    ("unpaired", "ciTag"),
]

class VoyagerTempoMPGen:
    def __init__(self,**kwargs):
        self.folderPath = kwargs.pop("folderPath")
        self._load_files()
        self._validate()

    def _load_files(self):
        for source,index_col in {"tracker":"CMO_Sample_ID","conflict":"ciTag","unpaired":"ciTag","mapping":"SAMPLE","pairing":"TUMOR_ID"}.items():
            print("loading " + source)
            setattr(self,source + "_file", os.path.join(self.folderPath,"sample_" + source + ".txt"))
            setattr(self,source, pd.read_csv(getattr(self,source + "_file"),sep="\t",header=0))
            getattr(self,source).index = getattr(self,source)[[index_col]]

    def _validate(self):
        errors = []
        for name, required in REQUIRED_COLUMNS.items():
            df = getattr(self, name)
            missing = [c for c in required if c not in df.columns]
            if missing:
                errors.append(f"{name}: missing columns {missing}")
        if errors:
            raise ValueError("VoyagerTempoMPGen validation failed:\n" + "\n".join(errors))

    def compare(self,other):
        mapping_new = pd.merge(self.mapping[["SAMPLE","TARGET","FASTQ_PE1"]], self.tracker[["CMO_Sample_ID","primaryId"]],left_on="SAMPLE",right_on="CMO_Sample_ID", how="inner")
        mapping_new = pd.merge(mapping_new, self.pairing, how="left", left_on="SAMPLE", right_on="TUMOR_ID")
        mapping_new = mapping_new.groupby(['primaryId','CMO_Sample_ID','TARGET','NORMAL_ID'])['FASTQ_PE1'].apply(list).reset_index(name='FASTQ_PE1')

        mapping_old = pd.merge(other.mapping[["SAMPLE","TARGET","FASTQ_PE1"]], other.tracker[["CMO_Sample_ID","primaryId"]],left_on="SAMPLE",right_on="CMO_Sample_ID", how="inner")
        mapping_old = pd.merge(mapping_old, other.pairing, how="left", left_on="SAMPLE", right_on="TUMOR_ID")
        mapping_old = mapping_old.groupby(['primaryId','CMO_Sample_ID','TARGET','NORMAL_ID'])['FASTQ_PE1'].apply(list).reset_index(name='FASTQ_PE1')

        merged_mapping = pd.merge(mapping_new, mapping_old, how="outer",on="primaryId",suffixes=('_new','_old'))
        merged_mapping["dropped"] = merged_mapping['CMO_Sample_ID_new'].isnull()
        merged_mapping["added"] = merged_mapping['CMO_Sample_ID_old'].isnull()
        merged_mapping = merged_mapping.assign(bait_change = lambda x: (x["TARGET_new"] != x["TARGET_old"]) & ~(x['dropped']) & ~(x['added']))
        merged_mapping = merged_mapping.assign(cmoId_change = lambda x: (x["CMO_Sample_ID_new"] != x["CMO_Sample_ID_old"]) & ~(x['dropped']) & ~(x['added']))
        merged_mapping = merged_mapping.assign(fastq_change = lambda x: (x["FASTQ_PE1_new"] != x["FASTQ_PE1_old"]) & ~(x['dropped']) & ~(x['added']))
        merged_mapping = merged_mapping.assign(normal_change = lambda x: (x["NORMAL_ID_new"] != x["NORMAL_ID_old"]) & ~(x['dropped']) & ~(x['added']))

        return merged_mapping

    def get_conflicts(self,query):
        pass

    def get_unpaired(self,query):
        pass
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd tests && python -m pytest test_voyagertempompgen.py::TestVoyagerValidation::test_valid_data_passes test_voyagertempompgen.py::TestVoyagerValidation::test_missing_required_column_raises -v
```

Expected: both PASS.

- [ ] **Step 5: Commit**

```bash
git add cohort_utils/model/voyager_tracker.py tests/test_voyagertempompgen.py
git commit -m "feat: add required column validation to VoyagerTempoMPGen"
```

---

### Task 2: Cross-file consistency validation

**Files:**
- Modify: `cohort_utils/model/voyager_tracker.py`
- Modify: `tests/test_voyagertempompgen.py`

- [ ] **Step 1: Write failing tests for each cross-file rule**

Add these 5 test methods to the `TestVoyagerValidation` class in `tests/test_voyagertempompgen.py`:

```python
def test_pairing_tumor_not_in_tracker_raises(self):
    tmpdir = self._make_temp_voyager({
        "sample_pairing.txt": "TUMOR_ID\tNORMAL_ID\nA_T\tA_N\nUNKNOWN_T\tA_N\n"
    })
    with self.assertRaises(ValueError) as ctx:
        cohort_utils.model.VoyagerTempoMPGen(folderPath=tmpdir)
    self.assertIn("pairing", str(ctx.exception))
    self.assertIn("UNKNOWN_T", str(ctx.exception))

def test_pairing_normal_not_in_tracker_raises(self):
    tmpdir = self._make_temp_voyager({
        "sample_pairing.txt": "TUMOR_ID\tNORMAL_ID\nA_T\tA_N\nB_T\tUNKNOWN_N\n"
    })
    with self.assertRaises(ValueError) as ctx:
        cohort_utils.model.VoyagerTempoMPGen(folderPath=tmpdir)
    self.assertIn("pairing", str(ctx.exception))
    self.assertIn("UNKNOWN_N", str(ctx.exception))

def test_mapping_sample_not_in_tracker_raises(self):
    tmpdir = self._make_temp_voyager({
        "sample_mapping.txt": "SAMPLE\tTARGET\tFASTQ_PE1\tFASTQ_PE2\nA_T\tidt\t/p/1.fastq.gz\t/p/2.fastq.gz\nUNKNOWN_S\tidt\t/p/3.fastq.gz\t/p/4.fastq.gz\n"
    })
    with self.assertRaises(ValueError) as ctx:
        cohort_utils.model.VoyagerTempoMPGen(folderPath=tmpdir)
    self.assertIn("mapping", str(ctx.exception))
    self.assertIn("UNKNOWN_S", str(ctx.exception))

def test_conflict_citag_not_in_tracker_raises(self):
    tmpdir = self._make_temp_voyager({
        "sample_conflict.txt": "ciTag\tcmoPatientId\tprimaryId\tsampleClass\trunMode\tsampleType\tbaitSet\trunDate\tConflict Reason\nUNKNOWN_C\tC-AAA\t12345_1\tTumor\tWES\tDNA\tidt\t2024-01-01\treason\n"
    })
    with self.assertRaises(ValueError) as ctx:
        cohort_utils.model.VoyagerTempoMPGen(folderPath=tmpdir)
    self.assertIn("conflict", str(ctx.exception))
    self.assertIn("UNKNOWN_C", str(ctx.exception))

def test_unpaired_citag_not_in_tracker_raises(self):
    tmpdir = self._make_temp_voyager({
        "sample_unpaired.txt": "ciTag\tcmoPatientId\tprimaryId\tsampleClass\trunMode\tsampleType\tbaitSet\trunDate\tPossible Reason?\nUNKNOWN_U\tC-AAA\t12345_1\tTumor\tWES\tDNA\tidt\t2024-01-01\treason\n"
    })
    with self.assertRaises(ValueError) as ctx:
        cohort_utils.model.VoyagerTempoMPGen(folderPath=tmpdir)
    self.assertIn("unpaired", str(ctx.exception))
    self.assertIn("UNKNOWN_U", str(ctx.exception))
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd tests && python -m pytest test_voyagertempompgen.py::TestVoyagerValidation::test_pairing_tumor_not_in_tracker_raises test_voyagertempompgen.py::TestVoyagerValidation::test_pairing_normal_not_in_tracker_raises test_voyagertempompgen.py::TestVoyagerValidation::test_mapping_sample_not_in_tracker_raises test_voyagertempompgen.py::TestVoyagerValidation::test_conflict_citag_not_in_tracker_raises test_voyagertempompgen.py::TestVoyagerValidation::test_unpaired_citag_not_in_tracker_raises -v
```

Expected: all 5 FAIL (no `ValueError` raised for consistency violations yet).

- [ ] **Step 3: Extend `_validate` with cross-file consistency checks**

Replace the `_validate` method in `cohort_utils/model/voyager_tracker.py` (lines 30–36) with:

```python
def _validate(self):
    errors = []
    for name, required in REQUIRED_COLUMNS.items():
        df = getattr(self, name)
        missing = [c for c in required if c not in df.columns]
        if missing:
            errors.append(f"{name}: missing columns {missing}")
    if "CMO_Sample_ID" in self.tracker.columns:
        tracker_ids = set(self.tracker["CMO_Sample_ID"])
        for file_name, col_name in CROSS_FILE_CHECKS:
            df = getattr(self, file_name)
            if col_name in df.columns:
                unknown = set(df[col_name]) - tracker_ids
                if unknown:
                    errors.append(f"{file_name}: {col_name} values not in tracker: {unknown}")
    if errors:
        raise ValueError("VoyagerTempoMPGen validation failed:\n" + "\n".join(errors))
```

- [ ] **Step 4: Run all validation tests**

```bash
cd tests && python -m pytest test_voyagertempompgen.py -v
```

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add cohort_utils/model/voyager_tracker.py tests/test_voyagertempompgen.py
git commit -m "feat: add cross-file consistency validation to VoyagerTempoMPGen"
```

---

### Task 3: Multiple violations reported together

**Files:**
- Modify: `tests/test_voyagertempompgen.py`

- [ ] **Step 1: Write test asserting both violations appear in one `ValueError`**

Add this test method to `TestVoyagerValidation` in `tests/test_voyagertempompgen.py`:

```python
def test_multiple_violations_reported_together(self):
    tmpdir = self._make_temp_voyager({
        "sample_pairing.txt": "TUMOR_ID\tNORMAL_ID\nA_T\tA_N\nUNKNOWN_T\tA_N\n",
        "sample_mapping.txt": "SAMPLE\tTARGET\tFASTQ_PE1\tFASTQ_PE2\nA_T\tidt\t/p/1.fastq.gz\t/p/2.fastq.gz\nUNKNOWN_S\tidt\t/p/3.fastq.gz\t/p/4.fastq.gz\n"
    })
    with self.assertRaises(ValueError) as ctx:
        cohort_utils.model.VoyagerTempoMPGen(folderPath=tmpdir)
    msg = str(ctx.exception)
    self.assertIn("pairing", msg)
    self.assertIn("UNKNOWN_T", msg)
    self.assertIn("mapping", msg)
    self.assertIn("UNKNOWN_S", msg)
```

- [ ] **Step 2: Run test to verify it passes**

```bash
cd tests && python -m pytest test_voyagertempompgen.py::TestVoyagerValidation::test_multiple_violations_reported_together -v
```

Expected: PASS (the collect-all-then-raise design handles this without additional implementation).

- [ ] **Step 3: Run full test file to confirm no regressions**

```bash
cd tests && python -m pytest test_voyagertempompgen.py -v
```

Expected: all tests PASS.

- [ ] **Step 4: Commit**

```bash
git add tests/test_voyagertempompgen.py
git commit -m "test: verify multiple VoyagerTempoMPGen violations are reported together"
```
