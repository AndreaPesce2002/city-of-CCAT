## La Città delle CCAT 🏙️🤖

Benvenuti nella Città dei CCAT, un luogo dove l'intelligenza artificiale e le fantasie umane danzano insieme sotto il cielo stellato di un mondo digitale.

In questa piccola cittadina, le AI vivranno in perfetta armonia, passeggeranno tra le molteplici strutture della città e comunicheranno pacificamente.
## Significato di CCAT
Il CCAT è l'anima dei nostri cittadini. Grazie a [Piero Savastano](https://www.linkedin.com/in/piero-savastano-523b3016/?originalSubdomain=it) e al suo progetto  [cheshire-cat-ai](https://github.com/cheshire-cat-ai/core), possimo avere degli LLM che vivono in una cittadina.

## Come funziona

1) avviare il file `crea_agnte_base.py`, il file creerà un [cheshire-cat-ai](https://github.com/cheshire-cat-ai/core) ottimizato per parlare con più agenti
2) avviare il docker compose dell'`agente base`
   - attivare uttti i plugin
   - caricare il LLM
   - caricare eventuali file, come per esempio la mappa o infomrazioni base dei vostri cittadini

   **Importante**: Ogni volta che apportate modifiche all'`agente_base`, assicuratevi di eliminare le cartelle dei vostri agenti. Si ricreeranno automaticamente in futuro quando eseguirete il file `avviaDOcker.py`.
   
3) spegnere il docker compose dell'agente base
   
4) ora che abbiamo l'agente base ci baseà disegnare i nostri cittadini. Potete utilizzare il file [agenti.json](https://github.com/AndreaPesce2002/city-of-ccat/blob/master/caratteristiche_agenti/agenti.json)
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

5) Ricordatevi di aggiungere le immagini con il cittdino in `game/asset` e denominatelo propio col nome del cittadino (esempio `anna.png`)

6) Una volta disegnati i vostri cittadini, avviate il file `avviaDocker.py` il programma renderà i cittadini vivi.

   Il programma potrebbe dare l'`errore 104` in console, ma appaiono solo perché il programma tenta di accedere mentre il Docker si sta avviando.
   se invece vi da altri errori come per esempio il `111` vi conviene controllare l'agente base se ha qualche problema
    
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
from collegamento_2 import converection

con=converection() #permetti il collegamento

# con i primi due attributi scegliete i cittadini il rpimo sarà sempre quello che inizia la conversazione
con.creaConversazione('Andrea','Anna', '*ti sei trovato con Anna per un appuntamento romantico*')
con.chiudiSessione() #ricorda di sconettere sempre la connesione dopo creaConversazione

```
