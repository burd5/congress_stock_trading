import pandas as pd 

# current_leg = pd.read_csv('/Users/austinburdette/Downloads/legislators-current.csv', index_col=False)
# current_leg = current_leg[['full_name', 'type', 'state', 'district', 'party']]
# # current_leg['full_name'] = current_leg['first_name'] + ' ' + current_leg['last_name']
# current_leg['district'] = current_leg['district'].astype('Int64', errors='ignore')
# current_leg['marker'] = current_leg['state'] + current_leg['district'].astype('str')

# for k, v in current_leg['marker'].items():
#     if '<NA>' in v:
#         v = v.split('<')[0]
#     if '0' in v:
#         v = v.split('0')[0]
#     if '-' in v:
#         v = v.split('-')[0]
#     current_leg['marker'][k] = v

# current_leg = current_leg.replace('sen', 'Senate', regex=True)
# current_leg = current_leg.replace('rep', 'House', regex=True)

# current_leg = current_leg[['full_name', 'type', 'state', 'party', 'marker']]

# current_leg.to_csv('data/migrations/current_leg.csv', index=False)

nasdaq_stocks = pd.read_csv('/Users/austinburdette/Downloads/nasdaq_stocks.csv', usecols=['Symbol', 'Name'], encoding='utf-8')
nasdaq_stocks.to_csv('data/migrations/nasdaq_stocks.csv', index=False)

otc_stocks =  pd.read_csv('/Users/austinburdette/Downloads/otc_stocks.csv', sep=';', names=['Symbol', 'Name', 'Equity', 'USD'])
otc_stocks = otc_stocks[['Symbol', 'Name']]
otc_stocks.to_csv('data/migrations/otc.csv', index=False)

nasdaq = pd.read_csv('data/migrations/nasdaq_stocks.csv', index_col=False)
nyse = pd.read_csv('data/migrations/nyse_converted.csv', index_col=False)
otc = pd.read_csv('data/migrations/otc.csv', index_col=False)

combined_stocks = pd.concat([nasdaq, nyse])
unique_stocks1 = combined_stocks.drop_duplicates(subset=['Symbol'], keep='last')
combined_stocks2 = pd.concat([unique_stocks1, otc])
unique_stocks2 = combined_stocks2.drop_duplicates(subset=['Symbol'], keep='last')
unique_stocks2.to_csv('data/migrations/combined_stocks.csv', index=False)
