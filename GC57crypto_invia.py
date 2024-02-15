# Invio Messaggi Criptati
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
from random import randint
import pickle
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
    global codice_selezionato,chiave,filename
    filename = filedialog.askopenfilename(
        title="Apri file",
        initialdir="c:\\semiprimi",  # Cartella iniziale predefinita
        # filetypes=(("Tutti i File", "*.*"),("File di testo", "*.txt")),
    )
    if filename=='':
        prewin.destroy()
        quit()

    semipsel = filename.split("/")
    codice_selezionato = semipsel[2]
    chiave_usb=apri_dati+':\\chiave_'+codice_selezionato

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
prewin.title("Seleziona BIT di Codifica")
prewin.configure(bg="yellow")
prewin.geometry(f"{'300'}x{'100'}+{larghezza//2}+{altezza//3}")

label = tk.Label(
    prewin, text="Seleziona BIT di Codifica", bg="yellow", font="arial 12 bold"
)
label.pack(pady=10)

select_button = tk.Button(prewin, width=10, text="APRI", bg="green", command=apri_file)
select_button.pack(pady=5)
prewin.protocol("WM_DELETE_WINDOW", on_exit)

prewin.mainloop()


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


def elaborazione_email():
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
    memorizza_file='send_mess_'+codice_selezionato
    with open(memorizza_file, "wb") as file:
        pickle.dump((ciphertext, nonce, tag, str(semiprime)), file)
    messagebox.showinfo("Via E-mail:", "Messaggio creato con successo")


def elaborazione_cloud():
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
    memorizza_file = "F:\\DCP/send_mess_" + codice_selezionato

    with open(memorizza_file, "wb") as file:
        pickle.dump((ciphertext, nonce, tag, str(semiprime)), file)
    messagebox.showinfo("Via Cloud:", "Messaggio creato con successo")


def carica_immagine():
    try:
        # Apri un'immagine utilizzando PIL
        img = Image.open("logo.jpg")

        # Converte l'immagine in un formato compatibile con Tkinter
        img_tk = ImageTk.PhotoImage(img)

        # Aggiungi l'immagine al canvas
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

        # Memorizza un riferimento all'immagine per evitare che venga eliminata dalla Garbage Collection
        canvas.image = img_tk
    except FileNotFoundError:
        pass


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


# *************************************************
# *       dimensione e colori
# *************************************************
finestra_x = 600
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
root.title("Invio Documenti Criptati   IDC")
root.geometry(finestra+'+200+50')
root.config(bg=fondo_finestra)
# Creazione del canvas
px = finestra_x - 130
py = finestra_y - 130
canvas = tk.Canvas(root, width=130, height=130)
canvas.place(x=px, y=py)
px = 10
py = 10
tw1 = tk.Text(
    root,
    wrap=WORD,
    width=64,
    height=17,
    bg=fondo_text,
    font="helvetica, 12",
    cursor="left_ptr",
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
    command=stampa_messaggio
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
    text="Invia Per E-mail",
    bg=fondo_button2,
    font="arial, 12 bold",
    width=13,
    cursor="hand2",
    command=elaborazione_email,
    state="disabled",
)
b3.place(x=px, y=py)

py = py + 50

b4 = tk.Button(
    root,
    text="Invia Con Cloud",
    bg=fondo_button2,
    font="arial, 12 bold",
    width=13,
    cursor="hand2",
    command=elaborazione_cloud,
)
b4.place(x=px, y=py)

py = py + 3
px = px + 150
e2 = tk.Entry(root, width=20, font="arial, 14", bg=fondo_entry, justify="center")
e2.insert(0, "Cartella cloud su PC")
e2.place(x=px, y=py)

py = py + -50
e3 = tk.Entry(root, width=20, font="arial, 14", bg=fondo_entry, justify="center")
e3.insert(0, "Non Disponibile")
e3.place(x=px, y=py)

# Carica l'immagine automaticamente quando la finestra si apre
carica_immagine()

root.mainloop()
