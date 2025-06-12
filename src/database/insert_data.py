import cx_Oracle
import pandas as pd

#connect to oracle
dsn = cx_Oracle.makedsn("localhost", 1521, service_name="XE")
conn = cx_Oracle.connect(user="system", password="Mekdes12&meg", dsn=dsn)
cursor = conn.cursor()


banks_data = [
    ("Commercial Bank of Ethiopia", "com.combanketh.mobilebanking"),
    ("Bank of Abyssinia", "com.boa.boaMobileBanking"),
    ("Dashen Bank", "com.dashen.dashensuperapp")
]


for name, app_id in banks_data:
    cursor.execute("""
        SELECT COUNT(*) FROM tbl_banks WHERE name = :name OR app_id = :app_id
    """, {"name": name, "app_id": app_id})
    
    count, = cursor.fetchone()
    
    if count == 0:  # Insert only if it doesn't exist
        cursor.execute("""
            INSERT INTO tbl_banks (name, app_id) VALUES (:name, :app_id)
        """, {"name": name, "app_id": app_id})

conn.commit()


csv_paths = {
    "Commercial Bank of Ethiopia": "notebooks/processed_cbe_data_with_sentiment_reviews.csv",
    "Bank of Abyssinia": "notebooks/processed_boa_data_with_sentiment_reviews.csv",
    "Dashen Bank": "notebooks/processed_dashen_data_with_sentiment_reviews.csv",
}

# Insert reviews 
for bank_name, csv_path in csv_paths.items():
    print(f"Inserting data for {bank_name}...")
    
    #read NaN value
    df = pd.read_csv(csv_path).fillna({"sentiment_score": 0, "rating": 0})

    # Convert columns to numeric 
    df["sentiment_score"] = pd.to_numeric(df["sentiment_score"], errors="coerce").fillna(0)
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0)

    # Get bank_id dynamically
    cursor.execute("SELECT id FROM tbl_banks WHERE name = :name", {"name": bank_name})
    bank_id_row = cursor.fetchone()
    
    if bank_id_row:
        bank_id = bank_id_row[0]
    else:
        print(f"Skipping {bank_name}: Bank ID not found!")
        continue

    for _, row in df.iterrows():
        try:
            # Convert rating and sentiment_score safely
            rating = float(row["rating"]) if pd.notnull(row["rating"]) else 0
            sentiment_score = float(row["sentiment_score"]) if pd.notnull(row["sentiment_score"]) else 0

            cursor.execute("""
                INSERT INTO tbl_reviews (bank_id, review_text, rating, review_date, source, sentiment_label, sentiment_score)
                VALUES (:bank_id, :review_text, :rating, TO_DATE(:review_date, 'YYYY-MM-DD'), :source, :sentiment_label, :sentiment_score)
            """, {
                "bank_id": bank_id,
                "review_text": row["review"],
                "rating": rating,
                "review_date": row["date"],
                "source": row["source"],
                "sentiment_label": row.get("sentiment_label", ""),
                "sentiment_score": sentiment_score
            })
        except Exception as e:
            print(f"Skipping row due to error: {e}")
            continue

conn.commit()
cursor.close()
conn.close()

print("✅ Data inserted successfully!")
