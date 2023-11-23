import requests
""" Utilizat pentru a trimite solicitari catre servere web """

import webbrowser
""" Deschidem URL-ul intr-un browser """
from bs4 import BeautifulSoup
""" Extrage informatii din documente de tip HTML si XML """

url = input("Introduceți link-ul: ")

try:
    # Se face un request catre acel URL
    response = requests.get(url)
    # Verificam statusul cererii, 200 insemnand ca cererea a fost reusita
    if response.status_code == 200:
        # Accesam URL-ul
        webbrowser.open(url)
        # Accesam informatiile de la adresa respectiva si extragem 'description_meta'
        soup = BeautifulSoup(response.text, features="html.parser")
        metas = soup.find_all('meta')
        for m in metas:
            if m.get('name') == 'description':
                desc = m.get('content')
                print(desc)
    else:
        print("Eroare la solicitarea paginii:", response.status_code)
except Exception as e:
    """ Gestionarea erorilor ce pot aparea in timpul rularii """
    print("Eroare:", str(e))

