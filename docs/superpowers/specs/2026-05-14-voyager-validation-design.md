# VoyagerTempoMPGen Validation Design

**Date:** 2026-05-14
**Status:** Approved

## Summary

Add validation to `VoyagerTempoMPGen` that runs automatically at construction time. Validation checks required columns per file and cross-file consistency (all sample IDs reference known tracker entries). All violations are collected before raising, so callers see the full error report in one exception.

## Architecture

`__init__` calls `_load_files()` then `_validate()`.

`_load_files` is unchanged. If any of the 5 files is missing, `pd.read_csv` raises `FileNotFoundError` immediately and construction fails before `_validate` is ever reached — no changes needed.

`_validate` runs only when all files loaded successfully. It:

1. **Required columns** — for each of the 5 DataFrames, checks that all expected columns are present. Collects any missing columns as errors, e.g.:
   ```
   tracker: missing columns ['primaryId']
   ```

2. **Cross-file consistency** — checks 5 membership relationships against `tracker.CMO_Sample_ID`. For each, collects IDs present in the child file but absent from the tracker, e.g.:
   ```
   pairing: TUMOR_ID values not in tracker: {'X_T', 'Y_T'}
   ```

3. If any errors were collected, raises `ValueError` with all violations joined as a multiline string.

### Cross-file consistency rules

| Child file | Column(s) checked | Must be subset of |
|---|---|---|
| mapping | `SAMPLE` | `tracker.CMO_Sample_ID` |
| pairing | `TUMOR_ID` | `tracker.CMO_Sample_ID` |
| pairing | `NORMAL_ID` | `tracker.CMO_Sample_ID` |
| conflict | `ciTag` | `tracker.CMO_Sample_ID` |
| unpaired | `ciTag` | `tracker.CMO_Sample_ID` |

### Required columns per file

| File | Required columns |
|---|---|
| tracker | `CMO_Sample_ID`, `primaryId` |
| conflict | `ciTag`, `cmoPatientId`, `primaryId`, `sampleClass`, `runMode`, `sampleType`, `baitSet`, `runDate`, `Conflict Reason` |
| unpaired | `ciTag`, `cmoPatientId`, `primaryId`, `sampleClass`, `runMode`, `sampleType`, `baitSet`, `runDate`, `Possible Reason?` |
| mapping | `SAMPLE`, `TARGET`, `FASTQ_PE1`, `FASTQ_PE2` |
| pairing | `TUMOR_ID`, `NORMAL_ID` |

## Error handling

- Missing file → `FileNotFoundError` from `pd.read_csv` (existing behavior, unchanged)
- Column or consistency violations → `ValueError` raised at end of `_validate` with all violations listed, one per line
- Column check failures for a given file do not block cross-file consistency checks for other files; however, consistency checks that involve a file with missing columns are skipped for that file to avoid misleading errors

## Testing

New tests added to `tests/test_voyagertempompgen.py`. Each failing-case test writes a modified temp folder using `tempfile.TemporaryDirectory` and copies the `voyager1` test data, then overwrites the relevant file.

| Test | What it does | Assertion |
|---|---|---|
| `test_valid_data_passes` | Constructs from `voyager1` data | No exception raised |
| `test_missing_required_column` | Removes `primaryId` from tracker | `ValueError` mentioning `tracker` and `primaryId` |
| `test_pairing_tumor_not_in_tracker` | Adds unknown `TUMOR_ID` to pairing | `ValueError` mentioning `pairing` and the bad ID |
| `test_pairing_normal_not_in_tracker` | Adds unknown `NORMAL_ID` to pairing | `ValueError` mentioning `pairing` and the bad ID |
| `test_mapping_sample_not_in_tracker` | Adds unknown `SAMPLE` to mapping | `ValueError` mentioning `mapping` and the bad ID |
| `test_conflict_citag_not_in_tracker` | Adds unknown `ciTag` to conflict | `ValueError` mentioning `conflict` and the bad ID |
| `test_unpaired_citag_not_in_tracker` | Adds unknown `ciTag` to unpaired | `ValueError` mentioning `unpaired` and the bad ID |
| `test_multiple_violations_reported_together` | Corrupts both pairing and mapping | `ValueError` mentions both issues in one message |
