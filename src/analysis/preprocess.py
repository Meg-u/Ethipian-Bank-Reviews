# Data cleaning pipeline
import pandas as pd
import os

# Create processed directory 
os.makedirs('data/processed', exist_ok=True)

# List all raw CSV files
raw_dir = 'data/raw'
processed_dir = 'data/processed'

for filename in os.listdir(raw_dir):
    if filename.endswith('.csv'):
        filepath = os.path.join(raw_dir, filename)
        print(f"Processing {filename}...")

        # Load the data
        df = pd.read_csv(filepath)

        # Rename if needed (some versions have 'content' instead of 'review')
        if 'content' in df.columns and 'review' not in df.columns:
            df.rename(columns={'content': 'review'}, inplace=True)

        # Drop duplicates and rows with missing reviews or ratings
        df.drop_duplicates(subset=['review'], inplace=True)
        df.dropna(subset=['review', 'score', 'at'], inplace=True)

        # Normalize date format
        df['date'] = pd.to_datetime(df['at']).dt.strftime('%Y-%m-%d')

        # Rename and select only necessary columns
        df_clean = df[['review', 'score', 'date', 'bank', 'source']]
        df_clean.rename(columns={'score': 'rating'}, inplace=True)

        # Save to processed directory
        clean_path = os.path.join(processed_dir, filename.replace('raw', 'cleaned'))
        df_clean.to_csv(clean_path, index=False)
        print(f"Saved cleaned data to {clean_path}")
