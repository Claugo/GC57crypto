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
from tkinter import filedialog
import win32print
import win32ui
import win32con

apri_dati = simpledialog.askstring("USB", "Inserisci la porta USB se diversa da D")
if not apri_dati:
    apri_dati = "d"


# file_path = os.path.join(apri_dati)


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


def apri_file():
    global codice_selezionato, chiave, filename
    filename = filedialog.askopenfilename(
        title="Apri file",
        initialdir="F:\\DCP",  # Cartella iniziale predefinita
        # filetypes=(("Tutti i File", "*.*"),("File di testo", "*.txt")),
    )
    semipsel = filename.split("/")
    files=semipsel[2].split('_')
    codice_selezionato = files[2]
    chiave_usb = apri_dati + ":\\chiave_" + codice_selezionato

    if os.path.exists(chiave_usb):
        with open(chiave_usb, "r") as leggif:
            leggi1 = int(leggif.readline())
            leggi2 = int(leggif.readline())
            leggi3 = int(leggif.readline())
            chiave = leggi1**leggi2
            prewin.destroy()  # Chiude la finestra tkinter dopo aver selezionato il file

    else:
        messagebox.showerror("Errore", "Dati su USB non trovati")
        prewin.destroy()  # Chiude la finestra tkinter dopo aver selezionato il file
        quit()

def on_exit():
   prewin.destroy()
   quit()

prewin = tk.Tk()
larghezza = prewin.winfo_screenwidth()
altezza = prewin.winfo_screenheight()
prewin.title("Seleziona il File Da Decriptare")
prewin.configure(bg="orange")
prewin.geometry(f"{'300'}x{'100'}+{larghezza//2}+{altezza//3}")

label = tk.Label(
    prewin, text="Seleziona File per la Decodifica", bg="orange", font="arial 12 bold"
)
label.pack(pady=10)

select_button = tk.Button(prewin, width=10, text="APRI", bg="green", command=apri_file)
select_button.pack(pady=5)
prewin.protocol("WM_DELETE_WINDOW", on_exit)
prewin.mainloop()


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
    
    path = "F:\\DCP/send_mess_"+codice_selezionato
    with open(path, "rb") as file:
        ciphertext, nonce, tag, semiprime = pickle.load(file)
    semiprime = int(semiprime)
    secret_key_received = factorize(semiprime, chiave)
    aes_key_received = generate_aes_key(secret_key_received)
    decrypted_message = decrypt_message(ciphertext, aes_key_received, nonce, tag)
    tw1.delete("1.0", END)
    tw1.insert("1.0", decrypted_message)


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


def stampa_messaggio():
    testo = tw1.get(
        "1.0", tk.END
    ).strip()
    if testo=='':
        messagebox.showerror('Attenzione:','Nessun testo Da stampare')
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
    if os.path.exists(filename):
        os.remove(filename)


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
root.geometry(finestra+'+1000+50')
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
    command=stampa_messaggio,
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
    state="disabled",
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
e2 = tk.Entry(root, width=25, font="arial, 12", bg=fondo_entry, justify="center")
e2.insert(0, filename)
e2.place(x=px, y=py)

py = py + -50
e3 = tk.Entry(root, width=20, font="arial, 14", bg=fondo_entry, justify="center")
e3.insert(0, "Non Disponibile")
e3.place(x=px, y=py)


# Carica l'immagine automaticamente quando la finestra si apre
carica_immagine()

root.mainloop()
