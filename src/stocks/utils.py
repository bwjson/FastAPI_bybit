from bs4 import BeautifulSoup
import requests

def is_valid_ticker(ticker):
	ticker = ticker.upper().strip()
	url = f'https://kase.kz/ru/shares/show/{ticker}/'

	try:
		page = requests.get(url)
		page.raise_for_status()
	except:
		return False
	return True
		
		
def get_ticker_value(ticker):
	ticker = ticker.upper().strip()
	url = f'https://kase.kz/ru/shares/show/{ticker}/'

	try:
		page = requests.get(url, timeout=10)
		page.raise_for_status()  
	except Exception as e:
		return {
			"status": "failed",
			"error": f"An error occurred: {e}"
		}

	try:
		soup = BeautifulSoup(page.text, "html.parser")
		value_element = soup.find('div', class_='h1-block__indicator')
		
		if value_element:
			value = value_element.text.strip()
			return {
				"status": "success",
				"ticker": ticker,
				"value": value
			}
		else:
			return {
				"status": "failed",
				"error": f"Could not find the ticker value for {ticker}."
			}
	except Exception as e:
		return {
			"status": "failed",
			"error": f"Failed to parse the page: {e}"
		}
	
