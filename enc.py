import json
import base64
from cryptography.fernet import Fernet
from os import environ as env







def encrypt (data):
    key = env.get('app_secret')
    fernet = Fernet(key.encode("utf8"))
    user_encode_data = json.dumps(data).encode()

    encoded = fernet.encrypt(user_encode_data)





    return encoded

def decrypt(enc_message):
    key = env.get('app_secret')
    fernet = Fernet(key.encode("utf8"))
    dec_message = fernet.decrypt(enc_message).decode()
    return dec_message


def create_key():

    key = Fernet.generate_key().decode()
    return

if __name__ == "__main__":
    enc = encrypt(service_key)
    print(enc.decode())
    dec = decrypt(enc.decode())
    print(dec)




