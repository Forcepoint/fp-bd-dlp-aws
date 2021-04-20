import base64
import os
from cryptography.fernet import Fernet


def encrypt_password(pass_phrase):
    key = base64.urlsafe_b64encode(os.urandom(32))
    string_key = key.decode("utf-8")
    cipher_suite = Fernet(string_key)
    ciphered_text = cipher_suite.encrypt(str.encode(pass_phrase))
    '''f = open("password.txt", "w")
    f.write(ciphered_text.decode("utf-8"))
    f.close()'''
    return string_key, ciphered_text.decode("utf-8")


def get_encrypted_password():
    f = open("password.txt", "r")
    return f.read()


def decrypt_password(key, encypted_pass_phrase):
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(str.encode(encypted_pass_phrase))


'''if get_encrypted_password():
    pass_phrase = get_encrypted_password()
    key = input("Please enter your key:\n")
    print((decrypt_password(key, pass_phrase)).decode("utf-8"))
else:
    pass_phrase = input("Please enter your pass phrase:\n")
    key = save_encrypted_password(pass_phrase)
    print(f'Please save this key somewhere safe if you need to log in again : {key}')'''


