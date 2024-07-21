#!/bin/bash

# Clone repository and execute database init script
git clone https://github.com/jesusfberrios/canada_crime_stats.git
chmod +x canada_crime_stats/db_install/init_db.sh
canada_crime_stats/db_install/init_db.sh