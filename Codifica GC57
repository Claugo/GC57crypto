La codifica GC57 comprende una serie di operazione al fine di nascondere in modo sicuro il messaggio che verrà criptato.

Il processo viene eseguito in due fasi:

PRIMA FASE:

 1)   Fattorizzazione del numero con l'algoritmo GC57: Ottenere due fattori primi molto grandi da questo processo, che chiameremo p e q.
 

2)   Trasformazione di p in una lista di pacchetti di due cifre: Ogni cifra di p viene divisa in pacchetti di due cifre.


 3)   Trasformazione del testo in codice ASCII UTF-8: Il testo da codificare viene trasformato in codice ASCII UTF-8.


 4)   Creazione di variabili m1, m2, m3, m4, m5: Cinque variabili composte da numeri a tre cifre selezionate casualmente da 100 a 400.


 5)   Selezione casuale di una posizione di partenza per la codifica: Questa posizione determina da quale pacchetto di due cifre iniziare ad estrarre i pacchetti.


 6)   Codifica del testo: Ogni carattere del testo viene codificato in base alle regole riportate sotto:

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


Naturalmente questo schema può essere reso più complicato o distribuito in modo diverso per ogni programma
 

SECONDA FASE:

1)    Estrazione di due serie di numeri dal fattore primo q: Le serie vengono divise in pacchetti di tre cifre.

2)    Gestione automatica della lunghezza del fattore primo q: Le serie vengono create automaticamente in base alla lunghezza di q.


3)    Scelta casuale di due tipi di partenza per le serie: Queste due serie vengono create a partire da due numeri di partenza selezionati casualmente.


4)    Trasformazione dei pacchetti in binario a 11 bit: Ogni pacchetto di tre cifre viene trasformato in un numero binario a 11 bit.


5)   Esecuzione di uno XOR tra le due serie binarie: Ottenendo così un'altra lista binaria che è il risultato di questa operazione.


6)    Trasformazione della lista di codifica del testo in binario a 11 bit: Ogni pacchetto di tre cifre della lista di codifica del testo viene trasformato in un numero binario a 11 bit.


7)    Esecuzione di uno XOR tra la lista binaria del testo e la lista ottenuta dall'operazione XOR precedente: Ciò produce una serie di caratteri indecifrabili.


8)    Salvataggio dei caratteri indecifrabili in un file con il semiprimo: Questi caratteri indecifrabili vengono salvati in un file insieme al semiprimo utilizzato per la codifica, con il metodo Pickle(python)


Il file spedito al destinatario verrà poi caricato dal programma per eseguire il processo al contrario e visualizzare il messaggio in chiaro.


La sicurezza della criptazione è sempre basata sulla difficoltà di fattorizzazione di un semiprimo molto grande. I passaggi elaborati per nascondere il messaggio sono in parte randomizzati e in parte mescolati. Questo processo rende molto complicato o impossibile risalire al testo originale se non si conoscono i fattori primi che lo hanno creato

