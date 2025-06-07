import pandas as pd
import os

banks = ["cbe", "abyssinia", "dashen"]

for bank in banks:
    path = f"outputs/task-2/sentiment/{bank}_sentiment.csv"
    df = pd.read_csv(path)

    if 'rating' not in df.columns:
        print(f"⚠️ No 'rating' column in {bank}, skipping aggregation.")
        continue

    agg = df.groupby('rating').agg(
        avg_sentiment=('sentiment_score', 'mean'),
        review_count=('review', 'count'),
        positive_reviews=('sentiment_label', lambda x: (x == 'positive').sum()),
        negative_reviews=('sentiment_label', lambda x: (x == 'negative').sum()),
        neutral_reviews=('sentiment_label', lambda x: (x == 'neutral').sum())
    ).reset_index()

    agg.to_csv(f"outputs/task-2/sentiment/{bank}_sentiment_aggregated.csv", index=False)
    print(f"✅ Aggregated sentiment saved for {bank}")
