import json
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# Dane do szyfrowania
client_options = {
    "crypt": {
        "cypher": "AES-256-CBC",
        "key": "MySuperSecretKeyForParamsToken12"
    }
}

# Funkcja do szyfrowania
def encrypt(value):
    iv = get_random_bytes(16)
    cipher = AES.new(client_options['crypt']['key'].encode('utf-8'), AES.MODE_CBC, iv)
    ct_bytes = cipher.encrypt(pad(json.dumps(value).encode('utf-8'), AES.block_size))
    iv_base64 = base64.b64encode(iv).decode('utf-8')
    ct_base64 = base64.b64encode(ct_bytes).decode('utf-8')
    return json.dumps({"iv": iv_base64, "value": ct_base64})

# Funkcja do deszyfrowania
def decrypt(encrypted_token):
    encrypted_token = json.loads(encrypted_token)
    iv = base64.b64decode(encrypted_token['iv'])
    ct = base64.b64decode(encrypted_token['value'])
    cipher = AES.new(client_options['crypt']['key'].encode('utf-8'), AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return json.loads(pt.decode('utf-8'))

# Przykładowe użycie
token = {
    "username": "admin",
    "role": "admin",
    "expiration": "2024-12-31"
}

# Zakodowanie tokenu
encrypted_token = encrypt(token)
print("Encrypted Token:", encrypted_token)

# Odkodowanie tokenu
decoded_token = decrypt(encrypted_token)
print("Decoded Token:", decoded_token)
