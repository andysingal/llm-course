import streamlit as st
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from nltk.sentiment import SentimentIntensityAnalyzer

# Load pre-trained sentiment models
MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(comment):
    # VADER sentiment analysis
    vader_result = sia.polarity_scores(comment)
    
    # Roberta sentiment analysis
    encoded_text = tokenizer(comment, return_tensors='pt')
    output = model(**encoded_text)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    roberta_result = {
        'roberta_neg': scores[0],
        'roberta_neu': scores[1],
        'roberta_pos': scores[2]
    }

    return {'vader': vader_result, 'roberta': roberta_result}

# Streamlit App
st.title("Sentiment Analysis App")

comment = st.text_area("Enter your comment:")
if st.button("Analyze"):
    if comment:
        result = analyze_sentiment(comment)

        st.subheader("VADER Sentiment Analysis:")
        st.write(result['vader'])

        st.subheader("Roberta Sentiment Analysis:")
        st.write(result['roberta'])

        # You can further customize the display as needed
    else:
        st.warning("Please enter a comment for analysis.")
