import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os

# Initialize the sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Paths to your review CSVs — update if your filenames or paths are different
bank_files = {
    "CBE": "data/processed/commercial_bank_of_ethiopia_cleaned_reviews.csv",
    "Abyssinia": "data/processed/bank_of_abyssinia_cleaned_reviews.csv",
    "Dashen": "data/processed/dashen_bank_cleaned_reviews.csv"


}

# Output folder
os.makedirs("outputs/task-2/sentiment", exist_ok=True)

# Function to classify sentiment
def get_sentiment_label(score):
    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    else:
        return "neutral"

# Apply sentiment analysis to each bank
for bank, path in bank_files.items():
    df = pd.read_csv(path)

    df['sentiment_score'] = df['review'].apply(lambda x: analyzer.polarity_scores(str(x))['compound'])
    df['sentiment_label'] = df['sentiment_score'].apply(get_sentiment_label)

    output_path = f"outputs/task-2/sentiment/{bank.lower()}_sentiment.csv"
    df.to_csv(output_path, index=False)
    print(f"✅ Sentiment analysis completed for {bank} → {output_path}")
