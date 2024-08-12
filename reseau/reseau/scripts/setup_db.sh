#!/bin/sh

# Set the PYTHONPATH to include the parent directory of the scripts
export PYTHONPATH=$(dirname $(dirname $(realpath $0)))

# Execute Python scripts to fill the database with required data
# Usage: ./setup_db.sh

python3 reseau/scripts/cities.py
python3 reseau/scripts/interests.py
