from bs4 import BeautifulSoup
import requests


class KaseAPIClient():
	@staticmethod
	def is_valid_ticker(ticker: str):
		ticker = ticker.upper().strip()
		url = f'https://kase.kz/ru/shares/show/{ticker}/'

		try:
			page = requests.get(url)
			page.raise_for_status()
		except:
			return False
		return True

	@staticmethod	
	def get_ticker_value(ticker):
		ticker = ticker.upper().strip()
		url = f'https://kase.kz/ru/shares/show/{ticker}/'

		try:
			page = requests.get(url, timeout=10)
			page.raise_for_status()  
		except Exception as e:
			return None

		try:
			soup = BeautifulSoup(page.text, "html.parser")
			value_element = soup.find('div', class_='h1-block__indicator')
			
			if not value_element:
				return None
			
			raw_value = value_element.text.strip()
			cleaned_value = raw_value.replace(' ', '')
			value = cleaned_value.replace(',', '.')
			return value
		except Exception as e:
			return None
	
