# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

```bash
pip install git+https://github.com/anoronh4/smile-client@main
pip install -r requirements.txt
pip install -e .
```

## Commands

**Run all CI-tested tests** (requires `TEMPO_METADB_PROFILE=local`):
```bash
cd tests && TEMPO_METADB_PROFILE=local python -m pytest test_crf.py test_message_handler.py validate_schema.py -v
```

**Run a single test file:**
```bash
cd tests && TEMPO_METADB_PROFILE=local python -m pytest test_crf.py -v
```

**Run a single test by name:**
```bash
cd tests && TEMPO_METADB_PROFILE=local python -m pytest test_crf.py::TestCRF::test_parse -v
```

**Start local NATS server for listener development:**
```bash
bash listener/setup_nats_local.bash
bash listener/run.bash -p local
```

## Architecture

This is a Python package (`cohort_utils`) for managing cancer genomics cohorts at MSK. It handles cohort lifecycle: parsing, validation, metadata enrichment, and publishing events to the SMILE/NATS messaging infrastructure.

### Core domain

**`cohort_utils/model/`** — domain objects:
- `Cohort`: Central class. Loads from a CRJ dict or CRF file, normalizes IDs, validates against `cohort-request.schema.json`. Can serialize back to CRF, generate cohort-complete events, fill in missing normals, and integrate with SMILE metadata.
- `Sample`: Thin wrapper around a dict of sample metadata (cmoId/primaryId); used for enrichment via local metadata table or SMILE REST API.
- `Pairing`: Tumor-normal pairing table loaded from a TSV.
- `VoyagerTempoMPGen`: Parses Voyager tracker files (mapping, pairing, conflicts, unpaired).

**Two file formats:**
- **CRF (Cohort Request File)**: Tab-delimited file with `#key:value` metadata header lines followed by `TUMOR_ID / NORMAL_ID / PRIMARY_ID / NORMAL_PRIMARY_ID` columns. Filename convention: `<cohortId>.cohort.txt`.
- **CRJ (Cohort Request JSON)**: JSON dict with `cohortId`, `endUsers`, `pmUsers`, `projectTitle`, `type`, and `samples` array.

**Two sample ID namespaces:**
- `cmoId` / `normalCmoId`: CMO sample names, e.g. `C-AAAAAA-P001-d`
- `primaryId` / `normalPrimaryId`: IGO/primary IDs, e.g. `12345-A-1`

`utils.normalize_id` strips `s-` and `IGO-` prefixes and converts underscores to hyphens. `utils.categorize_id` uses regex to detect which ID type a string is.

### NATS messaging

**`cohort_utils/nats/settings.py`** — reads `TEMPO_METADB_PROFILE` env var (`local` | `dev` | `prod`) to set NATS URL, topic names, and output paths. This import has side effects (prints profile, raises on invalid value), so tests must set `TEMPO_METADB_PROFILE` before importing anything from `cohort_utils.nats`.

**`cohort_utils/nats/handler.py` — `EventHandler`**: Validates and publishes a single event. Supported types: `bam`, `maf`, `qc`, `cohort`, `cbioportal`, `cohortRequest`, `cohortUpdate`. JSON events are validated against their schema before send; `cbioportal` events use protobuf (`TempoMessage`).

**`cohort_utils/generate_updates.py`**: `@send_event` decorator wraps named functions (`bam_complete_event`, `maf_complete_event`, etc.) to auto-derive event type and publish via `EventHandler`.

**`cohort_utils/nats/message_handler.py` — `cohort_request_handler`**: NATS callback invoked by `smile-client` for each message on `MDB_STREAM.consumers.tempo.*`. Handles two subjects:
- `new-cohort-submit`: validates JSON, creates a `Cohort`, writes `<cohortId>.cohort.txt` to `CRF_OUTPUT_DIR`, appends embargo dates.
- `cohort-update`: decodes protobuf (`TempoCohortUpdate`), updates only the `#` metadata header lines in the existing CRF, preserving sample data rows.

### Protobuf

`cohort_utils/pb/` contains `.proto` definitions and generated `_pb2.py` files:
- `tempo.proto` / `tempo_pb2.py`: `TempoMessage` + `Event` — somatic mutation events sent to cBioPortal
- `smile.proto` / `smile_pb2.py`: `TempoSample`, `TempoCohortUpdate` — messages received from SMILE
- `tempo_maf.proto` / `tempo_maf_pb2.py`: MAF-specific protobuf

**Do not edit `_pb2.py` files directly** — regenerate from `.proto` sources using `protoc`.

### Schemas

`cohort_utils/schema/` holds JSON Schema files for NATS event validation: `cohort-request`, `cohort-complete`, `bam-complete`, `maf-complete`, `qc-complete`. All are loaded at import time from `schema/__init__.py`.

### Listener

`listener/` contains the production NATS listener setup. The listener runs `smile-client`, which subscribes to `MDB_STREAM.consumers.tempo.*` and calls `cohort_utils.nats.message_handler.cohort_request_handler` for each message. Environment-specific config files (`smile_client_config_<env>.json`) with TLS credentials are not in the repo (stored at `/home/svc_core005_bot04/metadb_certs/`).

### External dependency: SMILE REST API

`utils.search_smile_inputid` calls `http://smile.mskcc.org:3000/sampleById/<id>` to look up sample metadata. This is only reachable from the MSK network. Tests that exercise this path should mock it.
