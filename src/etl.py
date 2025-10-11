import pandas as pd
import re

# Note: Most encoding fixings for uncommon characters were solved using DeepSeek.

def run_etl(input_path: str) -> pd.DataFrame:
    print("\n=== EXTRACT: SAMPLE OF ORIGINAL DATA ===")
    print("Loading data from: ", input_path)
    
    # Load with specific encoding for Indian characters
    try:
        df = pd.read_csv(input_path, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(input_path, encoding='latin-1')
        except:
            df = pd.read_csv(input_path, encoding='iso-8859-1')

    print(f"\nOriginal data shape: {df.shape}")
    print("Original columns:", list(df.columns))
    
    # Clear column names
    df.columns = (
        df.columns
        .str.strip()
        .str.replace("ï»¿", "")
        .str.replace("â", "a")
        .str.lower()
        .str.replace(" ", "_")
    )

    print("\n=== DEBUG: SAMPLE OF ORIGINAL DATA ===")
    print(df[['discounted_price', 'actual_price', 'discount_percentage', 'rating_count']].head(3))

    print("\n=== TRANSFORM: CLEANING NUMERIC COLUMNS ===")
    
    # Apply specific cleaning
    def clean_currency(value):
        if pd.isna(value):
            return None
        value_str = str(value)
        value_str = re.sub(r'[â‚¹₹]', '', value_str)
        # Remove any other non-numeric characters except . and ,
        value_str = re.sub(r'[^\d.,]', '', value_str)
        value_str = value_str.replace(',', '')
        try:
            return float(value_str)
        except:
            print(f"Warning: Could not convert '{value}' to float, cleaned to '{value_str}'")
            return None

    def clean_percentage(value):
        if pd.isna(value):
            return None
        value_str = str(value)
        # Remove percent symbol and spaces
        value_str = value_str.replace('%', '').strip()
        try:
            return float(value_str)
        except:
            print(f"Warning: Could not convert percentage '{value}' to float")
            return None

    def clean_rating_count(value):
        if pd.isna(value):
            return None
        value_str = str(value)
        # Remove thousands commas
        value_str = value_str.replace(',', '')
        try:
            return float(value_str)
        except:
            print(f"Warning: Could not convert rating count '{value}' to float")
            return None
    
    if "discounted_price" in df.columns:
        print("Cleaning discounted_price...")
        df["discounted_price"] = df["discounted_price"].apply(clean_currency)
    
    if "actual_price" in df.columns:
        print("Cleaning actual_price...")
        df["actual_price"] = df["actual_price"].apply(clean_currency)
    
    if "discount_percentage" in df.columns:
        print("Cleaning discount_percentage...")
        df["discount_percentage"] = df["discount_percentage"].apply(clean_percentage)
    
    if "rating_count" in df.columns:
        print("Cleaning rating_count...")
        df["rating_count"] = df["rating_count"].apply(clean_rating_count)
    
    # Convert rating normally (no special symbols)
    if "rating" in df.columns:
        df["rating"] = pd.to_numeric(df["rating"], errors='coerce')

    print("\n=== DEBUG: SAMPLE AFTER CLEANING ===")
    print(df[['discounted_price', 'actual_price', 'discount_percentage', 'rating_count']].head(3))

    print("\n=== TRANSFORM: REMOVE ROWS WITH NULL VALUES ===")

    # Only delete rows where product_id and product_name are null
    initial_count = len(df)
    df = df.dropna(subset=["product_id", "product_name"])
    print(f"Removed {initial_count - len(df)} rows with missing product_id or product_name")

    # Create derived columns only if there are valid prices
    if "actual_price" in df.columns and "discounted_price" in df.columns:
        valid_mask = (df["actual_price"].notna()) & (df["discounted_price"].notna())
        df.loc[valid_mask, "profit_margin"] = df.loc[valid_mask, "actual_price"] - df.loc[valid_mask, "discounted_price"]
        df.loc[valid_mask, "discount_ratio"] = df.loc[valid_mask, "discounted_price"] / df.loc[valid_mask, "actual_price"]

    print("\n=== LOAD: FINAL DATA SUMMARY ===")

    output_path = "data/standardized_sales.csv"
    # Save with encoding that preserves special characters
    df.to_csv(output_path, index=False, encoding='utf-8')

    print(f"\n✅ Final data shape: {df.shape}")
    print(f"✅ Data saved to: {output_path}\n")

    numeric_cols = ["discounted_price", "actual_price", "discount_percentage", "rating", "rating_count"]
    for col in numeric_cols:
        if col in df.columns:
            non_null = df[col].notna().sum()
            print(f"{col}: {non_null}/{len(df)} non-null values")
    
    return df