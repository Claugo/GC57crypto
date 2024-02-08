L’algoritmo che tratterrò in questa presentazione l’ho chiamato GC57.  Quello che cercherò di descrivere in questa presentazione sarà la sua grande versatilità nel creare nuove chiavi, la velocità con cui li crea, e la loro sicurezza.


Creazione delle Chiavi

Inserimento di un fattore primo abbastanza grande, 30-40 cifre, elevato alla potenza per raggiungere i bit richiesti. Nell’esempio che io porterò, il fattore primo è di 34 cifre che elevato alla potenza di 116 porterà ad avere un semiprimo di 13076 bit.
L’algoritmo si preoccuperà di creare una chiave e di definire un campo dove potrà fattorizzare a tempo zero  
La chiave per fattorizzare questi seniprimi sarà del fattore primo inserito elevato alla 58, cioè alla metà della potenza intera. Mentre i due fattori primi saranno ricercati a partire da da due basi, e cioè fattore primo inserito elevato alla 56 e fattore primo inserito elevato alla 60. Da notare che le due elevazioni sono pari a 116.
Il campo dove l’algoritmo cercherà i fattori primi varia a seconda della distanza tra le due potenze e anche del fattore primo inserito. Per dare una idea, con più è piccolo il fattore primo inserito, con più dovrà essere maggiore la distanza tra i due esponenti, al contrario con più è grande ll fattore primo inserito con più la distanza tra i due esponenti si assotiglia, fino ad arrivare a una quota minima di sicurezza di 4, come è nell’esempio.

Riporto l’esempio pratico di questo caso. 

    • Il fattore primo inserito 6366805760909027985741435139224233
    • i bit richiesti 13000 che si sono tradotti in 13076
    • la chiave generata 6366805760909027985741435139224233^58
    • i due fattori primi per generare il semiprimo di 13076 bit sono rispettivamente:
            nextprime(6366805760909027985741435139224233^56+randint(10000,1000000*2^200)
            nextprime(6366805760909027985741435139224233^60+randint(10000,1000000*2^200)
    • Il programma comincerà a selezionare i fattori primi all’interno di quel campo e li moltiplicherà tra di loro per creare i semiprimi a 13076 bit, che poi li memorizzerà in un file chiamato 13000b







Funzionamento del programma



Tipo di codifica Usata:

    • Codifica AES: Utilizza l'algoritmo Advanced Encryption Standard (AES), ampiamente riconosciuto per la sua sicurezza e affidabilità, per la codifica dei messaggi. La combinazione di chiavi a 6000 bit e AES garantisce una protezione robusta dei dati.
    • Crittografia Asimmetrica con Fattorizzazione dei Semiprimi: Il programma sfrutta un approccio ibrido che combina crittografia asimmetrica e simmetrica. Le chiavi AES uniche per ogni messaggio vengono generate utilizzando un semiprimo e una chiave pubblica predefinita, garantendo un elevato livello di sicurezza.

Il programma scritto in Python si presenta con una interfaccia grafica con la possibilità di scrivere il messaggio e inviarlo criptato al destinatario.

Un secondo programma si occuperà di decodificarlo ad avvenuta consegna del messaggio e di stampare il messaggio decodificato a video

Le librerie caricate dal programma per criptare il messaggio sono:
from Crypto.Cipher import AES 
from Crypto.Hash import SHA256

All’apertura il programma si occuperà di recuperare la chiave di fattorizzazione da una chiavetta USB, e di caricarla in memoria. Come seconda operazione caricherà un semiprimo dal file 13000b in modo random per essere fattorizzato con l’algoritmo GC57. La funzione di fattorizzazione la riporto qui sotto per mostrare meglio il suo procedimento. 

def factorize(semiprime):
    a = semiprime % chiave
    b = semiprime - a
    for i in range(10):  # Effettua fino a 10 tentativi di fattorizzazione
        key = gcd(a, b)  # Calcola il massimo comune divisore tra due numeri
        if key != 1:  # Se il massimo comune divisore è diverso da 1, è stata trovata una fattorizzazione
            break
        a = a + chiave  # Aggiorna i valori di 'a' e 'b' per il prossimo tentativo
        b = b - chiave
    return key

Il processo di fattorizzazione è a tempo zero. Le 10 iterazioni sono solo una sicurezza che si trova anche all’interno del programma di creazione dei semiprimi. Sono le iterazione massime che può fare per risolvere la fattorizzazione, se no, il campo viene abbassato

La fattorizzazione avviene a tempo zero e con questo viene creata la chiave (Fattore primo di 6000 bit) che darà accesso agli algoritmi di sicurezza riportati sopra

Si procederà poi a scrivere il messaggio e che nell’istante in cui si preme invia… questo verrà codificato e salvato in un file e spedito.

Programma di decodifica 

Il programma di decodifica non necessiterà di caricare il semiprimo, in quanto questo è stato inserito dentro il messaggio. L’unica cosa che dovrà fare è caricare da USB la chiave e fattorizzare il semiprimo situato all’interno del messaggio estraendo la chiave(fattore primo da 6000 bit) per avviare il ciclo di decodificazione
