## La Città delle CCAT 🏙️🤖

Benvenuti nella Città dei CCAT, un luogo dove l'intelligenza artificiale e le fantasie umane danzano insieme sotto il cielo stellato di un mondo digitale.

In questa piccola cittadina, le AI vivranno in perfetta armonia, passeggeranno tra le molteplici strutture della città e comunicheranno pacificamente.
## Significato di CCAT
iIl CCAT è l'anima dei nostri cittadini. Grazie a [Piero Savastano](https://www.linkedin.com/in/piero-savastano-523b3016/?originalSubdomain=it) e al suo progetto  [cheshire-cat-ai](https://github.com/cheshire-cat-ai/core), sono riuscito a dare vita a una vera e propria civiltà.

## Come funziona

Idealmente, tutto dovrebbe essere già pronto con 3 cittadini pronti all'uso. Tuttavia, nel caso vogliate modificare o aggiungere nuovi cittadini, i passaggi sono i seguenti:

- Iniziate caricando il cheshire-cat-ai e denominatelo `agente_base`, Quest'ultimo avrà tutte le caratteristiche di base di ogni abitante. L'attuale è modificato appositamente per lo scopo, quindi consiglio di utilizzare quello attuale o copiare le modifiche per una migliore efficacia.

    Una volta caricato, avviate il cheshire-cat-ai e inserite il LLM (consigliabile utilizzarne uno gratuito). Poi caricate alcune informazioni di base che volete che gli abitanti abbiano, come una mappa del luogo o dei file necessari.

    **Importante**: Ogni volta che apportate modifiche all'`agente_base`, assicuratevi di eliminare le cartelle dei vostri agenti. Si ricreeranno automaticamente in futuro quando eseguirete il file `avviaDOcker.py`.

- Il secondo passo è generare numerosi cheshire-cat e dare ad ognuno la propria personalità. Potete utilizzare il file [agenti.json](https://github.com/AndreaPesce2002/city-of-ccat/blob/master/caratteristiche_agenti/agenti.json)
  ```json
  {
    "Anna":{
        "port":1866,
        "impostazioni":{
            "prompt_prefix": "sei un giovane ragazza di nome Anna di 25 anni, sei molto intelligente e curiosa, vivi in una piccola cittadina di campagna e sei felice di vivere li, lavori nel negozio dei tuoi genitori ma stai studiando per andare all'università",
            "max_caratteri": 250,
            "episodic_memory_k": 3,
            "episodic_memory_threshold": 0.7,
            "declarative_memory_k": 3,
            "declarative_memory_threshold": 0.7,
            "procedural_memory_k": 3,
            "procedural_memory_threshold": 0.7,
            "user_name": "Andrea",
            "language": "italiano"
        }
    }
  }
  ```
  Le informazioni importanti sono:
    - **il nome**: deve essere sempre diverso per identificare ogni singolo abitante come un ID
    - **la posrta**: deve essere sempre diversa tra un abitante e l'altro per consentire al CCAT di agire
    - **il prompt_prefix**: è la descrizione di base dell'abitante, fornendo una personalità base valida per ogni dialogo.

  Se lo desiderate, potete aggiungere dei file di testo con ulteriori descrizioni del cittadino all'interno di `caratteristica_agenti`.

- Ricordatevi di aggiungere le immagini con il personaggio in `game/asset`

- Una volta aggiunti i vostri cittadini, avviate il file `avviaDOcker.py`.

    Il programma potrebbe dare degli errori in console, ma appaiono solo perché il programma tenta di accedere mentre il Docker si sta avviando. 
    
    **Attenzione:** più cittadini ci sono, più tempo ci metterà ad avviare tutti i cittadini.

## Avvio del vilaggio

Ora che i nostri cittadini sono pronti, basta solo spedirli nel meraviglioso villaggio. Ecco i passaggi:

- Prima di tutto, verificate di avere una mappa in `game/asset` denominata `map.png` e create dei punti dove i cittadini possono andare con `punti_mappa.json`, Ecco un esempio:
```json
    "strada casa Andrea e negozio": {
        "pos": [500, 128],
        "collegati": [
            "casa di Andrea",
            "incrocio",
            "strada davanti casa Anna",
            "negozio"
        ]
    }
```
- Avviate il file `game/game.py`. Quest'ultimo aprirà una finestra `pygame` e i vostri cittadini inizieranno a girare e a conversare tra di loro.

## Conversazione di circostanza

I cittadini non sono obbligati a parlare e viaggiare all'interno del villaggio se non lo desiderate. Utilizzando la classe `converection` che si trova in `collegamento_2.py`, potete far parlare i vostri cittadini con il seguente codice:

```python
con=converection() #permetti il collegamento

# con i primi due attributi scegliete i cittadini il rpimo sarà sempre quello che inizia la conversazione
con.creaConversazione('Andrea','Anna', '*ti sei trovato con Anna per un appuntamento romantico*')
con.chiudiSessione() #ricorda di sconettere sempre la connesione dopo creaConversazione

```
