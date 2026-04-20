# PulseCheck Configuration
# This file holds all settings for our pipeline

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# CDC Data Sources - these are free public APIs
CDC_DATASETS = {
    "heart_disease": "https://data.cdc.gov/resource/i2vk-mgdh.json",
    "diabetes": "https://data.cdc.gov/resource/t8re-hy3w.json",
    "obesity": "https://data.cdc.gov/resource/hn4x-zwk7.json"
}

# How many records to fetch per API call
BATCH_SIZE = 1000

# Where to save raw data on our laptop
RAW_DATA_PATH = "data/raw/"

# Alert thresholds for data quality
QUALITY_THRESHOLDS = {
    "max_null_percentage": 10.0,  # Alert if more than 10% nulls
    "min_row_count": 100,         # Alert if fewer than 100 rows
    "max_duplicate_percentage": 5.0  # Alert if more than 5% duplicates
}

print("✅ PulseCheck config loaded successfully")