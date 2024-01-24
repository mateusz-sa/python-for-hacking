import base64


def encode_pass(password):
    encoded_bytes = base64.b64encode(password.encode())
    return encoded_bytes

def decode_pass(encoded_password):
    decoded_password = base64.b64decode(encoded_password)
    return decoded_password

user_password = input("Enter your password: ")
encoded_pass = encode_pass(user_password)

print(encoded_pass)
print(decode_pass(encoded_pass))
