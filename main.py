import requests
import configparser
from bs4 import BeautifulSoup
import time


def get_olx_prices(keyword, log=False, pret_min=1000):
    url = f'https://www.olx.ro/oferte/q-{keyword}/'

    try:
        start_time = time.time()

        response = requests.get(url)

        end_time = time.time()

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            prices = []

            price_elements = soup.find_all('span', class_='pret')

            for price_element in price_elements:
                price = price_element.get_text()
                prices.append(price)

            prices.sort()

            if log:
                print(f"Timpul necesar request-ului către OLX: {end_time - start_time} secunde")

            # Verificăm dacă există prețuri înainte de a încerca să găsim prețul minim
            if prices:
                # Adăugăm verificarea pentru valoarea minimă a prețului
                min_price = float(min(prices))
                if min_price < pret_min:
                    print(f"Prețul minim ({min_price}) a scăzut sub valoarea minimă permisă ({pret_min})!")

                return prices
            else:
                print("Nu s-au găsit prețuri pe pagina OLX.")
                return None
        else:
            print(f"Eroare la solicitarea paginii OLX: {response.status_code}")
            return None
    except Exception as e:
        print(f"Eroare: {str(e)}")
        return None


config = configparser.ConfigParser()
config.read('config.ini')

if 'Settings' not in config:
    config['Settings'] = {}

if 'keyword' not in config['Settings']:
    keyword = input("Introduceți cuvântul cheie pentru căutare pe OLX: ")
    config['Settings']['keyword'] = keyword
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
else:
    keyword = config['Settings']['keyword']

if '-log' in config['Settings']:
    log_enabled = config['Settings']['-log'].lower() == 'true'
else:
    log_enabled = False

if 'min_price_threshold' in config['Settings']:
    min_price_threshold = float(config['Settings']['min_price_threshold'])
else:
    min_price_threshold = 1000  # Valoarea implicită

prices = get_olx_prices(keyword, log=log_enabled, pret_min=min_price_threshold)

if prices:
    print(f"Preturile pentru '{keyword}' pe OLX în ordine crescătoare sunt:")
    for price in prices:
        print(price)
