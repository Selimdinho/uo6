import requests
# search company name
term = 'shopify'  # use first name of company or first few letters

#  Do not change below code
url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={term}&apikey=7DOUC7QNT9IAFUR6'
r = requests.get(url)
data = r.json()

print(data)