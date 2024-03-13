import tkinter as tk
from PIL import Image, ImageTk
import os
from tkinter import simpledialog
from tkinter import messagebox
from sympy import nextprime
from random import randint, seed
import time

T = int(time.time())
seed(T)


apri_dati = simpledialog.askstring("USB", "Inserisci la porta USB se diversa da D")
if not apri_dati:
    apri_dati = "D"


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


# cartella1 = "C:\\DCP/Dropbox/cartella_a"
# cartella2 = "C:\\DCP/Dropbox/cartella_b"
cartella3='c:\\semiprimi'

if os.path.exists(cartella3):
    pass
else:
    os.makedirs(cartella3)


def esegui():
    nds = e1.get()
    ec=e2.get()
    ep=e3.get()
    eq=e4.get()
    agg=e5.get()
    campo=e6.get()
    bit=e7.get()
    numero=e8.get()

    if nds=='' or ec=='' or ep=='' or eq=='' or agg=='' or campo=='' or bit=='':
        messagebox.showerror('Attenzione:','tutti i campi devono essere compilati')
        return
    if numero=='' or int(numero)>20:
        risposta=messagebox.askquestion('il numero inserito è alto.\nsi vuole procedere lo stesso?')
        if risposta=='no':
            return
    scrivis=cartella3+'/'+bit+'b'
    scrivi = open(scrivis, "a")

    nd=int(nds)**int(ep)
    nd2=int(nds)**int(eq)
    rq=int(nds)**int(ec)
    cnd = nd
    cnd2 = nd2
    for i in range(int(numero)):
        nd = nextprime(cnd + randint(1000, int(agg) * (2**int(campo))))
        nd2 = nextprime(cnd2 + randint(1000, int(agg) * (2**int(campo))))
        n = nd * nd2
        a = n % rq
        b = n - a
        c1 = (n - a) // rq
        c3 = c1 % nd
        c4 = c1 % nd2
        if c3>10 and c4 >10:
            messagebox.showerror('Attenzione','Errore di campo')
            scrivi.close()
            return
        scrivi.write(str(n)+'\n')
    scrivi.close()
    scrivi_usb=apri_dati+':\\chiave_'+bit+'b'
    scrivi=open(scrivi_usb,'a') 
    scrivi.write(str(nds)+'\n')
    scrivi.write(str(ec)+'\n')
    scrivi.write(str(bit)+'\n')
    scrivi.close()
    messagebox.showinfo('Creazione Database','Processo terminato correttamente')   


def on_enter(event):
    b1.config(
        bg=passa_button
    )  # Cambia il colore di sfondo a blu quando il mouse entra nel pulsante


def on_leave(event):
    b1.config(bg=fondo_button)  # Ripristina il colore di sfondo


# *************************************************
# *       dimensione e colori
# *************************************************
finestra_x = 600
finestra_y = 220
finestra = str(finestra_x) + "x" + str(finestra_y)
fondo_finestra = "#528B8B"
fondo_text = "#808080"
fondo_button = "#20B2AA"
passa_button = "#C0FF3E"
fondo_button2 = "#71C671"
fondo_entry = "#C1C1C1"
# *************************************************
# *        Finestra principale
# *************************************************
root = tk.Tk()
root.title("Crea Database Semiprimi")
root.geometry(finestra)
root.config(bg=fondo_finestra)
# Creazione del canvas
px = finestra_x - 85
py = finestra_y - 85
canvas = tk.Canvas(root, width=90, height=90)
canvas.place(x=px, y=py)
px = 10
py = 10

l1=tk.Label(text='Base',bg=fondo_finestra,font='arial, 12 bold')
l1.place(x=px,y=py)
px=px+50
e1=tk.Entry(width=55,bg=fondo_button,font='arial, 12')
e1.place(x=px,y=py)

py=py+45
px=30

l2 = tk.Label(text="EC", bg=fondo_finestra, font="arial, 12 bold")
l2.place(x=px, y=py)
px = px + 30
e2 = tk.Entry(width=5, bg=fondo_button, font="arial, 12")
e2.place(x=px, y=py)

px=px+60
l3 = tk.Label(text="EP", bg=fondo_finestra, font="arial, 12 bold")
l3.place(x=px, y=py)
px = px + 30
e3 = tk.Entry(width=5, bg=fondo_button, font="arial, 12")
e3.place(x=px, y=py)

px = px + 60
l4 = tk.Label(text="EQ", bg=fondo_finestra, font="arial, 12 bold")
l4.place(x=px, y=py)
px = px + 30
e4 = tk.Entry(width=5, bg=fondo_button, font="arial, 12")
e4.place(x=px, y=py)

px = px + 70
l7 = tk.Label(text="Bit", bg=fondo_finestra, font="arial, 12 bold")
l7.place(x=px, y=py)
px = px + 30
e7 = tk.Entry(width=10, bg=fondo_button, font="arial, 12")
e7.place(x=px, y=py)

px = px + 108
l8 = tk.Label(text="Numero", bg=fondo_finestra, font="arial, 12 bold")
l8.place(x=px, y=py)
px = px + 40
e8 = tk.Entry(width=5, bg=fondo_button, font="arial, 12")
e8.place(x=px, y=py)

py=py+50
px = 10
l5 = tk.Label(text="Aggiungi", bg=fondo_finestra, font="arial, 12 bold")
l5.place(x=px, y=py)
px = px + 80
e5 = tk.Entry(width=10, bg=fondo_button, font="arial, 12")
e5.place(x=px, y=py)
px = 10
px=px+180
l6 = tk.Label(text="Campo", bg=fondo_finestra, font="arial, 12 bold")
l6.place(x=px, y=py)
px = px + 65
e6 = tk.Entry(width=10, bg=fondo_button, font="arial, 12")
e6.place(x=px, y=py)


px = 10
py = py+70

b1 = tk.Button(
    root,
    text="Esegui",
    bg=fondo_button,
    font="arial, 12 bold",
    width=10,
    cursor="hand2",
    command=esegui
)
b1.place(x=px, y=py)
b1.bind("<Enter>", on_enter)
b1.bind("<Leave>", on_leave)

px = px + 180

l2 = tk.Label(text="", width=12, bg=fondo_finestra, font="arial 14 bold")
l2.place(x=px, y=py)

testo = "Crea S."
colore = "blue"  # Colore del testo
fonte = ("arial", 10, "bold")
colore_sfondo = fondo_finestra  # Colore dello sfondo
canvas.config(bg=colore_sfondo)
canvas.create_text(45, 20, text="GC57crypto", fill="red", font=fonte)
canvas.create_text(45, 55, text=testo, fill=colore, font=fonte)


root.mainloop()
