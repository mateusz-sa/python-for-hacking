import base64


def encrypt_pass(password):
    encoded_bytes = base64.b64encode(password.encode())
    #print(encoded_bytes)
    return encoded_bytes


user_password = input("Enter your password: ")

print(encrypt_pass(user_password))