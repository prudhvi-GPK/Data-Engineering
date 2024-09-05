import requests
import psycopg2
from psycopg2 import sql

# API endpoint
url = "https://api.coincap.io/v2/assets"

# Database connection parameters
db_params = {
    "host": "localhost",  # Replace with your actual host
    "database": "assets",  # Replace with your database name
    "user": "postgres",  # Replace with your username
    "password": "Luffy10$"  # Replace with your password
}

# Send a GET request to the API
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON data
    data = response.json()

    # Extract the list of assets from the 'data' key in the JSON response
    assets = data['data']

    # Perform ETL operations
    processed_assets = []
    for asset in assets:
        # Extract only the required fields
        processed_asset = {
            'id': asset['id'],
            'name': asset['name'],
            'symbol': asset['symbol'],
            'price': round(float(asset['priceUsd']), 2),
            'price_change': round(float(asset['changePercent24Hr']), 3)
        }
        
        # Transform: Add a 'performance' field based on price change
        if processed_asset['price_change'] > 5:
            processed_asset['performance'] = 'Excellent'
        elif processed_asset['price_change'] > 0:
            processed_asset['performance'] = 'Good'
        elif processed_asset['price_change'] > -5:
            processed_asset['performance'] = 'Fair'
        else:
            processed_asset['performance'] = 'Poor'
        
        # Load: Add the processed asset to our list
        processed_assets.append(processed_asset)
    
    # Initialize conn and cur variables
    conn = None
    cur = None

    # Connect to the PostgreSQL database
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Create table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS crypto_assets (
                id VARCHAR(50) PRIMARY KEY,
                name VARCHAR(100),
                symbol VARCHAR(10),
                price NUMERIC(20, 2),
                price_change NUMERIC(10, 3),
                performance VARCHAR(20)
            )
        """)

        # Insert data into the table
        insert_query = sql.SQL("""
            INSERT INTO crypto_assets (id, name, symbol, price, price_change, performance)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
                name = EXCLUDED.name,
                symbol = EXCLUDED.symbol,
                price = EXCLUDED.price,
                price_change = EXCLUDED.price_change,
                performance = EXCLUDED.performance
        """)

        for asset in processed_assets:
            cur.execute(insert_query, (
                asset['id'],
                asset['name'],
                asset['symbol'],
                asset['price'],
                asset['price_change'],
                asset['performance']
            ))

        # Commit the transaction
        conn.commit()

        print(f"Successfully loaded {len(processed_assets)} assets into the database.")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL or inserting data:", error)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
            print("PostgreSQL connection is closed")

else:
    print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")
