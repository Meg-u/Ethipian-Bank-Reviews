from google_play_scraper import reviews, Sort
import pandas as pd
import os
from langdetect import detect

# Define the apps and their corresponding bank names
apps = {
    'com.combanketh.mobilebanking': 'Commercial Bank of Ethiopia',
    'com.boa.boaMobileBanking': 'Bank of Abyssinia',
    'com.dashen.dashensuperapp': 'Dashen Bank'
}


os.makedirs('data/raw', exist_ok=True)

# Scrape English reviews
for app_id, bank_name in apps.items():
    print(f"\nScraping English reviews for {bank_name}...")
    all_english_reviews = []
    fetched = 0
    batch_size = 200
    continuation_token = None

    while len(all_english_reviews) < 400:
        try:
            result, continuation_token = reviews(
                app_id,
                lang='en', country='us',
                sort=Sort.NEWEST,
                count=batch_size,
                filter_score_with=None,
                continuation_token=continuation_token
            )

            if not result:
                print("No more reviews available.")
                break

            # Filter only English ones from this batch
            for r in result:
                try:
                    if detect(r['content']) == 'en':
                        all_english_reviews.append(r)
                except:
                    continue  

            fetched += len(result)
            print(f"Fetched {fetched} total, {len(all_english_reviews)} English reviews so far...")

        except Exception as e:
            print(f"Error fetching for {bank_name}: {e}")
            break

    # Save to CSV
    df = pd.DataFrame(all_english_reviews)
    df['bank'] = bank_name
    df['source'] = 'Google Play'

    filename = f"data/raw/{bank_name.replace(' ', '_').lower()}_reviews.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Saved {len(df)} English reviews for {bank_name} to {filename}")
