# generatore_password schede
import sqlite3
import string
import tkinter as tk
from tkinter import messagebox, ttk, filedialog, simpledialog
from random import seed,randint,random,choice
from sympy import nextprime
from math import gcd
import time
import os
import pickle
import hashlib
T=int(time.time())
seed(T)

# *******************************************************
# * controllo file CFG
# *******************************************************

filecfg = "passcfg"
if os.path.exists(filecfg):
    pass
else:

    def chiudi_programma():
        risposta = messagebox.askquestion("Attenzione:", "uscire dal programma?")
        if risposta == "yes":
            rootcfg.destroy()
            quit()
        else:
            return

    def salva_esci():
        controllo1 = e2_cfg.get()
        if controllo1 == "":
            messagebox.showerror("Attenzione:", "Campo Cartella Vuoto")
            return
        elif os.path.exists(f"{controllo1}"):
            pass
        else:
            messagebox.showerror("Attenzione:", "La cartella INVIO non esiste")
            return


        scrivi = open("passcfg", "w")
        scrivi.write(controllo1 + "\n")
        scrivi.close()
        messagebox.showinfo("Salvataggi CFG:", "Configurazione Salvata")
        rootcfg.destroy()

    rootcfg = tk.Tk()

    # Imposta le dimensioni della finestra
    window_width = 415
    window_height = 270

    # Ottieni le dimensioni dello schermo
    screen_width = rootcfg.winfo_screenwidth()
    screen_height = rootcfg.winfo_screenheight()

    # Calcola la posizione x e y per centrare la finestra
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Imposta la posizione e le dimensioni della finestra
    rootcfg.geometry(f"{window_width}x{window_height}+{x}+{y}")
    rootcfg.title("Configurazione Cartella Pass_schede")
    rootcfg.configure(bg="#458B74")
    colore_testo_entry = "#104E8B"
    testo = (
        "Se appare questa finestra è perchè il programma viene eseguito per la prima volta in questa posizione, \
oppure il file 'Passcfg' è stato cancellato\n\
Copiare e incollare con CTR-V la posizione della cartella:",
    )

    l1_cfg = tk.Label(
        rootcfg, text=testo, justify=tk.LEFT, font="arial 12 bold", wraplength=400
    )
    l1_cfg.place(x=10, y=20)

    px = 10
    py = 150
    l2_cfg = tk.Label(
        rootcfg,
        text="Incollare Indirizzo Cartella",
        bg="#458B74",
        font="arial 12 bold",
    )
    l2_cfg.place(x=px, y=py)
    py = py + 20
    e2_cfg = tk.Entry(rootcfg, width=40, fg=colore_testo_entry, font="arial 12")
    e2_cfg.place(x=px, y=py)

    px = px + 150
    py = py + 50
    b1 = tk.Button(
        rootcfg,
        text="Salva ed Esci",
        font="arial 12 bold",
        cursor="hand1",
        bg="green",
        command=salva_esci,
    )
    b1.place(x=px, y=py)
    rootcfg.protocol("WM_DELETE_WINDOW", chiudi_programma)

    rootcfg.mainloop()

# *******************************************************
# * Carica CFG
# *******************************************************
filename = ""
apricfg = open("passcfg", "r")
cartella_scheda= apricfg.readline().strip()
apricfg.close()
if len(cartella_scheda)>3:
    cartella_scheda=cartella_scheda+"/"
    
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
if os.path.exists(usb_path+"chiave_pass.txt"):
    apri = open(usb_path + "chiave_pass.txt", "r")
    s1=apri.readline()
    apri.close()
    s1=int(s1)
else:
    messagebox.showwarning(
        "Attenzione", "File chiave non trovato"
    )
    quit()
chiave=s1**20


# *******************************************************
# * Carica schedario criptato e lo decripta
# *******************************************************
if os.path.exists(f"{cartella_scheda} schede.crp"):
    def decode_byte(decoded_byte, conta,chi_list):
        # key = 0xC4  # Chiave XOR
        seed(int(chi_list[conta]))
        ran = randint(32, 256)
        bin_ran = bin(ran)[2:].zfill(8)

        key = int(bin_ran, 2)
        decoded_byte = decoded_byte ^ key
        return decoded_byte

    with open(f"{cartella_scheda} schede.crp", "rb") as file:
        dati = pickle.load(file)

    # Ora possiamo accedere ai dati
    semiprimo = dati.get("semiprimo")
    schede_criptate = dati.get("schede_criptate")

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
        quit()
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

    with open(f"{cartella_scheda} schede.db", "wb") as decoded_file:
        for byte in schede_criptate:
            if conta >= len(chi_list):
                conta = 0
            decoded_byte = decode_byte(byte, conta,chi_list)
            decoded_file.write(decoded_byte.to_bytes(1, "little"))
            conta +=1 

# *******************************************************
# Creare una connessione al database (o creare il database se non esiste)
# *******************************************************

conn = sqlite3.connect(f"{cartella_scheda} schede.db")

# Creare un cursore
cur = conn.cursor()

# Creare la tabella delle schede con tre dati di tipo stringa
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS schede (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dato1 TEXT NOT NULL,
        dato2 TEXT NOT NULL,
        dato3 TEXT NOT NULL
    )
"""
)
# ************************************************
#                 ESCI senza CODIFICA
# ************************************************
def esci_senza_codifica():
    risposta=messagebox.askquestion("Attenzione","uscita senza codifica, Procedere?")
    if risposta=="yes":
        conn.close()
        os.remove(f"{cartella_scheda} schede.db")
        root.destroy()
        quit()
    else:
        return    


# ************************************************
#                 ESCI e CODIFICA
# ************************************************

def encode_byte(byte, conta,chi_list):
    # key = 0xC4  # Chiave XOR
    seed(int(chi_list[conta]))
    ran = randint(32, 256)
    bin_ran = bin(ran)[2:].zfill(8)

    key = int(bin_ran, 2)
    encoded_byte = byte ^ key
    return encoded_byte


def esci_codifica():
    # Chiudere la connessione al database quando il programma termina
    conn.close()
    p=nextprime(s1**18+randint(1,2**200))
    q=nextprime(s1**23+randint(1,2**200))
    semiprimo=p*q

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
    # print(chi_list)

    conta=start
    schede_criptate=[]
    with open(f"{cartella_scheda} schede.db", "rb") as encoded_file:
        byte = encoded_file.read(1)
        while byte:
            if conta>=len(chi_list):
                conta=0
            encoded_byte = encode_byte(byte[0],conta,chi_list)
            schede_criptate.append(
                encoded_byte
            )  # Memorizza il byte processato nella lista
            byte = encoded_file.read(1)
            conta=conta+1

    # schede_criptate = cripta_allegato(allegato_invia)

    dati_da_salvare = {
        "semiprimo": semiprimo,
        "schede_criptate": schede_criptate
    }
    # Salva i dati in un file binario usando pickle con allegato
    with open(f"{cartella_scheda} schede.crp", "wb") as file_binario:
        pickle.dump(dati_da_salvare, file_binario)

    messagebox.showinfo("Salvataggio", "Database password codificato correttamente")
    os.remove(f"{cartella_scheda} schede.db")
    root.destroy()
    quit()


# ************************************************
# Salvare le modifiche
# ************************************************
conn.commit()


def salva_p():
    pas = e1.get().strip()
    if pas == "":
        messagebox.showerror("Attenzione", "Password Vuota")
        return
    nome_collegamento = e3.get().strip()
    if nome_collegamento == "":
        messagebox.showerror("Attenzione", "Nome collegamento vuoto")
        return
    descr = e4.get().strip()
    if descr == "":
        messagebox.showerror("Attenzione", "Descrizione Vuota")
        return

    # Inserire i dati nel database
    cur.execute(
        """
        INSERT INTO schede (dato1, dato2, dato3)
        VALUES (?, ?, ?)
    """,
        (pas, nome_collegamento, descr),
    )
    conn.commit()

    messagebox.showinfo("ok", "Password Salvata")
    return


def genera_password():
    n_caratteri = e2.get()
    if n_caratteri == "":
        n_caratteri = 16
    else:
        n_caratteri = int(n_caratteri)
    if n_caratteri > 32:
        messagebox.showerror("Attenzione", "Numero Caratteri Fuori Scala")
        return
    caratteri = string.ascii_letters + string.digits + string.punctuation
    password = "".join(choice(caratteri) for i in range(n_caratteri))
    e1.delete(0, tk.END)
    e1.insert(0, password)


def copia_in_memoria():
    text = e1.get()
    root.clipboard_clear()
    root.clipboard_append(text)
    messagebox.showinfo("Copiato", "Il testo è stato copiato negli appunti")


def carica_dati():
    # Creare una nuova finestra
    carica_finestra = tk.Toplevel(root)
    carica_finestra.title("Gestione Dati")
    carica_finestra.geometry("600x400")
    carica_finestra.configure(bg=fondo_finestra)

    # Definire una funzione per aggiornare la visualizzazione dei dati
    def aggiorna_visualizzazione():
        for row in tree.get_children():
            tree.delete(row)
        cur.execute("SELECT * FROM schede")
        rows = cur.fetchall()
        for row in rows:
            tree.insert("", tk.END, values=row)

    # Definire una funzione per eliminare un dato
    def elimina_dato():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Errore", "Nessun elemento selezionato")
            return
        item = tree.item(selected_item)
        id = item["values"][0]
        cur.execute("DELETE FROM schede WHERE id = ?", (id,))
        conn.commit()
        aggiorna_visualizzazione()

    # Definire una funzione per copiare la password
    def copia_pas():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Errore", "Nessun elemento selezionato")
            return
        item = tree.item(selected_item)
        password = item["values"][1]
        carica_finestra.clipboard_clear()
        carica_finestra.clipboard_append(password)
        messagebox.showinfo("Copiato", "Password copiata negli appunti")
        carica_finestra.destroy()

    # Definire una funzione per modificare un dato
    def modifica_dato():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Errore", "Nessun elemento selezionato")
            return
        item = tree.item(selected_item)
        id = item["values"][0]

        # Creare una finestra di modifica
        modifica_finestra = tk.Toplevel(carica_finestra)
        modifica_finestra.title("Modifica Dato")
        modifica_finestra.geometry("400x300")
        modifica_finestra.configure(bg=fondo_finestra)

        # Definire le Entry per modificare i dati
        tk.Label(
            modifica_finestra, text="Password", font="arial 12 bold", bg=fondo_finestra
        ).pack(pady=5)
        new_dato1 = tk.Entry(
            modifica_finestra, width=40, justify="center", font="arial 12"
        )
        new_dato1.pack()
        new_dato1.insert(0, item["values"][1])

        tk.Label(
            modifica_finestra,
            text="Nome collegamento",
            font="arial 12 bold",
            bg=fondo_finestra,
        ).pack(pady=5)
        new_dato2 = tk.Entry(
            modifica_finestra, width=40, justify="center", font="arial 12"
        )
        new_dato2.pack()
        new_dato2.insert(0, item["values"][2])

        tk.Label(
            modifica_finestra,
            text="Descrizione",
            font="arial 12 bold",
            bg=fondo_finestra,
        ).pack(pady=5)
        new_dato3 = tk.Entry(
            modifica_finestra, width=40, justify="center", font="arial 12"
        )
        new_dato3.pack()
        new_dato3.insert(0, item["values"][3])

        def salva_modifiche():
            cur.execute(
                """
                UPDATE schede
                SET dato1 = ?, dato2 = ?, dato3 = ?
                WHERE id = ?
            """,
                (new_dato1.get(), new_dato2.get(), new_dato3.get(), id),
            )
            conn.commit()
            aggiorna_visualizzazione()
            modifica_finestra.destroy()

        tk.Button(
            modifica_finestra,
            text="Salva",
            command=salva_modifiche,
            font="arial 12",
            cursor="hand2",
        ).pack(pady=20)

    # Creare una Treeview per visualizzare i dati
    columns = ("ID", "Password", "Nome collegamento", "Descrizione")
    tree = ttk.Treeview(carica_finestra, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(expand=True, fill="both")

    # Aggiungere i bottoni per eliminare, modificare e copiare la password
    btn_frame = tk.Frame(carica_finestra, bg=fondo_finestra)
    btn_frame.pack(pady=10)
    tk.Button(
        btn_frame, text="Elimina", command=elimina_dato, font="arial 12", cursor="hand2"
    ).pack(side=tk.LEFT, padx=10)
    tk.Button(
        btn_frame,
        text="Modifica",
        command=modifica_dato,
        font="arial 12",
        cursor="hand2",
    ).pack(side=tk.LEFT, padx=10)
    tk.Button(
        btn_frame,
        text="Copia Password",
        command=copia_pas,
        font="arial 12",
        cursor="hand2",
    ).pack(side=tk.LEFT, padx=10)

    # Caricare i dati iniziali
    aggiorna_visualizzazione()


fondo_finestra = "#CDB79E"
rootx = 410
rooty = 400

# Crea la finestra principale
root = tk.Tk()
root.geometry(f"{rootx}x{rooty}")
root.title("Genera Password")
root.configure(bg=fondo_finestra)
px = 100
py = 10

e1 = tk.Entry(root, width=25, justify="center", font="arial 12")
e1.place(x=px, y=py)
py = py + 30
tk.Button(
    root, text="Copia", command=copia_in_memoria, font="arial 12", cursor="hand2"
).place(x=px + 80, y=py)
py = py + 50
tk.Button(
    root,
    text="Genera Password",
    command=genera_password,
    font="arial 12",
    cursor="hand2",
).place(x=px + 33, y=py)

px = 20
py = py + 50

tk.Label(root, text="N. Caratteri", font="arial 12 bold", bg=fondo_finestra).place(
    x=px, y=py
)
e2 = tk.Entry(root, width=3, justify="center", font="arial 12")
e2.place(x=px + 100, y=py)

py = py + 50
tk.Label(root, text="Nome collegamento", font="arial 12 bold", bg=fondo_finestra).place(
    x=px, y=py
)
py = py + 20
e3 = tk.Entry(root, width=40, justify="center", font="arial 12")
e3.place(x=px, y=py)

py = py + 50
tk.Label(root, text="Descrizione", font="arial 12 bold", bg=fondo_finestra).place(
    x=px, y=py
)
py = py + 20
e4 = tk.Entry(root, width=40, justify="center", font="arial 12")
e4.place(x=px, y=py)

py = py + 70
tk.Button(
    root, text="Salva", font="arial 12", cursor="hand2", command=salva_p, bg="#C1FFC1"
).place(x=px, y=py)

tk.Button(
    root,
    text="Carica",
    font="arial 12",
    cursor="hand2",
    command=carica_dati,
    bg="#C1FFC1",
).place(x=px + 300, y=py)

tk.Button(
    root, text="Esci e Codifica", font="arial 12", cursor="hand2", bg="#97FFFF",command=esci_codifica
).place(x=px + 120, y=py)
root.protocol("WM_DELETE_WINDOW", esci_senza_codifica)

root.mainloop()
