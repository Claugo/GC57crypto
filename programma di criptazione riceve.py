# Decodifica Messaggio Criptati
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import os
from tkinter import messagebox
from tkinter import simpledialog
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from math import gcd
from random import randint
import pickle

# Modes: system (default), light, dark

apri_dati = simpledialog.askstring("USB", "Inserisci la porta USB se diversa da D")
if not apri_dati:
    apri_dati = "d"


file_path = os.path.join(apri_dati + ":", "chiave")

try:
    with open(file_path, "r") as leggif:
        leggi1 = int(leggif.readline())
        leggi2 = int(leggif.readline())
        leggi3 = int(leggif.readline())
        chiave=leggi1**leggi2
except FileNotFoundError:
    messagebox.showerror("Errore", "Dati su USB non trovati")
    quit()


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


def generate_aes_key(prime_factor):
    hash_object = SHA256.new(data=str(prime_factor).encode())
    return hash_object.digest()



    # Stampa i dati letti


def decrypt_message(ciphertext, aes_key, nonce, tag):
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext.decode()


def decodifica():
    path = "F:\\DCP/send_mess_13000b"
    if os.path.exists(path):
        with open(path, "rb") as file:
            ciphertext, nonce, tag, semiprime = pickle.load(file)
        semiprime = int(semiprime)
        secret_key_received = factorize(semiprime, chiave)
        aes_key_received = generate_aes_key(secret_key_received)
        decrypted_message = decrypt_message(ciphertext, aes_key_received, nonce, tag)
        tw1.delete('1.0',END)
        tw1.insert('1.0',decrypted_message)
    else:
        messagebox.showerror('Attenzione','File Non Trovato')


def carica_immagine():
    # Apri un'immagine utilizzando PIL
    img = Image.open("logo.jpg")

    # Converte l'immagine in un formato compatibile con Tkinter
    img_tk = ImageTk.PhotoImage(img)

    # Aggiungi l'immagine al canvas
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

    # Memorizza un riferimento all'immagine per evitare che venga eliminata dalla Garbage Collection
    canvas.image = img_tk


def on_enter(event):
    b1.config(
        bg=passa_button
    )  # Cambia il colore di sfondo a blu quando il mouse entra nel pulsante


def on_leave(event):
    b1.config(bg=fondo_button)  # Ripristina il colore di sfondo


def on_enter1(event):
    b2.config(
        bg=passa_button
    )  # Cambia il colore di sfondo a blu quando il mouse entra nel pulsante


def on_leave1(event):
    b2.config(bg=fondo_button)  # Ripristina il colore di sfondo


def cancella():
    tw1.delete("1.0", END)
    return


# *************************************************
# *       dimensione e colori
# *************************************************
finestra_x = 600
finestra_y = 500
finestra = str(finestra_x) + "x" + str(finestra_y)
fondo_finestra = "#6E8B3D"
fondo_text = "#808080"
fondo_button = "#20B2AA"
passa_button = "#C0FF3E"
fondo_button2 = "#71C671"
fondo_entry = "#C1C1C1"
# *************************************************
# *        Finestra principale
# *************************************************
root = tk.Tk()
root.title("Decodifica Documento Criptato  DDC")
root.geometry(finestra)
root.config(bg=fondo_finestra)
# Creazione del canvas
px = finestra_x - 130
py = finestra_y - 130
canvas = tk.Canvas(root, width=130, height=130)
canvas.place(x=px, y=py)
px = 10
py = 10
tw1 = tk.Text(
    root, width=64, height=17, bg=fondo_text, font="helvetica, 12", cursor="left_ptr"
)
tw1.place(x=px, y=py)

px = 150
py = 330

b1 = tk.Button(
    root,
    text="Stampa",
    bg=fondo_button,
    font="arial, 12 bold",
    width=10,
    cursor="hand2",
)
b1.place(x=px, y=py)
b1.bind("<Enter>", on_enter)
b1.bind("<Leave>", on_leave)

px = px + 150
py = 330

b2 = tk.Button(
    root,
    text="Cancella",
    bg=fondo_button,
    font="arial, 12 bold",
    width=10,
    cursor="hand2",
    command=cancella,
)
b2.place(x=px, y=py)
b2.bind("<Enter>", on_enter1)
b2.bind("<Leave>", on_leave1)

px = 20
py = 330 + 70

b3 = tk.Button(
    root,
    text="Decodifica da E-mail",
    bg=fondo_button2,
    font="arial, 12 bold",
    width=17,
    cursor="hand2",
    state='disabled'
)
b3.place(x=px, y=py)

py = py + 50

b4 = tk.Button(
    root,
    text="Decodifica da Cloud",
    bg=fondo_button2,
    font="arial, 12 bold",
    width=17,
    cursor="hand2",
    command=decodifica,
)
b4.place(x=px, y=py)

py = py + 3
px = px + 190
e2 = tk.Entry(root, width=20, font="arial, 14", bg=fondo_entry,justify='center')
e2.insert(0,'Cartella Cloud su PC')
e2.place(x=px, y=py)

py = py + -50
e3 = tk.Entry(root, width=20, font="arial, 14", bg=fondo_entry,justify='center')
e3.insert(0,'Non Disponibile')
e3.place(x=px, y=py)

# Carica l'immagine automaticamente quando la finestra si apre
carica_immagine()

root.mainloop()
