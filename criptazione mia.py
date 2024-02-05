# con nonce e tag
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from math import gcd
from random import randint
import os
from tkinter import messagebox
import pickle


chiave = 6366805760909027985741435139224233**58

def carica_semiprimo_random(nome_file):
    with open(nome_file, "r") as file:
        righe = file.readlines()
        codice_random = randint(0, len(righe) - 1)  # Genera un indice casuale
        n = righe[codice_random]
    return int(n.strip())


def factorize(semiprime):
    a = semiprime % chiave
    b = semiprime - a
    for i in range(10):
        key = gcd(a, b)
        if key != 1:
            break
        a = a + chiave
        b = b - chiave
    return key


def generate_aes_key(prime_factor):
    hash_object = SHA256.new(data=str(prime_factor).encode())
    return hash_object.digest()


def encrypt_message(message, aes_key):
    cipher = AES.new(aes_key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    return ciphertext, cipher.nonce, tag


# Carica un semiprimo casuale dal file
nome_file = "13000b"
semiprime = carica_semiprimo_random(nome_file)

# Genera chiave AES utilizzando il fattore primo
secret_key = factorize(semiprime)
aes_key = generate_aes_key(secret_key)

# Messaggio da cifrare
apri = open("C:\\Users\\Claugo\\OneDrive\\Desktop\\fernet.txt", "r", encoding="utf-8")
message_to_encrypt = apri.read()
apri.close()
message_to_encrypt = message_to_encrypt.strip()
# message_to_encrypt = "Il mio messaggio segreto da cifrare"

# Cifrare il messaggio
ciphertext, nonce, tag = encrypt_message(message_to_encrypt, aes_key)

# Creare una struttura dati contenente il messaggio cifrato, il semiprimo utilizzato, il nonce e il tag
data_to_send = {
    "ciphertext": ciphertext,
    "semiprime": semiprime,
    "nonce": nonce,
    "tag": tag,
}
with open("send_mess", "wb") as file:
    pickle.dump((ciphertext, nonce, tag, str(semiprime)), file)


# ***************************************************************


chiave = 6366805760909027985741435139224233**58


def factorize(semiprime, chiave):
    a = semiprime % chiave
    b = semiprime - a
    for i in range(10):
        key = gcd(a, b)
        if key != 1:
            break
        a = a + chiave
        b = b - chiave
    return key


path = "send_mess"
if os.path.exists(path):
    with open("send_mess", "rb") as file:
        ciphertext, nonce, tag, semiprime = pickle.load(file)

    # Stampa i dati letti
    semiprime=int(semiprime)


def decrypt_message(ciphertext, aes_key, nonce, tag):
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext.decode()


# Stampa la struttura dati contenente tutte le informazioni
# print("Dati da inviare:", data_to_send)
secret_key_received = factorize(semiprime, chiave)

# Genera chiave AES utilizzando il semiprimo ricevuto
aes_key_received = generate_aes_key(secret_key_received)

# Decifrare il messaggio
decrypted_message = decrypt_message(ciphertext, aes_key_received, nonce, tag)

# Stampa il messaggio decifrato
print("Messaggio decifrato:", decrypted_message)
