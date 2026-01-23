import os
import csv
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Supabase credentials
SUPABASE_URL = os.getenv('REACT_APP_URL') # e.g., https://abcdefgh.supabase.co
SUPABASE_KEY = os.getenv('REACT_APP_KEY')  # Your anon/service key
TABLE_NAME = "data"  # Change if your table has a different name
CSV_FILE_PATH = "./src/dataset/dataset.csv"  # Path to your CSV file

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_csv_file():
    try:
        # Read CSV file
        with open(CSV_FILE_PATH, 'r', encoding='utf-8') as f:
            csv_reader = csv.DictReader(f)
            rows = list(csv_reader)
        
        print(f"Found {len(rows)} rows in CSV")
        print(f"Supabase URL: {SUPABASE_URL}")
        
        success_count = 0
        error_count = 0
        
        # Option 1: Insert all rows at once (faster, but fails if any row has issues)
        # try:
        #     result = supabase.table(TABLE_NAME).insert(rows).execute()
        #     print(f"✓ Uploaded all {len(rows)} rows")
        #     success_count = len(rows)
        # except Exception as e:
        #     print(f"✗ Bulk insert failed: {str(e)}")
        #     error_count = len(rows)
        
        # Option 2: Insert rows one by one (slower, but shows which rows fail)
        for i, row in enumerate(rows, 1):
            try:
                result = supabase.table(TABLE_NAME).insert(row).execute()
                print(f"✓ Uploaded row {i}/{len(rows)}")
                success_count += 1
            except Exception as e:
                print(f"✗ Error with row {i}: {str(e)}")
                error_count += 1
        
        print(f"\n--- Summary ---")
        print(f"Successful: {success_count}")
        print(f"Errors: {error_count}")
        
    except FileNotFoundError:
        print(f"✗ CSV file not found: {CSV_FILE_PATH}")
    except Exception as e:
        print(f"✗ Error reading CSV: {str(e)}")

if __name__ == "__main__":
    upload_csv_file()