#!/bin/bash


set -e  # Exit immediately if a command exits with a non-zero status

# List of pytest commands, one per line
pytest_commands=(
    ### run local tests ###
    "python3.12 -m pytest tests/local/ -x"

    ### run local decoupled tests ###
    "python3.12 -m pytest tests/local_decoupled/receivers/test_receiver_start.py -x"
    "python3.12 -m pytest tests/local_decoupled/receivers/test_receiver_preprocess.py -x"
    "python3.12 -m pytest tests/local_decoupled/receivers/test_receiver_process.py -x"
    "python3.12 -m pytest tests/local_decoupled/receivers/test_receiver_end.py -x"

    ### run cloud decoupled tests ###
    "python3.12 -m pytest tests/cloud_decoupled/receivers/test_receiver_start.py -x"
    "python3.12 -m pytest tests/cloud_decoupled/receivers/test_receiver_preprocess.py -x"
    "python3.12 -m pytest tests/cloud_decoupled/receivers/test_receiver_process.py -x"
    "python3.12 -m pytest tests/cloud_decoupled/receivers/test_receiver_end.py -x"

    ### run cloud e2e tests ###
    "python3.12 -m pytest tests/cloud_e2e/test_receiver_circuit.py -x"

)

for cmd in "${pytest_commands[@]}"; do
  echo "Running: $cmd"
  $cmd
done






### deploy lambdas
# test_deploy_receivers.py




### run cloud tests ###
# python3.10 -m pytest tests/cloud/receivers
# python3.10 -m pytest tests/cloud/entrypoints

