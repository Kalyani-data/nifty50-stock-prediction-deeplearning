import requests
import csv
import os
from datetime import datetime

# Step 1: Set up your News API key
api_key = "Your API-key "  # Replace with your NewsAPI key

# Step 2: Define the endpoint and parameters
url = "your API-key url"
params = {
    "q": "Nifty50 OR #Nifty50 OR NSE OR Nifty",  # Search for articles related to Nifty50
    "sortBy": "publishedAt",  # Sort articles by publication date
    "apiKey": api_key,  # Your API key
    "language": "en",  # Language of the news articles
    "pageSize": 100  # Number of articles per request (max 100)
}

# Step 3: Define the CSV filename using a relative path
data_dir = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(data_dir, exist_ok=True)  # Ensure the data directory exists
filename = os.path.join(data_dir, "news_data.csv")

# Step 4: Initialize a list to store all articles and a set to track unique URLs
all_articles = []
unique_urls = set()  # Set to keep track of URLs to avoid duplicates
max_articles = 500  # Define the number of articles you want to fetch
current_page = 1

# Step 5: Fetch articles in a loop until we reach the desired number or there are no more articles
while len(all_articles) < max_articles:
    # Update the page parameter for pagination
    params["page"] = current_page

    # Make a request to the API
    response = requests.get(url, params=params)

    # Check the response status
    if response.status_code == 200:
        # Parse the response JSON
        articles = response.json().get("articles", [])

        # Break the loop if no more articles are found
        if not articles:
            break

        # Add the fetched articles to the list and remove duplicates
        for article in articles:
            # Check if the article's URL is unique
            if article["url"] not in unique_urls:
                all_articles.append(article)
                unique_urls.add(article["url"])  # Add URL to the set

        # Check if we have fetched enough articles
        if len(all_articles) >= max_articles:
            break

        # Increment the page number for the next request
        current_page += 1

    else:
        # Handle errors
        print(f"Error: {response.status_code}")
        print(f"Response: {response.text}")
        break

# Step 6: Prepare new articles to be added to the CSV
new_articles = []
for article in all_articles:
    new_articles.append({
        "title": article["title"],
        "source": article["source"]["name"],
        "publishedAt": article["publishedAt"],
        "description": article["description"],
        "url": article["url"]
    })

# Step 7: Sort the new articles by 'publishedAt' date in descending order
new_articles.sort(key=lambda x: datetime.strptime(x["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"), reverse=True)

# Step 8: Write the filtered recent articles to the CSV file (overwrite existing file)
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["title", "source", "publishedAt", "description", "url"])
    writer.writeheader()
    writer.writerows(new_articles)

print(f"Recent news articles related to Nifty50 have been saved to {filename}")
print(f"Total articles saved: {len(new_articles)}")

# Function to fetch latest news data
def fetch_latest_news():
    try:
        # Define the path to the stored news CSV file
        filename = os.path.join(os.path.dirname(__file__), "data", "news_data.csv")

        # Read the stored news articles
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            news_list = [row for row in reader]

        return news_list  # Return list of latest news articles

    except Exception as e:
        print(f"Error reading news data: {e}")
        return []

