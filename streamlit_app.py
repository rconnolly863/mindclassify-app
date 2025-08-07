import streamlit as st
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
nltk.download("vader_lexicon")

# Load model and vectorizer
model = joblib.load("model.joblib")
vectorizer = joblib.load("vectorizer.joblib")

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

# App layout
st.title("🧠 MindClassify – Mental Health Text Classifier")
st.markdown("Paste a Reddit-style mental health post below. The app will predict the most likely subreddit and analyze its tone.")

# User input
user_input = st.text_area("Enter your Reddit-style post here:", height=200)

if st.button("Classify"):
    if not user_input.strip():
        st.warning("Please enter some text.")
    else:
        # Clean and vectorize input
        cleaned = user_input.lower()
        X_input = vectorizer.transform([cleaned])

        # Predict condition
        prediction = model.predict(X_input)[0]
        probabilities = model.predict_proba(X_input)[0]

        # Analyze sentiment
        sentiment_score = sia.polarity_scores(user_input)["compound"]

        # Display results
        st.subheader("🧾 Prediction")
        st.write(f"**Predicted Mental Health Condition:** `{prediction}`")
        st.write(f"**Sentiment Score (VADER):** `{sentiment_score:.2f}`")

        # Show prediction confidence
        st.subheader("📊 Model Confidence")
        prob_df = pd.DataFrame({
            "Condition": model.classes_,
            "Probability": probabilities
        }).sort_values(by="Probability", ascending=False)

        st.bar_chart(prob_df.set_index("Condition"))

