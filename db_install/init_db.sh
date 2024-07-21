#!/bin/bash

# Install apps and python dependencies
sudo apt update -y
sudo apt install mysql-server python3-pip unzip jq -y
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
pip3 install sqlalchemy mysql-connector-python pandas

# Get credentials from secrets
SECRET_VALS=$(aws secretsmanager get-secret-value --secret-id /mysql/credentials --query SecretString)
export DB_USER=$(echo $SECRET_VALS | jq -r 'fromjson' | jq -r '.DB_USER')
export DB_PASSWORD=$(echo $SECRET_VALS | jq -r 'fromjson' | jq -r '.DB_PASSWORD')

# Initialize Database params, restart service
sudo mysql <<EOF
CREATE DATABASE canada_stats;
CREATE USER '$DB_USER'@'%' IDENTIFIED BY '$DB_PASSWORD';
GRANT ALL PRIVILEGES ON canada_stats.* TO '$DB_USER'@'%';
FLUSH PRIVILEGES;
EOF
sudo cp /etc/mysql/mysql.conf.d/mysqld.cnf /etc/mysql/mysql.conf.d/mysqld.cnf.backup
sudo sed -i 's/^bind-address.*$/bind-address = 0.0.0.0/' /etc/mysql/mysql.conf.d/mysqld.cnf
sudo systemctl restart mysql

# Get data
git clone https://github.com/jesusfberrios/canada_crime_stats.git
cd canada_crime_stats/db_install/
python3 init_database.py