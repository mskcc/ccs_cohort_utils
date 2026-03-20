# TEMPO Cohort Listener

This folder contains the setup for running a NATS listener that receives cohort messages from SMILE (Sample & Metadata Infrastructure for Labs and Engineering) and writes the results to Cohort Request Files (CRFs) used by the TEMPO WES delivery pipeline.

## Overview

When SMILE publishes a cohort event on the NATS message bus, this listener picks it up and processes it. There are two event types it handles:

- **`new-cohort-submit`** — A new cohort is being submitted. The listener validates the message against the cohort request JSON schema, creates a CRF file (`<cohortId>.cohort.txt`) containing cohort metadata and the sample pairing table, and records any embargo dates.
- **`cohort-update`** — Metadata for an existing cohort has changed (e.g., project title, end users). The listener updates only the metadata header lines of the existing CRF, leaving the sample data rows untouched.

## Components

### `run.bash`
The main entry point for starting the listener. It activates the conda environment, sources the appropriate TLS credentials, and launches the `smile-client` listener process. Logs are written to the `logs/` directory with a timestamped filename.

### `smile_client_config_<env>.json`
Environment-specific configuration files for the `smile-client`. Each specifies:
- **`NATS_URL`** — Address of the NATS server
- **`NATS_USERNAME` / `NATS_PASSWORD`** — NATS credentials
- **`NATS_SSL_CERTFILE` / `NATS_SSL_KEYFILE` / `NATS_ROOT_CA`** — TLS certificate paths
- **`NATS_FILTER_SUBJECT`** — The NATS subject pattern to subscribe to (`MDB_STREAM.consumers.tempo.*`)
- **`CALLBACK`** — The Python function invoked for each received message (`cohort_utils.nats.message_handler.cohort_request_handler`)

These are currently held in `/home/svc_core005_bot04/metadb_certs/`. The main entry point contains the paths.

### `setup_nats_local.bash`
A helper script for local development. Starts a NATS server with JetStream enabled on `localhost:4222` and creates the `MDB_STREAM` stream. Run this before starting the listener in `local` mode.

### `ccs_cohort_utils/`
A Python package (installed into the conda environment) that provides the message handling logic. The entry point is `cohort_utils.nats.message_handler.cohort_request_handler`, which is called by `smile-client` for each message received on the subscribed subject.

### `anoronh4_smile-client_fork/`
A local copy of a fork of the `smile-client` package. This is the NATS listener framework that manages the connection to NATS, subscribes to the configured subject, and dispatches received messages to the configured callback function.

### `logs/`
Output directory for listener log files. Each run creates a new file named `smile_listener_<timestamp>_<env>.log`.

## Running the Listener

### Prerequisites

1. The `smile_cohort_listener` conda environment must exist with `smile-client` and `ccs_cohort_utils` installed (already created for svc_core005_bot04). This environment is activated inside `run.bash`.
2. TLS certificate files must be present at the paths specified in the relevant `smile_client_config_<env>.json`.
3. The `TEMPO_METADB_PROFILE` environment variable must be set to match the target environment (`local`, `dev`, or `prod`). This is typically handled by the `initialize_<env>.sh` script sourced inside `run.bash`.

### Starting the listener

```bash
bash run.bash -p <environment>
```

Where `<environment>` is one of:

| Value | NATS server | Description | CRF output | Embargo Date Record |
|-------|-------------|-------------|------------|---------------------|
| `local` | `nats://127.0.0.1:4222` | Local development. Requires a local NATS server (see below). | `.` | `embargo_dates_local.txt` |
| `dev` | `nats://smile-dev.mskcc.org:4222` | Development SMILE instance. | `.` | `embargo_dates_dev.txt` |
| `prod` | `nats://smile.mskcc.org:4222` | Production SMILE instance. | `/data1/core006/ccs_pipelines/tempo/wes_repo/Results/v2.1.x/cohort_level/` | `/data1/core006/ccs_pipelines/tempo/tempodeliver_wes_repo_v2.0.x/stage_runs/deliver_cohorts_v2.1.x/embargo_dates.txt` |

### Local development setup

Before running in `local` mode, start a local NATS server and create the required stream:

```bash
bash setup_nats_local.bash
```

Then start the listener:

```bash
bash run.bash -p local
```

Requires `nats-server` and the `nats` CLI to be installed and available in `PATH`.

