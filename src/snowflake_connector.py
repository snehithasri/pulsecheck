# PulseCheck - Snowflake Connection
# This file handles all communication between Python and Snowflake

import snowflake.connector
import os
from dotenv import load_dotenv

# Load our secret passwords from .env file
load_dotenv()

def get_snowflake_connection():
    """
    Creates and returns a connection to Snowflake.
    Think of this like opening a phone call to Snowflake.
    """
    try:
        conn = snowflake.connector.connect(
            account=os.getenv('SNOWFLAKE_ACCOUNT'),
            user=os.getenv('SNOWFLAKE_USER'),
            password=os.getenv('SNOWFLAKE_PASSWORD'),
            database=os.getenv('SNOWFLAKE_DATABASE'),
            warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
            schema=os.getenv('SNOWFLAKE_SCHEMA')
        )
        print("✅ Connected to Snowflake successfully!")
        return conn
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return None

def test_connection():
    """
    Tests our Snowflake connection by running a simple query.
    Think of this like saying 'hello' after picking up the phone.
    """
    conn = get_snowflake_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_VERSION()")
        version = cursor.fetchone()
        print(f"✅ Snowflake version: {version[0]}")
        cursor.close()
        conn.close()
        print("✅ Connection closed cleanly")

# Run the test when we execute this file directly
if __name__ == "__main__":
    test_connection()