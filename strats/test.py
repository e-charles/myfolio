import yfinance as yf 
import pprint

res = yf.Ticker('OKLO').info

# pprint.pprint(res)

# need business summary 
pprint.pprint(res['longBusinessSummary'])
print('======================')
# need officers 
pprint.pprint(res['companyOfficers'])