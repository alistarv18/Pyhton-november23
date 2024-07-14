import requests
import configparser
from bs4 import BeautifulSoup
import time

def get_olx_prices(keyword, log=False, pret_min=1000):
    # Construct the URL for searching the keyword on OLX
    url = f'https://www.olx.ro/oferte/q-{keyword}/'

    try:
        # Record the start time of the request
        start_time = time.time()

        # Make the HTTP request to the OLX website
        response = requests.get(url)

        # Record the end time of the request
        end_time = time.time()

        # Check if the response status is OK
        if response.status_code == 200:
            # Parse the HTML content of the response
            soup = BeautifulSoup(response.text, 'html.parser')
            prices = []

            # Find all elements with the class 'pret' (price)
            price_elements = soup.find_all('span', class_='pret')

            # Extract the text (price) from each element and add it to the list
            for price_element in price_elements:
                price = price_element.get_text()
                prices.append(price)

            # Sort the prices
            prices.sort()

            # If logging is enabled, print the time taken for the request
            if log:
                print(f"Timpul necesar request-ului către OLX: {end_time - start_time} secunde")

            # Check if there are any prices found
            if prices:
                # Find the minimum price and compare it with the threshold
                min_price = float(min(prices))
                if min_price < pret_min:
                    print(f"Prețul minim ({min_price}) a scăzut sub valoarea minimă permisă ({pret_min})!")

                return prices
            else:
                # No prices were found on the page
                print("Nu s-au găsit prețuri pe pagina OLX.")
                return None
        else:
            # There was an error with the HTTP request
            print(f"Eroare la solicitarea paginii OLX: {response.status_code}")
            return None
    except Exception as e:
        # Handle any other exceptions that occur
        print(f"Eroare: {str(e)}")
        return None

# Read the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# If 'Settings' section does not exist, create it
if 'Settings' not in config:
    config['Settings'] = {}

# Check if 'keyword' is set in the configuration
if 'keyword' not in config['Settings']:
    # If not, prompt the user to input the keyword and save it to the configuration
    keyword = input("Introduceți cuvântul cheie pentru căutare pe OLX: ")
    config['Settings']['keyword'] = keyword
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
else:
    # If it exists, read the keyword from the configuration
    keyword = config['Settings']['keyword']

# Check if logging is enabled in the configuration
if '-log' in config['Settings']:
    log_enabled = config['Settings']['-log'].lower() == 'true'
else:
    log_enabled = False

# Check if the minimum price threshold is set in the configuration
if 'min_price_threshold' in config['Settings']:
    min_price_threshold = float(config['Settings']['min_price_threshold'])
else:
    min_price_threshold = 1000  # Default value

# Call the function to get the prices from OLX
prices = get_olx_prices(keyword, log=log_enabled, pret_min=min_price_threshold)

# If prices were found, print them in ascending order
if prices:
    print(f"Preturile pentru '{keyword}' pe OLX în ordine crescătoare sunt:")
    for price in prices:
        print(price)
