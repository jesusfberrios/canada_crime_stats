#!/bin/bash

# Clone repository and execute database init script
git clone https://github.com/jesusfberrios/canada_crime_stats.git
chmod +x install -r  canada_crime_stats/db_install/init_app.sh
canada_crime_stats/db_install/user_data_web.sh