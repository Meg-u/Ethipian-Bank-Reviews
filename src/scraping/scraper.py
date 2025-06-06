from google_play_scraper import reviews, Sort
import pandas as pd
import os

# Define the apps and their corresponding bank names
apps = {
    'com.combanketh.mobilebanking': 'Commercial Bank of Ethiopia',
    'com.boa.boaMobileBanking': 'Bank of Abyssinia',
    'com.dashen.dashensuperapp': 'Dashen Bank'
}

# Ensure the raw data directory exists
os.makedirs('data/raw', exist_ok=True)

# Iterate over each app to scrape reviews
for app_id, bank_name in apps.items():
    print(f"Scraping reviews for {bank_name}...")
    all_reviews = []
    count = 0
    batch_size = 200  # Number of reviews to fetch per batch
    while count < 400:
        try:
            result, _ = reviews(
                app_id,
                lang='en',
                country='us',
                sort=Sort.NEWEST,
                count=batch_size,
                filter_score_with=None
            )
            if not result:
                break
            all_reviews.extend(result)
            count += len(result)
            print(f"Collected {count} reviews so far for {bank_name}...")
        except Exception as e:
            print(f"An error occurred while fetching reviews for {bank_name}: {e}")
            break

    # Create a DataFrame from the collected reviews
    df = pd.DataFrame(all_reviews)
    df['bank'] = bank_name
    df['source'] = 'Google Play'

    # Save the DataFrame to a CSV file
    filename = f"data/raw/{bank_name.replace(' ', '_').lower()}_reviews.csv"
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} reviews for {bank_name} to {filename}")
