#!/bin/bash

# first input argument is stage
stage=$1

# run deploy script for stage
echo "Deploying $stage stage..."
python stage_launcher/deploy_stage.py $stage
echo "Finished deploying $stage stage"

