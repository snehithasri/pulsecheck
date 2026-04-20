# PulseCheck - CDC Data Fetcher
# This file fetches real health data from the CDC API

import requests
import pandas as pd
import json
import os
from datetime import datetime
from config import CDC_DATASETS, BATCH_SIZE, RAW_DATA_PATH

def fetch_cdc_dataset(dataset_name, url):
    """
    Fetches a single CDC dataset from their public API.
    Think of this as one truck delivery from the government.
    """
    print(f"🚚 Fetching {dataset_name} from CDC...")
    
    try:
        # Add limit parameter to control how many records we fetch
        full_url = f"{url}?$limit={BATCH_SIZE}"
        
        # Make the API call - like knocking on CDC's door
        response = requests.get(full_url, timeout=30)
        
        # Check if CDC answered the door successfully
        if response.status_code == 200:
            data = response.json()
            
            # Convert to pandas DataFrame - like organizing 
            # the delivery into a neat table
            df = pd.DataFrame(data)
            
            print(f"✅ Fetched {len(df)} records for {dataset_name}")
            print(f"📋 Columns: {list(df.columns)}")
            
            return df
        else:
            print(f"❌ Failed to fetch {dataset_name}")
            print(f"   Status code: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error fetching {dataset_name}: {e}")
        return None

def save_raw_data(df, dataset_name):
    """
    Saves raw data to our local data folder.
    Think of this as putting the delivery boxes
    in our storage room before unpacking them.
    """
    # Create the raw data folder if it doesn't exist
    os.makedirs(RAW_DATA_PATH, exist_ok=True)
    
    # Create filename with timestamp so we know 
    # exactly when data was fetched
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{RAW_DATA_PATH}{dataset_name}_{timestamp}.csv"
    
    # Save to CSV file
    df.to_csv(filename, index=False)
    print(f"💾 Saved to {filename}")
    
    return filename

def fetch_all_datasets():
    """
    Fetches ALL CDC datasets defined in our config.
    Think of this as receiving all trucks in one morning.
    """
    print("🏥 PulseCheck - Starting CDC Data Fetch")
    print("=" * 50)
    
    results = {}
    
    for dataset_name, url in CDC_DATASETS.items():
        # Fetch the data
        df = fetch_cdc_dataset(dataset_name, url)
        
        if df is not None:
            # Save it locally
            filename = save_raw_data(df, dataset_name)
            
            # Store results summary
            results[dataset_name] = {
                "rows": len(df),
                "columns": len(df.columns),
                "filename": filename,
                "status": "success"
            }
        else:
            results[dataset_name] = {
                "status": "failed"
            }
    
    # Print final summary
    print("\n" + "=" * 50)
    print("📊 Fetch Summary:")
    for name, result in results.items():
        if result["status"] == "success":
            print(f"  ✅ {name}: "
                  f"{result['rows']} rows, "
                  f"{result['columns']} columns")
        else:
            print(f"  ❌ {name}: failed")
    
    return results

# Run when executed directly
if __name__ == "__main__":
    fetch_all_datasets()