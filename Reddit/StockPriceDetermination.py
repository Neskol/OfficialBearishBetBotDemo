# The json_list contains dictionaries with the following keys:
# "code"
# "name"
# "industry"
# "sector"

import yfinance as yf
import datetime

def add_price_change(json_list):
    for entry in json_list:
        # Convert the Unix timestamp to a datetime object
        date = datetime.datetime.utcfromtimestamp(entry['time-stamp'])

        # Define start and end dates for yf.download function
        start_date = date.strftime('%Y-%m-%d')
        end_date = (date + datetime.timedelta(days=7)).strftime('%Y-%m-%d')

        data = yf.download(entry['code'], start=start_date, end=end_date)
        if data.empty:
            price_change = "No data presented"
        else:
            price_change = data['Close'].iloc[-1] - data['Open'].iloc[0]

        # Add the price_change to the dictionary
        entry["price_change"] = price_change

    return json_list
