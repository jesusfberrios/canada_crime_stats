#!/bin/bash

# Install apps and python dependencies
sudo apt update -y
sudo apt install python3-pip unzip jq -y
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
git clone https://github.com/jesusfberrios/canada_crime_stats.git
#pip3 install sqlalchemy mysql-connector-python pandas 
pip3 install -r  canada_crime_stats/web_app/requirements.txt

# Get credentials from secrets
export DB_USER=$(aws secretsmanager get-secret-value --secret-id /mysql/credentials --query SecretString | jq -r 'fromjson' | jq -r '.DB_USER')
export DB_PASSWORD=$(aws secretsmanager get-secret-value --secret-id /mysql/credentials --query SecretString | jq -r 'fromjson' | jq -r '.DB_PASSWORD')
export DB_HOST=$(aws secretsmanager get-secret-value --secret-id /mysql/credentials --query SecretString | jq -r 'fromjson' | jq -r '.DB_HOST')

# Get data
git clone https://github.com/jesusfberrios/canada_crime_stats.git
cd canada_crime_stats/db_install/
python3 init_database.py
