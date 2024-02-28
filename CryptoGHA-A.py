import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import os
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from math import gcd
from random import randint,seed
import time
import pickle
import win32print
import win32ui
import win32con
import hashlib
programma_invia_a = "C:\\mega/cartella_a"
programma_riceve_a = "C:\\mega/cartella_b"


T = int(time.time())
seed(T)

# *******************************************************
# * Inserimento passwors
# *******************************************************


def hash_password(password):
    # Genera un salt casuale per aggiungere casualità all'hashing
    salt = os.urandom(32)

    # Combina la password con il salt e calcola l'hash
    hashed_password = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, 100000
    )

    # Combina il salt e l'hash in un unico valore da memorizzare nel database
    hashed_password_hex = salt.hex() + hashed_password.hex()

    return hashed_password_hex


def verify_password(input_password, stored_password):
    # Estrae il salt dal valore memorizzato
    salt = bytes.fromhex(stored_password[:64])

    # Calcola l'hash della password di input con lo stesso salt
    hashed_input_password = hashlib.pbkdf2_hmac(
        "sha256", input_password.encode("utf-8"), salt, 100000
    )

    # Confronta il salt e l'hash con il valore memorizzato
    return stored_password[64:] == hashed_input_password.hex()


def get_password_from_user():
    password = simpledialog.askstring("Password", "Inserisci la password:", show="*")
    return password


# Esempio di utilizzo
password = "Cla1Giu19"
hashed_password = hash_password(password)

# Verifica della password
input_password = get_password_from_user()

if verify_password(input_password, hashed_password):
    pass
else:
    messagebox.showerror("Errore", "La password inserita è errata.")
    quit()


# *******************************************************
# * Controllo porta USB
# *******************************************************


apri_dati = simpledialog.askstring("USB", "Inserisci la porta USB se diversa da D")
if apri_dati==None:
    quit()

if not apri_dati:
    apri_dati = "d"
usb_path = apri_dati + ":\\"

if os.path.exists(usb_path):
    try:
        storage_devices = os.listdir(usb_path)
    except FileNotFoundError:
        pass
else:
    messagebox.showwarning(
        "Attenzione", "Chiavetta USB non trovata nella lettera di unità " + apri_dati
    )
    quit()

# *******************************************************
# * Apre file semiprimi scelta tipo di codifica
# *******************************************************


def apri_file():
    global codice_selezionato, chiave, filename
    filename = filedialog.askopenfilename(
        title="Apri file",
        initialdir="c:\\semiprimi",  # Cartella iniziale predefinita
        # filetypes=(("Tutti i File", "*.*"),("File di testo", "*.txt")),
    )

    if filename == "":
        messagebox.showwarning("Attenzione", "Nessuna codifica selezionata" + apri_dati)

        return
    semipsel = filename.split("/")
    codice_selezionato = semipsel[2]
    l1.config(text=semipsel[2])
    chiave_usb = apri_dati + ":\\chiave_" + codice_selezionato
    if os.path.exists(chiave_usb):
        with open(chiave_usb, "r") as leggif:
            leggi1 = int(leggif.readline())
            leggi2 = int(leggif.readline())
            leggi3 = int(leggif.readline())
            chiave = leggi1**leggi2

    else:
        messagebox.showerror("Errore", "Dati su USB non trovati")
        return

# *******************************************************
# * serie di funzioni per codifica
# *******************************************************

def carica_semiprimo_random(nome_file):
    with open(nome_file, "r") as file:
        righe = file.readlines()
        codice_random = randint(0, len(righe) - 1)  # Genera un indice casuale
        n = righe[codice_random]
    return int(n.strip())


def generate_aes_key(prime_factor):
    hash_object = SHA256.new(data=str(prime_factor).encode())
    return hash_object.digest()


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


def encrypt_message(message, aes_key):
    cipher = AES.new(aes_key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    return ciphertext, cipher.nonce, tag


# *******************************************************
# * inizia estrazione semiprimo e codifica testo
# *******************************************************

def codifica_messaggio():
    message_to_encrypt = tw1.get("1.0", END)
    if message_to_encrypt == "" or len(message_to_encrypt) < 20:
        messagebox.showerror(
            "Attenzione:", "Messaggio inesistente o più corto di 20 caratteri"
        )
        return
    # Carica un semiprimo casuale dal file
    nome_file = filename
    semiprime = carica_semiprimo_random(nome_file)
    # Genera chiave AES utilizzando il fattore primo
    secret_key = factorize(semiprime)
    aes_key = generate_aes_key(secret_key)
    message_to_encrypt = message_to_encrypt.strip()
    ciphertext, nonce, tag = encrypt_message(message_to_encrypt, aes_key)
    memorizza_file = programma_invia_a + "/GHA_mess_" + codice_selezionato

    with open(memorizza_file, "wb") as file:
        pickle.dump((ciphertext, nonce, tag, str(semiprime)), file)
    messagebox.showinfo("Via Cloud:", "Messaggio creato con successo")


# *******************************************************
# * stampa messaggio su stampante di default
# *******************************************************

def stampa_messaggiotw2():
    testo = tw2.get("1.0", tk.END).strip()
    if testo == "":
        messagebox.showerror("Attenzione:", "Nessun testo Da stampare")
        return
    stampa(testo)


def stampa_messaggiotw1():
    testo = tw1.get("1.0", tk.END).strip()
    if testo == "":
        messagebox.showerror("Attenzione:", "Nessun testo Da stampare")
        return
    stampa(testo)


def stampa(testo):
    printer_name = win32print.GetDefaultPrinter()
    hprinter = win32print.OpenPrinter(printer_name)
    hdc = win32ui.CreateDC()
    hdc.CreatePrinterDC(printer_name)

    # Ottieni le dimensioni della pagina
    width = hdc.GetDeviceCaps(win32con.PHYSICALWIDTH)
    height = hdc.GetDeviceCaps(win32con.PHYSICALHEIGHT)

    # Calcola il numero massimo di caratteri per riga basato sulla larghezza della pagina
    max_chars_per_line = int(width / hdc.GetTextExtent("X")[0])

    # Dividi il testo in righe più corte
    lines = []
    line = ""
    for word in testo.split():
        if len(line) + len(word) + 1 <= max_chars_per_line:
            line += word + " "
        else:
            lines.append(line.strip())
            line = word + " "
    if line:
        lines.append(line.strip())

    hdc.StartDoc("Stampa")
    hdc.StartPage()

    # Stampare le righe di testo
    y = 100
    for line in lines:
        hdc.TextOut(100, y, line)
        y += hdc.GetTextExtent(line)[1]  # spazio per la prossima riga

    hdc.EndPage()
    hdc.EndDoc()
    hdc.DeleteDC()
    win32print.ClosePrinter(hprinter)
    if l2.cget('text')!='':
        separa=l2.cget('text').split('/')
        l2.config(text='')
        cancella = programma_riceve_a + "/GHA_mess_" + separa[1]
        if os.path.exists(cancella):
            os.remove(cancella)


# *******************************************************
# * funzioni di decodifica
# *******************************************************

def decrypt_message(ciphertext, aes_key, nonce, tag):
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext.decode()


def factorized(semiprime,chiave):
    a = semiprime % chiave
    b = semiprime - a
    for i in range(10):
        key = gcd(a, b)
        if key != 1:
            break
        a = a + chiave
        b = b - chiave
    return key


# *******************************************************
# * decodifica messaggio
# *******************************************************
def decodifica():

    filename = filedialog.askopenfilename(
        title="Apri file",
        initialdir=programma_riceve_a,  # Cartella iniziale predefinita
        # filetypes=(("Tutti i File", "*.*"),("File di testo", "*.txt")),
    )

    if filename == "":
        messagebox.showerror('Attenzione:','File non selezionato')
        return

    if "\\" in filename:
        # Se il percorso utilizza '\', usa split('\\')
        semipsel = filename.split("\\")
    else:
        # Altrimenti, usa split('/')
        semipsel = filename.split("/")

    files = semipsel[-1].split("_")
    codice_selezionato = files[2]
    chiave_usb = os.path.join(apri_dati + ":", "chiave_" + codice_selezionato)

    if os.path.exists(chiave_usb):
        with open(chiave_usb, "r") as leggif:
            leggi1 = int(leggif.readline())
            leggi2 = int(leggif.readline())
            leggi3 = int(leggif.readline())
            chiave = leggi1**leggi2
    else:
        messagebox.showerror("Errore", "Dati su USB non trovati")
        return

    l2.configure(text='GHA/'+codice_selezionato)
    path = programma_riceve_a + "/GHA_mess_" + codice_selezionato
    with open(path, "rb") as file:
        ciphertext, nonce, tag, semiprime = pickle.load(file)
    semiprime = int(semiprime)
    secret_key_received = factorized(semiprime, chiave)
    aes_key_received = generate_aes_key(secret_key_received)
    decrypted_message = decrypt_message(ciphertext, aes_key_received, nonce, tag)
    tw2.delete("1.0", END)
    tw2.insert("1.0", decrypted_message)


# *******************************************************
# * parte Grafica gestione pulsanti
# *******************************************************

def cancellatw1():
    tw1.delete("1.0", END)
    return

def cancellatw2():
    tw2.delete("1.0", END)
    return


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


def on_enter2(event):
    rb1.config(
        bg=passa_button
    )  # Cambia il colore di sfondo a blu quando il mouse entra nel pulsante


def on_leave2(event):
    rb1.config(bg=fondo_button)  # Ripristina il colore di sfondo


def on_enter3(event):
    rb2.config(
        bg=passa_button
    )  # Cambia il colore di sfondo a blu quando il mouse entra nel pulsante


def on_leave3(event):
    rb2.config(bg=fondo_button)  # Ripristina il colore di sfondo


# *************************************************
# *       dimensione e colori
# *************************************************
finestra_x = 945
finestra_y = 500
finestra = str(finestra_x) + "x" + str(finestra_y)
fondo_finestra = "#36648B"
fondo_text = "#808080"
fondo_button = "#20B2AA"
passa_button = "#C0FF3E"
fondo_button2 = "#71C671"
fondo_entry = "#C1C1C1"
# *************************************************
# *        Finestra principale
# *************************************************
root = tk.Tk()
root.title("Codifica Con Metodo GHA - PROGRAMMA A")
root.geometry(finestra)
root.config(bg=fondo_finestra)
# Creazione del canvas
px = finestra_x - 115
py = finestra_y - 115
canvas = tk.Canvas(root, width=130, height=130)
canvas.place(x=px, y=py)

# ****************************************************
# * Grafica invia
# ****************************************************

px = 10
py = 10
tw1 = tk.Text(
    root, width=50, height=17, bg=fondo_text, font="helvetica, 12", cursor="left_ptr"
)
tw1.place(x=px, y=py)

px = 100
py = 330

b1 = tk.Button(
    root,
    text="Stampa",
    bg=fondo_button,
    font="arial, 12 bold",
    width=10,
    cursor="hand2",
    command=stampa_messaggiotw1
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
    command=cancellatw1
)
b2.place(x=px, y=py)
b2.bind("<Enter>", on_enter1)
b2.bind("<Leave>", on_leave1)

px = 20
py = 330 + 70

b3 = tk.Button(
    root,
    text="Seleziona Codifica",
    bg=fondo_button2,
    font="arial, 12 bold",
    width=15,
    cursor="hand2",
    command=apri_file
)
b3.place(x=px, y=py)

py = py + 50

b4 = tk.Button(
    root,
    text="Codifica",
    bg=fondo_button2,
    font="arial, 12 bold",
    width=15,
    cursor="hand2",
    command=codifica_messaggio
)
b4.place(x=px, y=py)

px = px + 180
py=py-50

l1 = tk.Label(text='',width=10, bg=fondo_finestra, font="arial 12 bold")
l1.place(x=px, y=py)

# ****************************************************
# * Grafica riceve
# ****************************************************

px = 480
py = 10
tw2 = tk.Text(
    root, width=50, height=17, bg=fondo_text, font="helvetica, 12", cursor="left_ptr"
)
tw2.place(x=px, y=py)

px = px+100
py = 330

rb1 = tk.Button(
    root,
    text="Stampa",
    bg=fondo_button,
    font="arial, 12 bold",
    width=10,
    cursor="hand2",
    command=stampa_messaggiotw2
)
rb1.place(x=px, y=py)
rb1.bind("<Enter>", on_enter2)
rb1.bind("<Leave>", on_leave2)

px = px + 150
py = 330

rb2 = tk.Button(
    root,
    text="Cancella",
    bg=fondo_button,
    font="arial, 12 bold",
    width=10,
    cursor="hand2",
    command=cancellatw2,
)
rb2.place(x=px, y=py)
rb2.bind("<Enter>", on_enter3)
rb2.bind("<Leave>", on_leave3)

px = px-240
py = 330 + 70

b3 = tk.Button(
    root,
    text="Seleziona File",
    bg=fondo_button2,
    font="arial, 12 bold",
    width=15,
    cursor="hand2",
    command=decodifica
)
b3.place(x=px, y=py)

px = px + 160

l2 = tk.Label(text="", width=12, bg=fondo_finestra, font="arial 14 bold")
l2.place(x=px, y=py)


testo = "CODIFICA\nGHA"
colore = "blue"  # Colore del testo
fonte = ("arial", 10, "bold")
colore_sfondo = fondo_finestra  # Colore dello sfondo
canvas.config(bg=colore_sfondo)
canvas.create_text(65,20,text='GC57crypto',fill='red',font=fonte)
canvas.create_text(65, 50, text="A", fill="red", font='arial 20 bold')
canvas.create_text(65, 85, text=testo, fill=colore, font=fonte)

root.mainloop()
