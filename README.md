# 📌Nifty50 Stock Market Prediction using Deep Learning 

A deep learning–based project that predicts the next day’s NIFTY 50 closing price using advanced  models like RNN, LSTM, Transformer(Encoder Only), and a hybrid(LSTM + Transformer). The best-performing model is integrated into a mobile application that also provides market sentiment analysis, generates Fear & Greed Index (FGI), and gives intelligent trading recommendations (Buy/Sell/Hold). The app is beginner-friendly and includes a learning hub for stock market concepts.

---

## 👥 Team Members

**Padala Kalyani**  
📩 padalakalyani66@gmail.com

**Co-member: Addada Sai Keerthana**  
📩 saikeerthana2720@gmail.com

---

## 🔍 Project Overview

This project delivers a robust NIFTY 50 stock forecasting and recommendation system that combines:

- Deep learning–based next-day closing price prediction.
- Real-time financial news sentiment analysis via FinBERT.
- Daily Fear & Greed Index (FGI) generated using technical and macroeconomic indicators.
- A mobile application for real-time interaction with predictions, trends, and financial news.
- Educational features for users to learn key stock market terms and tools.

Although various deep learning architectures, technical indicators, and sequence lengths were tested, only the best-performing version is included in the development of  mobile application.

---


## ⏳ Time Series Analysis

Thorough exploratory analysis was done to understand the structure of the data. This included:

- Trend and seasonality decomposition
- ACF and PACF plots for lag detection
- Augmented Dickey-Fuller (ADF) test for stationarity
- Rolling window visualizations
- Baseline modeling using ARIMA and SARIMA for comparison

This analysis helped identify optimal lag lengths and supported sequence selection for deep learning models.

---

## 🧠 Deep Learning Architectures Explored

We tested the following models:

- RNN
- LSTM (Unidirectional, Stacked, Bidirectional)
- Transformer (Encoder-only version)
- Hybrid model combining LSTM and Transformer

After rigorous evaluation, the best results were obtained from:

✅ **LSTM with sequence length of 60 days and Close Price as input**  
📉 **MAE:** 116.82  
📈 **RMSE:** 167.68

This version is used in the final mobile application development.

---

## ⚙️ How the Backend Works

The backend is built using Flask and performs the following daily automated tasks:

1. **Data Collection:**
   - Fetches the latest 60 days of NIFTY 50 data from Yahoo Finance.
   - Gathers the latest news articles related to NIFTY 50.

2. **Stock Price Prediction:**
   - The best LSTM model (trained with optimized hyperparameters) predicts the next day’s closing price.
   - Outputs include the predicted price and a realistic range.

3. **Market Sentiment:**
   - Uses the FinBERT pretrained model to analyze sentiment from the latest news articles.
   - Classifies sentiment as Positive, Negative, or Neutral.

4. **Fear & Greed Index (FGI):**
   - FGI is calculated using:
     - Technical indicators like SMA, EMA, RSI, MACD.
     - Macroeconomic factors like GDP, inflation rate, and interest rate.
   - The final score (0–100) is categorized into sentiments such as "Extreme Fear", "Fear", "Greed", and "Extreme Greed".
   - Historical FGI values are also stored and shown in the app.

5. **Recommendation Logic:**
   - Generates a trading recommendation (Buy / Sell / Hold) based on:
     - Today’s Close Price
     - Predicted Close Price
     - Market Sentiment
     - FGI Score
     - FGI Sentiment
   - Also generates a brief explanation behind the recommendation.

6. **Storage:**
   - Stores predictions and news sentiment daily.
   - Maintains historical prediction records for user tracking and comparison.

---


## 📱 Mobile Application Features

The mobile app is designed for real-time use and educational support. Built using Flutter and connected to the Flask backend.

### 🔮 Daily Prediction

Each daily prediction includes:

- 📅 Date of prediction
- 📈 Predicted Close Price (with upper and lower range)  
- 📰 Market Sentiment: Positive / Negative / Neutral  
- ✅ Recommendation: Buy / Sell / Hold  
- 💡 Explanation: Based on prediction trend, sentiment, and FGI

---
### 😱 Fear & Greed Index Page

- Shows daily FGI score (0–100)  
- Associated FGI sentiment (Fear,Greed, etc.)  
- Historical FGI chart available

---

### 📉 Past Predictions Page

- View historical actual vs predicted values  
- See FGI trend and past sentiment  
- Helps track model performance

---

### 📰 News & Sentiment Section

- Displays the latest NIFTY 50–related news articles  
- Each article includes sentiment classification using FinBERT  
- Tap to view the full article in browser

---

### 📚 Learning Hub

An educational section covering:

- Stock market basics  
- What is NIFTY 50  
- Key technical indicators (SMA, EMA, RSI, MACD)
- Additional links to explore more about Stock Market and Nifty50 

---



## 🛠️ Technologies Used

- **Deep Learning:** TensorFlow, Keras, PyTorch (FinBERT)  
- **Time Series Analysis:** ARIMA, SARIMA, ACF/PACF, decomposition  
- **APIs:** Yahoo Finance (`yfinance`), NewsAPI 
- **Frontend:** Flutter (mobile app)  
- **Backend:** Flask (Python)  
- **Sentiment Analysis:** FinBERT pretrained transformer  
- **Visualization:** Matplotlib, Seaborn

---


## 🚀 How to Run the Project

### Backend (Python)
```bash
cd backend
pip install -r requirements.txt
python app.py
```

---

### 📱 Mobile App Setup (Flutter)

#### 🔧 Prerequisites
- Flutter SDK installed
- Android Studio or Visual Studio Code
- Backend service running

---

#### 1. Navigate to the frontend
```bash
cd frontend/
```
Open the project in **Android Studio** or **VS Code**.

---

#### 2. Update Backend IP Address

Before running the app, update the backend IP address in the following files:

- `lib/services/api_service.dart`
- `lib/services/auth_service.dart`

Replace:
```dart
static String baseUrl = "http://<your-ip>:5000";
```

With your actual backend IP address or hosted URL. 

Example:
```dart
static String baseUrl = "http://192.168.1.100:5000";
```

---

#### 3. Get Dependencies & Run (Frontend)
```bash
flutter pub get
flutter run
```

Run the app on an **emulator** or a **physical device**.

---

## 🖼️ Screenshots & UI

### 👋 Welcome Screen
![Welcome Screen](mobile_application/images/welcome_page.png)

### 📝 Signup Screen
![Signup Screen](images/signup_screen.png)

### 🔐 Login Screen
![Login Screen](images/login_screen.png)

### 📄 Terms & Conditions
![Terms Screen](images/terms_screen.png)

### 🏠 Home Screen (Learning Hub)
![Home Screen](images/home_screen.png)

### 📊 Prediction Example
![Prediction Example](images/prediction_example_screen.png)

### 💡 Recommendation Explanation
![Recommendation Explanation](images/recommendation_explanation_screen.png)

### 🕒 Past Predictions
![Past Predictions](images/past_predictions_screen.png)

### 📈 FGI Index
![FGI Index](images/fgi_index_screen.png)

### 🕰️ Past FGI Index
![Past FGI Index](images/past_fgi_index_screen.png)

### 📰 Latest News Articles
![Latest News](images/latest_news_screen.png)

---

## 📫 Contact

For inquiries or collaboration:

- 📩 teamkk.stockai@gmail.com  
- 📩 sairam.stockai@gmail.com






