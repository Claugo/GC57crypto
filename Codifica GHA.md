Codifica Ibrida
La codifica ibrida comprende 3 algoritmi, GC57, HSA, AES.
Per tenere la fattorizzazione a tempo zero per il GC57 ho pensato di creare dei file contenenti i una quantità finita di semiprimi divisi per bit. Questo perché creare un semiprimo significa trovare due fattori primi di una certa dimensione e questo comporta un tempo che può superare i due minuti. 
Per esempio, questo file 13076b contiene 10 semiprimi da 13076 bit il che vuol dire fattori primi che vanno da 6000 bit a 7000 bit. Naturalmente posso inserire in questo file quanti semiprimi voglio, che siano 10 o 1000 è uguale, l'unica cosa che cambia è il tempo per crearlo che potrebbe superare anche il giorno di lavoro. 
Creato il file non mi devo più preoccupare del tempo per codificare e decodificare il messaggio.
Qui riporto alcuni esempi di file creati: 12072b, 10068b, 8379b

Quando il programma va in esecuzione chiede quale codifica intendiamo usare e carica in modo random un semiprimo all'interno del file che abbiamo selezionato. 

La chiave di fattorizzazione del GC57 si trova su una usb assieme a tutte le chiavi abbinate ai file dei semiprimi.

Caricato il semiprimo, carica la chiave con la quale il GC57 fattorizzerà il semiprimo a tempo zero. Il fattore primo che verrà trovato sarà passato all'algoritmo SHA che ne rileverà l'impronta digitale per poi passarla all'algoritmo AES per creare la chiave di criptazione con la quale sarà poi codificato il messaggio.

Il messaggio codificato e il semiprimo verranno poi memorizzati su un file criptato con Pikle (Python) pronto per essere spedito al destinatario.

Il destinatario non dovrà fare altro che caricare il messaggio che verrà poi diviso in due parti, semiprimo e messaggio criptato, e si procederà al contrario per avere di nuovo il messaggio in chiaro.

Naturalmente anche il destinatario dovrà avere su una usb tutte le chiavi necessarie per la fattorizzazione, nel caso il destinatario possedesse solo alcune di quelle chiavi, potrà decodificare solo i messaggi che saranno codificati con le chiavi in suo possesso.

Questo metodo è altamente competitivo con i metodi in circolazione. 
Innanzi tutto richiede la fattorizzazione di un grande semiprimo, e secondo, il sistema SHA e AES sono altamente riconosciuti per la loro difficoltà nel svelare le chiavi di criptazione. Inoltre è molto veloce nella codifica e decodifica del messaggio perché utilizza la chiave simmetrica.
