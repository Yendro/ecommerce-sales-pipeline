"""
Project: Amazon Sales ETL & Dashboard
Description: This script runs the entire project flow.
Author: Yendri Hernández
Year: 2025
"""

from src import etl, load_to_db

def main():
    try:
        print("Starting Amazon data pipeline\n")

        # Cleaning and standardization
        df_clean = etl.run_etl("data/amazon.csv")

        # Simulated loading to the Data Warehouse (SQLite) 
        load_to_db.load_data_to_sqlite(df_clean)

        print("\n✅ Process completed successfully. Run the dashboard with:")
        print("   streamlit run src/dashboard.py")

    except FileNotFoundError:
        print("Error: File 'amazon.csv' not found in data/ folder")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()