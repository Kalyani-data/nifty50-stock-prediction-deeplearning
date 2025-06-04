import os
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F
import nltk

# 📚 Download required NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# 📂 Define relative paths for data
base_dir = os.path.dirname(__file__)  # Get the directory of the script
news_data_path = os.path.join(base_dir, "data", "news_data.csv")  # News data CSV
sentiment_output_path = os.path.join(base_dir, "data", "news_sentiment_results.csv")  # Sentiment results
market_sentiment_path = os.path.join(base_dir, "data", "market_sentiment.csv")  # Overall sentiment tracking

# 🎯 Load FinBERT model and tokenizer
MODEL_NAME = "ProsusAI/finbert"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# 📊 Load news data
df = pd.read_csv(news_data_path)

# 📝 Combine 'title' and 'description' for sentiment analysis
df["text"] = df["title"].fillna('') + " " + df["description"].fillna('')

# ====================== HELPER FUNCTION ======================

# 🎯 Function to get sentiment from FinBERT
def predict_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=-1)

    # Get class with highest probability
    sentiment_labels = ["negative", "neutral", "positive"]
    sentiment = sentiment_labels[torch.argmax(probs)]
    sentiment_score = probs[0][torch.argmax(probs)].item()

    return sentiment, sentiment_score

# ====================== SENTIMENT ANALYSIS ======================

# 🔥 Apply sentiment prediction to each row
df["Sentiment"], df["Sentiment_Score"] = zip(*df["text"].map(predict_sentiment))

# 📊 Determine overall sentiment
sentiment_counts = df["Sentiment"].value_counts()
overall_sentiment = sentiment_counts.idxmax()
overall_sentiment_score = df[df["Sentiment"] == overall_sentiment]["Sentiment_Score"].mean()

# ✅ Save sentiment analysis results to CSV
df.to_csv(sentiment_output_path, index=False)

# ====================== MARKET SENTIMENT SUMMARY ======================

# 📅 Prepare sentiment summary for tomorrow's date
tomorrow_date = (pd.Timestamp.today() + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
sentiment_summary = pd.DataFrame([{
    "Date": tomorrow_date,
    "Overall_Sentiment": overall_sentiment,
    "Sentiment_Score": round(overall_sentiment_score, 4),  # Rounded for clarity
    "Negative_Count": sentiment_counts.get("negative", 0),
    "Neutral_Count": sentiment_counts.get("neutral", 0),
    "Positive_Count": sentiment_counts.get("positive", 0)
}])

# ====================== UPDATE MARKET SENTIMENT ======================

# 📂 Check if market sentiment file exists
if os.path.exists(market_sentiment_path):
    market_df = pd.read_csv(market_sentiment_path)

    # 📅 Check if tomorrow's date already exists
    if tomorrow_date in market_df["Date"].values:
        # ✅ Correctly update the existing row
        market_df.loc[market_df["Date"] == tomorrow_date, "Overall_Sentiment"] = overall_sentiment
        market_df.loc[market_df["Date"] == tomorrow_date, "Sentiment_Score"] = round(overall_sentiment_score, 4)
        market_df.loc[market_df["Date"] == tomorrow_date, "Negative_Count"] = sentiment_counts.get("negative", 0)
        market_df.loc[market_df["Date"] == tomorrow_date, "Neutral_Count"] = sentiment_counts.get("neutral", 0)
        market_df.loc[market_df["Date"] == tomorrow_date, "Positive_Count"] = sentiment_counts.get("positive", 0)
    else:
        # ➕ Append the new sentiment summary if date not present
        market_df = pd.concat([market_df, sentiment_summary], ignore_index=True)
else:
    # 🆕 Create new file with the first sentiment summary
    market_df = sentiment_summary

# ====================== CLEAN AND SAVE DATA ======================

# 🧹 Drop duplicate rows by 'Date' before saving
market_df.drop_duplicates(subset="Date", keep="last", inplace=True)

# 🚫 Drop rows with all NaN values as a backup check
market_df.dropna(how="all", inplace=True)

# ✅ Save the updated file without duplicates or NaN values
market_df.to_csv(market_sentiment_path, index=False)

# ====================== DISPLAY RESULTS ======================

# 📰 Display sample sentiment results
print(df[["title", "Sentiment", "Sentiment_Score"]].head())

# 📊 Print sentiment distribution
print("\nSentiment Distribution:")
print(sentiment_counts)
print(f"\n✅ Overall Market Sentiment: {overall_sentiment} ({round(overall_sentiment_score, 4)})")

# ====================== EXTERNAL SENTIMENT FUNCTION ======================

# 📡 Function for external sentiment analysis
def analyze_sentiment(text):
    sentiment, sentiment_score = predict_sentiment(text)
    return sentiment, sentiment_score
