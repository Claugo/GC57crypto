# GC57eAL Invio dati Crisptati Esteso con Allegato
import tkinter as tk
from tkinter import messagebox, filedialog,simpledialog
import os
import pickle
from math import gcd,log
import hashlib
import time
from random import randint, seed
filename = ""
programma_invia_a = "g:\\"
programma_riceve_a = "g:\\"
programma_allegati = "g:\\allegati"

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

def prefin_close():
    pre_fin.destroy()
    quit()


# *************************************************
#          finestra programma invia
# *************************************************

def apri_invia():

    def invia_close():
        root_invia.destroy()
        pre_fin.deiconify()
        return

    #*codifica allegato
    def encode_byte(byte, conta,chi_list):
        # key = 0xC4  # Chiave XOR
        seed(int(chi_list[conta]))
        ran = randint(32, 256)
        bin_ran = bin(ran)[2:].zfill(8)

        key = int(bin_ran, 2)
        encoded_byte = byte ^ key
        return encoded_byte

    # *******************************************************
    # * cripta file di testo con scostamento GC57
    # *******************************************************

    def cripta(p):
        # global start
        f1 = tw1_invia.get("1.0", tk.END)
        f1 = f1.strip()

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
            if ord(te[i]) > 70000:
                pass
            else:
                x = int(divln[cont])
                seed(x)
                m1 = randint(10000, 30000)
                x = x + m1 + ord(te[i])
                tcript = tcript + str(x)
                cont = cont + 1
        return tcript

    # *******************************************************
    # * Chiama lo scostamento e mescola la criptazione con XOR
    # *******************************************************

    def codifica():
        if filename == "":
            messagebox.showerror("Attenzione", "Non è stata selezionata nessuna codifica")
            return
        testo = tw1_invia.get("1.0", tk.END)
        if testo == "" or len(testo) < 12:
            messagebox.showerror("Attenzione", "Messaggio mancante o Troppo corto")
            return

        T = int(time.time())
        seed(T)

        with open(filename, "r") as file:
            righe = file.readlines()
            codice_random = randint(0, len(righe) - 1)  # Genera un indice casuale
            nn = righe[codice_random]
            n = int(nn.strip())
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

            testo_cript = cripta(p)

            lista_tc = list(testo_cript)
            lista_tc3 = []

            for i in range(0, len(lista_tc), 5):
                lista_tc3.append(
                    lista_tc[i]
                    + lista_tc[i + 1]
                    + lista_tc[i + 2]
                    + lista_tc[i + 3]
                    + lista_tc[i + 4]
                )

            # *controllo quanti pacchetti di 3 riesco a estrarre dal fattore primo q
            lista_q = list(str(q))

            n_round = ((len(lista_q) - 100)) // 5 * 5

            # *creo due punti di partenza differenti
            start1 = str(q)
            start2 = len(start1)
            c_round1 = int(start1[start2 - 9] + start1[start2 - 3])
            c_round2 = int(start1[start2 - 7] + start1[start2 - 4])

            # *creo due liste contenenti un numero divisibile per 5
            div_round1 = []
            div_round2 = []

            for ii in range(c_round1, c_round1 + n_round, 5):
                div_round1.append(
                    (
                        lista_q[ii]
                        + lista_q[ii + 1]
                        + lista_q[ii + 2]
                        + lista_q[ii + 3]
                        + lista_q[ii + 4]
                    )
                )

            for ii in range(c_round2, c_round2 + n_round, 5):
                div_round2.append(
                    (
                        lista_q[ii]
                        + lista_q[ii + 1]
                        + lista_q[ii + 2]
                        + lista_q[ii + 3]
                        + lista_q[ii + 4]
                    )
                )

            # ************************************************************
            chiave_xor = ""
            chiave_bin1 = ""

            for i in range(len(div_round1)):
                num_int = int(div_round1[i])
                bin1 = bin(num_int)[2:].zfill(17)

                chiave_bin1 = chiave_bin1 + chr(int(bin1, 2))

                num_int = int(div_round2[i])
                bin2 = bin(num_int)[2:].zfill(17)

                int_bin1 = int(bin1, 2)
                int_bin2 = int(bin2, 2)
                bin_x = int_bin1 ^ int_bin2
                xor_bin = bin(bin_x)[2:].zfill(17)
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
                xor_testo = bin(crea_codifica)[2:].zfill(17)
                testo_criptato = testo_criptato + chr(int(xor_testo, 2))
                ii += 1
            allegato_invia=e1_invia.get()

            if not allegato_invia or len(allegato_invia) < 6:
                dati_da_salvare = {"testo_criptato": testo_criptato, "semiprimo": n}

                # Salva i dati in un file binario usando pickle senza allegato
                with open(programma_invia_a + "/GC57eAL_mess_" + codice_selezionato, "wb") as file_binario:
                    pickle.dump(dati_da_salvare, file_binario)

                messagebox.showinfo("Salvataggio", "File Codificato Creato")
                return 
            else:
                # Cripta l'allegato se è stato fornito

                start1 = str(q)
                start2 = len(start1)
                start = int(start1[start2 - 8] + start1[start2 - 5])

                chi_list=[]
                fatq=str(q)
                if len(fatq)%2==0:
                    pass
                else:
                    fatq=fatq+'0'

                for i in range(0,len(fatq),2):
                    chi_list.append(fatq[i:i+2])
                #print(chi_list)

                conta=start
                allegato_criptato=[]
                with open(filename_allegato, "rb") as encoded_file:
                    byte = encoded_file.read(1)
                    while byte:
                        if conta>=len(chi_list):
                            conta=0
                        encoded_byte = encode_byte(byte[0],conta,chi_list)
                        allegato_criptato.append(
                            encoded_byte
                        )  # Memorizza il byte processato nella lista
                        byte = encoded_file.read(1)
                        conta=conta+1


                # allegato_criptato = cripta_allegato(allegato_invia)

                dati_da_salvare = {
                    "testo_criptato": testo_criptato,
                    "semiprimo": n,
                    "allegato_nome": allegato_invia,
                    "allegato_criptato": allegato_criptato
                }
                # Salva i dati in un file binario usando pickle con allegato
                with open(programma_invia_a + "/GC57eAL_mess_" + codice_selezionato, "wb") as file_binario:
                    file_binario.write(b"ALLEGATO_MARCATORE")  # Marcatore per indicare la presenza di un allegato
                    pickle.dump(dati_da_salvare, file_binario)

                messagebox.showinfo("Salvataggio", "File Codificato con Allegato Creato")
                return

    # *******************************************************
    # * Apre file semiprimi scelta tipo di codifica (INVIA)
    # *******************************************************
    def apri_codifica():
        global codice_selezionato, chiave, filename
        filename = filedialog.askopenfilename(
            title="Apri file",
            initialdir="c:\\semiprimi",  # Cartella iniziale predefinita
        )

        if filename == "":
            messagebox.showwarning("Attenzione", "Nessuna codifica selezionata" + apri_dati)
            return
        semipsel = filename.split("/")
        codice_selezionato = semipsel[2]
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

        e2_invia.delete(0, tk.END)
        e2_invia.insert(0, codice_selezionato)

    # *******************************************************
    # *             Carica allegato (INVIA)
    # *******************************************************
    def apri_allegato():
        global filename_allegato
        if e2_invia.get()=='':
            messagebox.showerror('Attenzione','Selezionare prima tipo di codifica')
            return
        filename_allegato = filedialog.askopenfilename(
            title="Apri file",
            initialdir="C:\\Users/Claugo/OneDrive/Documenti",
            filetypes=(
                ("Tutti i File", "*.*"),
                ("File di testo", "*.txt"),
                ("File PDF", "*.pdf"),
            ),
        )
        if filename_allegato=='':
            return
        else:
            cartella,allegato=os.path.split(filename_allegato)
            e1_invia.delete(0,tk.END)
            e1_invia.insert(0,allegato)

    # *******************************************************
    # *               Interfaccia (INVIA)
    # *******************************************************
    fondo_finestra = "#2F4F4F"
    colore_testo = "#E6E6FA"
    fondo_text = "#00688B"
    root_invia = tk.Toplevel()
    root_invia.title("Programma di Criptazione Dati - INVIA")
    root_invia.geometry("700x600")
    root_invia.config(bg=fondo_finestra)
    root_invia.protocol("WM_DELETE_WINDOW", invia_close)
    l1_invia = tk.Label(
        root_invia,
        text="INVIA CryptoGC57",
        bg=fondo_finestra,
        font="arial 18 bold",
        fg=colore_testo,
    )
    l1_invia.place(x=210, y=20)

    tw1_invia = tk.Text(
        root_invia,
        width=75,
        height=20,
        bg=fondo_text,
        font="helvetica, 12",
        cursor="left_ptr",
        wrap=tk.WORD,
    )
    tw1_invia.place(x=10,y=70)
    b1_invia = tk.Button(
        root_invia,
        text="Invia File",
        fg="#006400",
        width=15,
        font="arial 12 bold",
        cursor="hand2",
        command=codifica,
    )
    b1_invia.place(x=500, y=450)

    b2_invia = tk.Button(
        root_invia,
        text="Carica Allegato",
        fg="#006400",
        width=15,
        font="arial 12 bold",
        cursor="hand2",
        command=apri_allegato
    )
    b2_invia.place(x=10, y=490)

    b3_invia = tk.Button(
        root_invia,
        text="Seleziona Codifica",
        fg="#006400",
        width=15,
        font="arial 12 bold",
        cursor="hand2",
        command=apri_codifica,
    )
    b3_invia.place(x=10, y=530)

    e1_invia = tk.Entry(
        root_invia,
        width=25,
        font="arial 12 bold",
        bg=fondo_finestra,
        borderwidth=2,
        relief=tk.SUNKEN,
    )
    e1_invia.place(x=180,y=495)

    e2_invia = tk.Entry(
        root_invia,
        width=25,
        font="arial 12 bold",
        bg=fondo_finestra,
        borderwidth=2,
        relief=tk.SUNKEN,
    )
    e2_invia.place(x=180, y=535)

    pre_fin.withdraw()


# *************************************************
#  finestra programma riceve
# *************************************************

def apri_riceve():
    def riceve_close():
        root_riceve.destroy()
        pre_fin.deiconify()
        return

    def decode_byte(decoded_byte, conta,chi_list):
        # key = 0xC4  # Chiave XOR
        seed(int(chi_list[conta]))
        ran = randint(32, 256)
        bin_ran = bin(ran)[2:].zfill(8)

        key = int(bin_ran, 2)
        decoded_byte = decoded_byte ^ key
        return decoded_byte

    # *******************************************************
    # * decripta file ricevuto
    # *******************************************************
    def decripta(lista_dec5, p):

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

        cont = start
        tdecript = ""
        for i in range(len(lista_dec5)):
            if cont == len(divln):
                cont = 0
            x = int(divln[cont])
            seed(x)
            m1 = randint(10000, 30000)
            y = int(lista_dec5[i])
            tdecript = tdecript + chr(y - x - m1)
            cont = cont + 1
        return tdecript

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
                # l2.config(text=files[0] + "/" + codice_selezionato)

        else:
            messagebox.showerror("Errore", "Dati su USB non trovati")
            return

        with open(filename, "rb") as file_binario:
            # Controlla se il marcatore di allegato è presente
            if file_binario.read(len(b"ALLEGATO_MARCATORE")) == b"ALLEGATO_MARCATORE":
                allegato_presente = True
            else:
                allegato_presente = False

            # Riposiziona il puntatore del file all'inizio dopo la lettura del marcatore
            file_binario.seek(0)

            # Se è presente un allegato, leggi i dati come prima del marcatore
            if allegato_presente:
                file_binario.read(len(b"ALLEGATO_MARCATORE"))

            dati = pickle.load(file_binario)
            testo_criptato = dati.get("testo_criptato")
            semiprimo = dati.get("semiprimo")

            n = int(semiprimo)
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
            carica_tc = list(testo_criptato)
            lista_q = list(str(q))

            n_round = ((len(lista_q) - 100)) // 5 * 5

            # *creo due punti di partenza differenti
            start1 = str(q)
            start2 = len(start1)
            c_round1 = int(start1[start2 - 9] + start1[start2 - 3])
            c_round2 = int(start1[start2 - 7] + start1[start2 - 4])
            # *creo due liste contenenti un numero divisibile per 3
            div_round1 = []
            div_round2 = []
            for ii in range(c_round1, c_round1 + n_round, 5):
                div_round1.append(
                        (
                            lista_q[ii]
                            + lista_q[ii + 1]
                            + lista_q[ii + 2]
                            + lista_q[ii + 3]
                            + lista_q[ii + 4]
                        )
                    )

            for ii in range(c_round2, c_round2 + n_round, 5):
                div_round2.append(
                        (
                            lista_q[ii]
                            + lista_q[ii + 1]
                            + lista_q[ii + 2]
                            + lista_q[ii + 3]
                            + lista_q[ii + 4]
                        )
                    )

            # ************************************************************
            chiave_xor = ""
            chiave_bin1 = ""
            for i in range(len(div_round1)):
                num_int = int(div_round1[i])
                bin1 = bin(num_int)[2:].zfill(17)

                chiave_bin1 = chiave_bin1 + chr(int(bin1, 2))

                num_int = int(div_round2[i])
                bin2 = bin(num_int)[2:].zfill(17)

                int_bin1 = int(bin1, 2)
                int_bin2 = int(bin2, 2)
                bin_x = int_bin1 ^ int_bin2
                xor_bin = bin(bin_x)[2:].zfill(17)
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
                xor_testo = bin(crea_codifica)[2:].zfill(17)
                testo_decriptato = testo_decriptato + str(int(xor_testo, 2))
                ii += 1
            lista_dec = list(testo_decriptato)
            lista_dec5 = []
            for i in range(0, len(lista_dec), 5):
                lista_dec5.append(
                        lista_dec[i]
                        + lista_dec[i + 1]
                        + lista_dec[i + 2]
                        + lista_dec[i + 3]
                        + lista_dec[i + 4]
                    )    
            tdec = decripta(lista_dec5, p)
            tw1_riceve.delete("1.0", tk.END)
            tw1_riceve.insert("1.0", tdec)

            if allegato_presente:
                allegato_criptato = dati.get("allegato_criptato")
                allegato_inviato = dati.get("allegato_nome")
                e1_riceve.delete(0,tk.END)
                e1_riceve.insert(0,allegato_inviato)
            else:
                return
            
            
            start1 = str(q)
            start2 = len(start1)
            start = int(start1[start2 - 8] + start1[start2 - 5])
            chi_list=[]
            fatq=str(q)
            if len(fatq)%2==0:
                pass
            else:
                fatq=fatq+'0'

            for i in range(0,len(fatq),2):
                chi_list.append(fatq[i:i+2])
            conta=start    

            with open(programma_allegati+'/'+allegato_inviato, "wb") as decoded_file:
                for byte in allegato_criptato:
                    if conta >= len(chi_list):
                        conta = 0
                    decoded_byte = decode_byte(byte, conta,chi_list)
                    decoded_file.write(decoded_byte.to_bytes(1, "little"))
                    conta +=1 
    # *******************************************************
    # *               Interfaccia (Riceve)
    # *******************************************************

    fondo_finestra = "#292421"
    colore_testo='#E6E6FA'
    fondo_text = "#00688B"

    root_riceve = tk.Toplevel()
    root_riceve.title("Programma di Criptazione Dati - RICEVE")
    root_riceve.geometry("700x550")
    root_riceve.config(bg=fondo_finestra)
    l1_riceve = tk.Label(
        root_riceve,
        text="LEGGI CryptoGC57",
        bg=fondo_finestra,
        font="arial 18 bold",
        fg=colore_testo,
    )
    l1_riceve.place(x=210,y=20)

    tw1_riceve = tk.Text(
        root_riceve,
        width=75,
        height=20,
        bg=fondo_text,
        cursor="left_ptr",
        font="helvetica, 12",
        wrap=tk.WORD,
    )
    tw1_riceve.place(x=10,y=70)

    b1_riceve = tk.Button(
        root_riceve,
        text="Carica File",
        fg="#228B22",
        width=15,
        font="arial 12 bold",
        cursor="hand2",
        command=apri_filer,
    )
    b1_riceve.place(x=10, y=450)

    px=450
    py=475
    l1_riceve = tk.Label(
        root_riceve,
        text="Allegato",
        bg=fondo_finestra,
        font="arial 12 bold",
        fg=colore_testo,
    )
    l1_riceve.place(x=px, y=py)
    py=py+30
    e1_riceve = tk.Entry(
        root_riceve,
        width=23,
        font="arial 12 bold",
        fg='#66CD00',
        justify='center',
        bg=fondo_finestra,
        borderwidth=2,
        relief=tk.SUNKEN,
    )
    e1_riceve.place(x=px, y=py)

    root_riceve.protocol("WM_DELETE_WINDOW", riceve_close)

    pre_fin.withdraw()


# *************************************************
#  finestra principale
# *************************************************

pre_fin = tk.Tk()
pre_fin.title("********  Programma di Criptazione Dati con Allegati ***********")
pre_fin.geometry("500x210")
pre_fin.config(bg="#104E8B")

l1_pre = tk.Label(
    pre_fin,
    text="Crypto GC57eAL",
    bg="#104E8B",
    fg="#87CEFA",
    font="arial 20 bold",
)
l1_pre.place(x=130, y=30)

l2_pre = tk.Label(
    pre_fin,
    text="Condividi i tuoi File in totale sicurezza",
    bg="#104E8B",
    font="helvetica 14 bold",
)
l2_pre.place(x=53, y=80)

b1_pre = tk.Button(
    pre_fin,
    text="Invia File",
    fg="#228B22",
    width=15,
    font="arial 12 bold",
    cursor="hand2",
    command=apri_invia,
)
b1_pre.place(x=10, y=170)

b2_pre = tk.Button(
    pre_fin,
    text="Leggi File",
    fg="#228B22",
    width=15,
    font="arial 12 bold",
    cursor="hand2",
    command=apri_riceve,
)
b2_pre.place(x=330, y=170)

pre_fin.protocol("WM_DELETE_WINDOW", prefin_close)
pre_fin.mainloop()
