#!/bin/bash

# Install apps and python dependencies
sudo apt update -y
sudo apt install python3-pip unzip jq -y
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
pip3 install -r  canada_crime_stats/web_app/requirements_web.txt

# Get credentials from secrets
SECRET_VALS=$(aws secretsmanager get-secret-value --secret-id /mysql/credentials --query SecretString)
export DB_USER=$(echo $SECRET_VALS | jq -r 'fromjson' | jq -r '.DB_USER')
export DB_PASSWORD=$(echo $SECRET_VALS | jq -r 'fromjson' | jq -r '.DB_PASSWORD')
export DB_HOST=$(echo $SECRET_VALS | jq -r 'fromjson' | jq -r '.DB_HOST')

# Turn on app
nohup python3 canada_crime_stats/web_app/app.py >> app_logs.out &