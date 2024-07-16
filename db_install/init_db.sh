#!/bin/bash

# Variables
PGUSER="postgres"
NEW_USER="my_service_user"
NEW_PASSWORD="mypassword"
NEW_DB="canada_stats"
CSV_FILE="/path/to/your/data.csv"
TABLE_NAME="crime_stats"


sudo apt install mysql-server
sudo apt install python3-pip
pip3 install sqlalchemy mysql-connector-python pandas

CREATE DATABASE canada_stats;
CREATE USER 'db_user'@'%' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON canada_stats.* TO 'db_user'@'%';
FLUSH PRIVILEGES;
EXIT;

sudo cp /etc/mysql/mysql.conf.d/mysqld.cnf /etc/mysql/mysql.conf.d/mysqld.cnf.backup
sudo sed -i 's/^bind-address.*$/bind-address = 0.0.0.0/' /etc/mysql/mysql.conf.d/mysqld.cnf
sudo systemctl restart mysql


mkdir data 
cd data
wget https://raw.githubusercontent.com/jesusfberrios/canada_crime_stats/main/data/homicides.csv
wget https://raw.githubusercontent.com/jesusfberrios/canada_crime_stats/main/data/persons_charged.csv
wget https://raw.githubusercontent.com/jesusfberrios/canada_crime_stats/main/data/provinces.csv

export DBUSER="db_userdfsadafd"
export DBPASS="db_passcsdafcdsf"

python3 init_database.py