#!/bin/bash

# run scraping functions

python3 console.py

# cd into dbt folder

cd trades_dbt

# transform dating using dbt

dbt run --profiles-dir ./dbt_profiles