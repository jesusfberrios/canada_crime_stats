#!/bin/bash

# Clone repository and execute database init script
git clone https://github.com/jesusfberrios/canada_crime_stats.git
chmod +x canada_crime_stats/web_app/init_web.sh
canada_crime_stats/web_app/init_web.sh