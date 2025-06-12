# dashboard.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import os

st.set_page_config(page_title="Ethiopian Bank Reviews Dashboard", layout="wide")

# Load cleaned and analyzed data
@st.cache_data
def load_data():
    cbe = pd.read_csv("../notebooks/processed_cbe_data_with_sentiment_reviews.csv")
    boa = pd.read_csv("../notebooks/processed_boa_data_with_sentiment_reviews.csv")
    dashen = pd.read_csv("../notebooks/processed_dashen_data_with_sentiment_reviews.csv")
    return cbe, boa, dashen

cbe_df, boa_df, dashen_df = load_data()

# Sidebar selection
bank_option = st.sidebar.selectbox("Select a Bank", ["CBE", "BOA", "Dashen"])
bank_map = {"CBE": cbe_df, "BOA": boa_df, "Dashen": dashen_df}
df = bank_map[bank_option]

st.title(f"{bank_option} Bank Review Analysis")

# Metrics summary
st.subheader("Summary Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Reviews", len(df))
col2.metric("Average Rating", round(df['rating'].mean(), 2))
col3.metric("Average Sentiment Score", round(df['sentiment_score'].mean(), 2))

# Plot - Sentiment Distribution
st.subheader("Sentiment Distribution")
sentiment_fig, ax = plt.subplots()
sns.histplot(df['sentiment_score'], kde=True, ax=ax, color='skyblue')
ax.set_title("Sentiment Score Distribution")
st.pyplot(sentiment_fig)

# Plot - Rating Distribution
st.subheader("Rating Distribution")
rating_fig, ax = plt.subplots()
sns.countplot(x='rating', data=df, ax=ax, palette='Set2')
ax.set_title("Rating Distribution")
st.pyplot(rating_fig)

# Word Cloud for Themes
st.subheader("Common Themes (Word Cloud)")
themes = [theme for sublist in df['themes'].dropna().apply(eval) for theme in sublist]
theme_text = ' '.join(themes)
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(theme_text)

fig_wc, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig_wc)

st.info("Dashboard by [Your Name], 2025. Powered by Streamlit.")
