Marzo 2024


Esteso:
La differenza tra la codifica GC57 e GC57-E sta nel fatto di poter criptare qualsiasi codifica UTF.  Dal latino, al cirillico, al cinese. Questo sono solo alcuni esempi di linguaggi che si possono criptare: 
Italiano
Codifica caratteri in questa lingua e decodifica
Afrikaans
Kodeer karakters in hierdie taal en dekodeer.
Amarico
በዚህ ቋንቋ ፊደሎችን አስቀምጥ እና ዲኮድ።
Albanese
Kodoni karakteret në këtë gjuhë dhe dekodoni.
Arabo
ترميز الأحرف في هذه اللغة وفك تشفيرها.
Assamese
এই ভাষাত বৰ্ণবোৰ এনকোড কৰক আৰু ডিকোড কৰক।
Armeno
Այս լեզվով կոդավորեք տառերը եւ վերծանեք:
Azero
Bu dildə heroqlifləri kodla və dekod et.
Cecko
Kódujte znaky v tomto jazyce a dekódujte.
Bulgaro
Кодиране на знаци на този език и декодиране.
Giapponese
この言語で文字をエンコードし、デコードします。
Curdo
لە ناو ئەم زمانەدا هێما و کۆدەکان بکە.
Russo
Кодируйте символы на этом языке и декодируйте
Finlandese
Koodaa merkit tällä kielellä ja pura.
viestnamita
Mã hóa các ký tự trong ngôn ngữ này và giải mã.
Polacco
Zakoduj znaki w tym języku i zdekoduj.
Coreano
이 언어로 문자를 인코딩하고 디코딩합니다.
Cinese semplificato
用这种语言对字符进行编码和解码。
Ucraino
Кодуйте символи на цій мові та декодуйте.
Cinese Classico
用這種語言對字元進行編碼和解碼。
Ebraico
קידוד תווים בשפה זו ופענוח.

Per poter fare questo ho dovuto cambiare alcune cose:

1) la codifica di scostamento avviene su cifre di 5 e non più su 3.
2) le regole di scostamento sono aumentate e vengono determinate dal fattore primo p

Ecco un esempio di queste regole:

            x = int(divln[cont])
            seed(x)
            m1=randint(10000,30000)
            x = x + m1 + ord(te[i])
            tcript=tcript+str(x)

Il fattore primo p viene sempre diviso in pacchetti di 2 ma ogni pacchetto innesca un valore random Seed(x) da 10.000 a 30.000 che poi viene aggiunto al valore asci del carattere a cui viene aggiunto anche il valore del pacchetto.

3) i file binari vengono portati da 11 a 17 per coprire tutti i valori che vanno da 32 a 99.999 e poi vengono xorati come nella codifica GC57.

In questo modo si può criptare qualsiasi lingua che abbia un valore asci non superiore a 60.000 il ché vuol dire la maggior parte delle lingue esistenti.

