import requests
import pandas as pd
import os

def fetch_and_save_gdp_data():
    # ✅ API URL for India's GDP in current USD
    url = "Your API-Url"

    # 📡 Fetch data from World Bank API
    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # ✅ Check if valid data is returned
            if len(data) > 1 and isinstance(data[1], list):
                gdp_data = []

                # 🔄 Loop through all available data and store non-null values
                for record in data[1]:
                    if record['value'] is not None:
                        year = record['date']
                        gdp_value = round(float(record['value']), 2)
                        gdp_data.append({"Year": year, "GDP": gdp_value})

                # ✅ Create DataFrame and Save to CSV
                if gdp_data:
                    df = pd.DataFrame(gdp_data)

                    # Create data folder if it doesn't exist
                    data_folder = "./data"
                    os.makedirs(data_folder, exist_ok=True)

                    csv_file_path = os.path.join(data_folder, "gdp_data.csv")
                    df.to_csv(csv_file_path, index=False)

                    print(f"✅ GDP data saved to {csv_file_path}")
                    print(df.head())  # Show top 5 rows for confirmation
                else:
                    print("⚠️ No valid GDP data found.")
            else:
                print("❌ Invalid response format.")
        else:
            print(f"❌ Failed to fetch data. Status Code: {response.status_code}")

    except Exception as e:
        print(f"❌ Error fetching GDP data: {str(e)}")

# 🚀 Call the function to fetch and save GDP data
fetch_and_save_gdp_data()
