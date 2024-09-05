import requests
import csv

# API endpoint
url = "https://api.coincap.io/v2/assets"

# Send a GET request to the API
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON data
    data = response.json()

    # Extract the list of assets from the 'data' key in the JSON response
    assets = data['data']

    # Specify the CSV file's column headers
    csv_columns = ['id', 'rank', 'name', 'symbol', 'supply', 'maxSupply', 'marketCapUsd', 'volumeUsd24Hr', 'priceUsd', 'changePercent24Hr']

    # Write data to a CSV file
    csv_file = "cryptocurrency_data.csv"
    try:
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=csv_columns)
            writer.writeheader()
            
            for asset in assets:
                # Filter the asset data to include only the fields in csv_columns
                filtered_asset = {key: asset.get(key, '') for key in csv_columns}
                writer.writerow(filtered_asset)
                
        print(f"Data successfully written to {csv_file}")
    except IOError:
        print("I/O error while writing to CSV")
else:
    print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")
