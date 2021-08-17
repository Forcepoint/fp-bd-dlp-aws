import constant
from Cryptodome.Cipher import AES


def encrypt_phrase(phrase):
    cipher = AES.new(constant.AES, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(str(phrase).encode("utf-8"))
    file_out = open("./DLPExporter.bin", "wb")
    [file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]
    file_out.close()


def decrypt_password():
    file_in = open("./DLPExporter.bin", "rb")
    nonce, tag, ciphertext = [file_in.read(x) for x in (16, 16, -1)]
    cipher = AES.new(constant.AES, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    return data.decode()

