import yfinance as yf

from datetime import datetime, timedelta

# Calculate the start date as ten years ago from the current date
end_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=10*365)).strftime('%Y-%m-%d')

# Fetch historical data for the past ten years
data = yf.download("MSFT", start=start_date, end=end_date)

print(data)