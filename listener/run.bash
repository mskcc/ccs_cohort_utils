#!/bin/bash

# -----------------------------------------------
# Usage/help message
# -----------------------------------------------
usage() {
    echo "Usage: $(basename "$0") -p <environment> [-h]"
    echo ""
    echo "Options:"
    echo "  -p <environment>   Specify the environment to target."
    echo "                     Accepted values: local, dev, prod"
    echo "  -h                 Show this help message and exit."
    echo ""
    echo "Examples:"
    echo "  $(basename "$0") -p local"
    echo "  $(basename "$0") -p prod"
}

# -----------------------------------------------
# Parse options
# -----------------------------------------------
PROFILE=""

while getopts ":p:h" opt; do
    case "$opt" in
        p)
            PROFILE="$OPTARG"
            ;;
        h)
            usage
            exit 0
            ;;
        :)
            echo "Error: Option -$OPTARG requires an argument." >&2
            usage
            exit 1
            ;;
        \?)
            echo "Error: Unknown option -$OPTARG" >&2
            usage
            exit 1
            ;;
    esac
done

# -----------------------------------------------
# Validate -p value
# -----------------------------------------------
if [[ -z "$PROFILE" ]]; then
    echo "Error: -p <environment> is required." >&2
    usage
    exit 1
fi

case "$PROFILE" in
    local|dev|prod)
        ;;
    *)
        echo "Error: Invalid value for -p: '$PROFILE'" >&2
        echo "Accepted values: local, dev, prod" >&2
        exit 1
        ;;
esac

# -----------------------------------------------
# Main logic — add your code below
# -----------------------------------------------
echo "Running in environment: $PROFILE"

. "/home/svc_core005_bot04/miniforge3/etc/profile.d/conda.sh"
conda activate smile_cohort_listener

currentdate=$(date '+%Y-%m-%d-%H-%M-%S')
mkdir -p logs

# Example: branch on environment
case "$PROFILE" in
    local)
        echo "Starting local setup..."
	source /home/svc_core005_bot04/metadb_certs/initialize_local.sh
	logfile=logs/smile_listener_${currentdate}_local.log
	echo "Starting log file at $logfile..."
	smile-client start_listener --config=/home/svc_core005_bot04/metadb_certs/smile_client_config_local.json --subject="MDB_STREAM.consumers.tempo.*" --debug &> $logfile
        ;;
    dev)
        echo "Deploying to dev..."
	source /home/svc_core005_bot04/metadb_certs/initialize_dev.sh
	logfile=logs/smile_listener_${currentdate}_dev.log
	echo "Starting log file at $logfile..."
	smile-client start_listener --config=/home/svc_core005_bot04/metadb_certs/smile_client_config_dev.json --subject="MDB_STREAM.consumers.tempo.*" --debug &> $logfile
        ;;
    prod)
        echo "Deploying to prod..."
	source /home/svc_core005_bot04/metadb_certs/initialize_prod.sh
	logfile=logs/smile_listener_${currentdate}_prod.log
	echo "Starting log file at $logfile..."
	smile-client start_listener --config=/home/svc_core005_bot04/metadb_certs/smile_client_config_prod.json --subject="MDB_STREAM.consumers.tempo.*" --debug &> $logfile
        ;;
esac

