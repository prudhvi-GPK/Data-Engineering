# Cryptocurrency Data ETL

This project contains two scripts for extracting cryptocurrency data from the CoinCap API and storing it either in a CSV file or a PostgreSQL database.

## Requirements

- Python 3.6+
- `requests` library
- `psycopg2` library (for PostgreSQL version only)

Install the required libraries using: pip


## 1. CSV Export Script

### Description
This script fetches cryptocurrency data from the CoinCap API and exports it to a CSV file.

### Usage
1. Ensure you have the required libraries installed.
2. Run the script:python crypto_to_csv.py
3. The script will create a file named `cryptocurrency_data.csv` in the same directory.

### Features
- Fetches real-time cryptocurrency data
- Exports data to a CSV file
- Includes error handling for API requests and file operations

## 2. PostgreSQL Import Script

### Description
This script fetches cryptocurrency data from the CoinCap API, performs some transformations, and imports it into a PostgreSQL database.

### Prerequisites
- PostgreSQL database server
- Database and user credentials

### Configuration
Update the `db_params` dictionary in the script with your PostgreSQL connection details:

db_params = {
 "host": "localhost",
 "database": "your_database_name",
 "user": "your_username",
 "password": "your_password"
}

### Usage
- Ensure you have the required libraries installed and PostgreSQL set up.
- Run the script: python crypto_to_postgres.py

### Features

- **Fetches real-time cryptocurrency data**.
- **Performs ETL operations**:
  - Extracts relevant fields.
  - Transforms data (adds a 'performance' metric).
  - Loads data into PostgreSQL.
  - Uses UPSERT operation to handle existing records.
- **Includes error handling** for API requests and database operations.

### Data Fields

Both scripts handle the following data fields:
- `id`
- `name`
- `symbol`
- `price`
- `price_change`

The PostgreSQL script additionally calculates and stores:
- `performance` (based on price change).

### Error Handling

- Both scripts include error handling for API requests.
- The PostgreSQL script also includes error handling for database operations.

### Maintenance

- Regularly check the CoinCap API documentation for any changes to the endpoint or data structure.
- For the PostgreSQL script, ensure your database is properly maintained and backed up.
