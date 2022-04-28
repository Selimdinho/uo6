import sqlite3
import os
import requests
from portfolio import companies

connection = sqlite3.connect("Stocks.db")
cursor = connection.cursor()

for i in companies:
    print(f"i Is = {i}")
    # i represents Company name e,g APLE, TSLA etc

    parameters = {
        "function": "TIME_SERIES_DAILY",  # This will return daily stock information from API
        "symbol": i,  # Company name
        "apikey": "7DOUC7QNT9IAFUR6"
    }

    #  API url endpoint
    url = 'https://www.alphavantage.co/query'

    r = requests.get(url, params=parameters)

    response = r.json()

    data = response['Time Series (Daily)']

    # Create Tables in Database from Dictionary. Table will have 6 columns
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {i} (
    time_stamp text primary key not null on conflict ignore,
    open integer,
    low  integer,
    high integer,
    close integer,
    volume integer,
    UNIQUE (time_stamp) ON CONFLICT IGNORE
    )
     """)
    connection.commit()
    print(f"Successfully Created {i} table")

    # Insert Data into table i
    for d in data:
        opened = data[d]['1. open']
        high = data[d]['2. high']
        close = data[d]['4. close']
        low = data[d]['3. low']
        volume = data[d]['5. volume']

        cursor.execute(f"INSERT INTO {i} VALUES (?, ?, ?, ?, ?, ?)",
                       (d, opened, high, close, low, volume))
        connection.commit()
    print(f"Successfully Entered data into table {i}")

# Uncomment the below code to check which tables are created. It will print list of table names in console
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# print(cursor.fetchall())
