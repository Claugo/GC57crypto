import tkinter as tk
#from tkinter import *
from PIL import Image, ImageTk
from tkinter import simpledialog
from tkinter import filedialog
import os
from tkinter import messagebox
import pickle
from random import randint, seed
import time
from math import gcd
import hashlib
import win32print
import win32ui
import win32con

filename=''
programma_invia_a = "c:\\mega/cartella_a"
programma_riceve_a = "c:\\mega/cartella_b"


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
password = "12345"
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
if apri_dati == None:
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
# * decripta file ricevuto
# *******************************************************
def decripta(lista_m,lista_testo,p):

    start1 = str(p)
    start2 = len(start1)
    start = int(start1[start2 - 5] + start1[start2 - 4])

    ln = list(str(p))
    if len(ln) % 2 == 0:
        pass
    else:
        ln.append("0")
    divln = []

    for i in range(0, len(ln), 2):
        c1 = int(ln[i])
        c2 = int(ln[i + 1])
        c3 = c1 * 10 + c2
        divln.append(c3)
    # **********************************************
    m1 = int(lista_m[0])
    m2 = int(lista_m[1])
    m3 = int(lista_m[2])
    m4 = int(lista_m[3])
    m5 = int(lista_m[4])
    # **********************************************

    cont = start
    tdecript = ""
    for i in range(len(lista_testo)):
        if cont == len(divln):
            cont = 0
        x = int(divln[cont])
        if x >= 0 and x < 25:
            y = int(lista_testo[i])
            tdecript = tdecript + (chr(y - x - m1))
        if x >= 25 and x < 40:
            y = int(lista_testo[i])
            tdecript = tdecript + (chr(y - x - m2))
        if x >= 40 and x < 50:
            y = int(lista_testo[i])
            tdecript = tdecript + (chr(y - x - m3))
        if x >= 50 and x < 75:
            y = int(lista_testo[i])
            tdecript = tdecript + (chr(y - x - m4))
        if x >= 75 and x < 100:
            y = int(lista_testo[i])
            tdecript = tdecript + (chr(y - x - m5))
        cont = cont + 1
    return tdecript


# *******************************************************
# * apri file ricevuto
# *******************************************************
def apri_filer():
    global codice_selezionato, chiave, filename
    filename = filedialog.askopenfilename(
        title="Apri file",
        initialdir=programma_riceve_a,  # Cartella iniziale predefinita
        # filetypes=(("Tutti i File", "*.*"),("File di testo", "*.txt")),
    )

    if filename == "":
        messagebox.showerror("Attenzione", "File non selezionato")
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
            l2.config(text=files[0] + "/" + codice_selezionato)

    else:
        messagebox.showerror("Errore", "Dati su USB non trovati")
        return
    with open(filename, "rb") as file_binario:
        dati_caricati = pickle.load(file_binario)
    testo_criptato = dati_caricati["testo_criptato"]
    n = dati_caricati["semiprimo"]

    carica_tc = list(testo_criptato)
    a = n % chiave
    b = n - a

    for i in range(10):
        r = gcd(a, b)
        if r != 1:
            p = r
            q = n // p
            break
        a = a + chiave
        b = b - chiave
    if r == 1:
        messagebox.showerror("Attenzione", "Codifica non Superata")
        return
    # *controllo quanti pacchetti di 3 riesco a estrarre dal fattore primo q
    lista_q = list(str(q))

    n_round = ((len(lista_q) - 100)) // 3 * 3

    # *creo due punti di partenza differenti
    start1 = str(q)
    start2 = len(start1)
    c_round1 = int(start1[start2 - 9] + start1[start2 - 3])
    c_round2 = int(start1[start2 - 7] + start1[start2 - 4])
    # *creo due liste contenenti un numero divisibile per 3
    div_round1 = []
    div_round2 = []

    for ii in range(c_round1, c_round1 + n_round, 3):
        div_round1.append((lista_q[ii] + lista_q[ii + 1] + lista_q[ii + 2]))

    for ii in range(c_round2, c_round2 + n_round, 3):
        div_round2.append((lista_q[ii] + lista_q[ii + 1] + lista_q[ii + 2]))

    # ************************************************************
    chiave_xor = ""
    chiave_bin1 = ""
    for i in range(len(div_round1)):
        num_int = int(div_round1[i])
        bin1 = bin(num_int)[2:].zfill(11)

        chiave_bin1 = chiave_bin1 + chr(int(bin1, 2))

        num_int = int(div_round2[i])
        bin2 = bin(num_int)[2:].zfill(11)

        int_bin1 = int(bin1, 2)
        int_bin2 = int(bin2, 2)
        bin_x = int_bin1 ^ int_bin2
        xor_bin = bin(bin_x)[2:].zfill(11)
        chiave_xor = chiave_xor + chr(int(xor_bin, 2))
    c_xor = list(chiave_xor)
    ii = 0
    testo_decriptato = ""
    for i in range(len(carica_tc)):
        if ii == len(c_xor):
            ii = 0
        p_asci = ord(c_xor[ii])
        p_asci2 = ord(carica_tc[i])
        codifica1 = int(p_asci)
        codifica2 = int(p_asci2)
        crea_codifica = codifica1 ^ codifica2
        xor_testo = bin(crea_codifica)[2:].zfill(11)
        testo_decriptato = testo_decriptato + str(int(xor_testo, 2))
        ii += 1
    lista_dec = list(testo_decriptato)
    lista_dec3 = []
    for i in range(0, len(lista_dec), 3):
        lista_dec3.append(lista_dec[i] + lista_dec[i + 1] + lista_dec[i + 2])
    lista_testo = lista_dec3[:-5]
    lista_m = lista_dec3[-5:]
    tdec = decripta(lista_m,lista_testo,p)
    tw2.delete('1.0',tk.END)
    tw2.insert('1.0',tdec)

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
        messagebox.showwarning(
        "Attenzione", "Nessuna codifica selezionata" + apri_dati
        )

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
# * cripta file di testo con scostamento GC57
# *******************************************************

def cripta(p):
    global start
    f1 = tw1.get('1.0',tk.END)
    f1=f1.strip()

    start1 = str(p)
    start2 = len(start1)
    start = int(start1[start2 - 5] + start1[start2 - 4])

    ln = list(str(p))
    if len(ln) % 2 == 0:
        pass
    else:
        ln.append("0")

    divln = []
    for i in range(0, len(ln), 2):
        c1 = int(ln[i])
        c2 = int(ln[i + 1])
        c3 = c1 * 10 + c2
        divln.append(c3)
    # **********************************************
    m1 = randint(100, 400)
    m2 = randint(100, 400)
    m3 = randint(100, 400)
    m4 = randint(100, 400)
    m5 = randint(100, 400)
    # **********************************************

    text = f1
    te = list(text)
    cont = start
    tcript = ""
    # *************************
    # *regole di codifica testo
    # *************************
    for i in range(len(text)):
        if cont == len(divln):
            cont = 0
        if ord(te[i]) > 700:
            pass
        else:
            x = int(divln[cont])
            if x >= 0 and x < 25:
                x = x + m1 + ord(te[i])
            if x >= 25 and x < 40:
                x = x + m2 + ord(te[i])
            if x >= 40 and x < 50:
                x = x + m3 + ord(te[i])
            if x >= 50 and x < 75:
                x = x + m4 + ord(te[i])
            if x >= 75 and x < 100:
                x = x + m5 + ord(te[i])
            tcript = tcript + str(x)
            cont = cont + 1
    tcript = tcript + str(m1)
    tcript = tcript + str(m2)
    tcript = tcript + str(m3)
    tcript = tcript + str(m4)
    tcript = tcript + str(m5)
    return tcript

# *******************************************************
# * Mescola la criptazione con XOR
# *******************************************************

def codifica():
    if filename=='':
        messagebox.showerror('Attenzione','Non è stata selezionata nessuna codifica')
        return
    testo=tw1.get('1.0',tk.END)
    if testo=='' or len(testo)<12:
        messagebox.showerror("Attenzione", "Messaggio mancante o Troppo corto")
        return

    with open(filename, "r") as file:
        righe = file.readlines()
        codice_random = randint(0, len(righe) - 1)  # Genera un indice casuale
        n = righe[codice_random]
        n=int(n.strip())
        a = n % chiave
        b = n - a
        for i in range(10):
            r = gcd(a, b)
            if r != 1:
                p=r
                q=n//p
                break
            a = a + chiave
            b = b - chiave
        if r == 1:
            messagebox.showerror('Attenzione','Codifica non Superata')
            return

        testo_cript=cripta(p)

        lista_tc = list(testo_cript)
        lista_tc3 = []

        for i in range(0, len(lista_tc), 3):
            lista_tc3.append(lista_tc[i] + lista_tc[i + 1] + lista_tc[i + 2])

        # *controllo quanti pacchetti di 3 riesco a estrarre dal fattore primo q
        lista_q = list(str(q))

        n_round = ((len(lista_q) - 100)) // 3 * 3

        # *creo due punti di partenza differenti
        start1 = str(q)
        start2 = len(start1)
        c_round1 = int(start1[start2 - 9] + start1[start2 - 3])
        c_round2 = int(start1[start2 - 7] + start1[start2 - 4])

        # *creo due liste contenenti un numero divisibile per 3
        div_round1 = []
        div_round2 = []

        for ii in range(c_round1, c_round1 + n_round, 3):
            div_round1.append((lista_q[ii] + lista_q[ii + 1] + lista_q[ii + 2]))

        for ii in range(c_round2, c_round2 + n_round, 3):
            div_round2.append((lista_q[ii] + lista_q[ii + 1] + lista_q[ii + 2]))

        # ************************************************************
        chiave_xor = ""
        chiave_bin1 = ""

        for i in range(len(div_round1)):
            num_int = int(div_round1[i])
            bin1 = bin(num_int)[2:].zfill(11)

            chiave_bin1 = chiave_bin1 + chr(int(bin1, 2))

            num_int = int(div_round2[i])
            bin2 = bin(num_int)[2:].zfill(11)

            int_bin1 = int(bin1, 2)
            int_bin2 = int(bin2, 2)
            bin_x = int_bin1 ^ int_bin2
            xor_bin = bin(bin_x)[2:].zfill(11)
            chiave_xor = chiave_xor + chr(int(xor_bin, 2))

        c_xor = list(chiave_xor)
        ii = 0
        testo_criptato = ""
        for i in range(len(lista_tc3)):
            if ii == len(c_xor):
                ii = 0
            p_asci = ord(c_xor[ii])
            codifica1 = p_asci
            codifica2 = int(lista_tc3[i])
            crea_codifica = codifica1 ^ codifica2
            xor_testo = bin(crea_codifica)[2:].zfill(11)
            testo_criptato = testo_criptato + chr(int(xor_testo, 2))
            ii += 1

        dati_da_salvare = {"testo_criptato": testo_criptato, "semiprimo": n}

        # Salva i dati in un file binario usando pickle
        with open(programma_invia_a + "/GC57_mess_" + l1.cget('text'), "wb") as file_binario:
            pickle.dump(dati_da_salvare, file_binario)

        messagebox.showinfo("Salvataggio", "File Codificato Creato")
        return

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
    if l2.cget("text") != "":
        separa = l2.cget("text").split("/")
        l2.config(text="")
        cancella = programma_riceve_a + "/GC57_mess_" + separa[1]
        if os.path.exists(cancella):
            os.remove(cancella)


# *******************************************************
# * parte Grafica gestione pulsanti
# *******************************************************

def cancellatw1():
    tw1.delete("1.0", tk.END)
    return

def cancellatw2():
    tw2.delete("1.0", tk.END)
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
root.title("Codifica Con Metodo GC57 - PROGRAMMA A")
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
    command=codifica
)
b4.place(x=px, y=py)

px = px + 180
py=py-50

l1 = tk.Label(text='',width=10, bg=fondo_finestra, font="arial 14 bold")
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
    command=apri_filer,
)
b3.place(x=px, y=py)

px = px + 160

l2 = tk.Label(text="", width=12, bg=fondo_finestra, font="arial 14 bold")
l2.place(x=px, y=py)


# Carica l'immagine automaticamente quando la finestra si apre

testo = "CODIFICA\nGC57"
colore = "blue"  # Colore del testo
fonte = ("arial", 10, "bold")
colore_sfondo = fondo_finestra  # Colore dello sfondo
canvas.config(bg=colore_sfondo)
canvas.create_text(65,20,text='GC57crypto',fill='red',font=fonte)
canvas.create_text(65, 50, text="A", fill="red", font='arial 20 bold')
canvas.create_text(65, 85, text=testo, fill=colore, font=fonte)


root.mainloop()
