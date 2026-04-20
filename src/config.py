# PulseCheck Configuration
# This file holds all settings for our pipeline

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# CDC Data Sources - these are free public APIs
CDC_DATASETS = {
    "obesity": "https://data.cdc.gov/resource/hn4x-zwk7.json",
    "nutrition": "https://data.cdc.gov/resource/pj7h-gcxc.json",
    "chronic_disease": "https://data.cdc.gov/resource/g4ie-h725.json"
}

# How many records to fetch per API call
BATCH_SIZE = 1000

# Where to save raw data on our laptop
# Build absolute path so scripts work from any directory
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_PATH = os.path.join(_PROJECT_ROOT, "data", "raw") + "/"

# Alert thresholds for data quality
QUALITY_THRESHOLDS = {
    "max_null_percentage": 10.0,  # Alert if more than 10% nulls
    "min_row_count": 100,         # Alert if fewer than 100 rows
    "max_duplicate_percentage": 5.0  # Alert if more than 5% duplicates
}

print("✅ PulseCheck config loaded successfully")