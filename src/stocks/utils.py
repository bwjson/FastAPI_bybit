from bs4 import BeautifulSoup
import requests

def get_ticker_value(ticker):
	ticker = ticker.upper()

	url = f'https://kase.kz/ru/shares/show/{ticker}/'

	page = requests.get(url)

	soup = BeautifulSoup(page.text, "html.parser")

	value = soup.find('div', class_='h1-block__indicator').text

	return value

rez = get_ticker_value('hsbk')
print(rez)