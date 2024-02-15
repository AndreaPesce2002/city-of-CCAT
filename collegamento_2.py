import json
import os
import time
import cheshire_cat_api as ccat

class converection:
    def __init__(self) -> None:
        self.conversazioneInAtto = False
        self.coppia_conversante = ("Anna", "Andrea")
        self.fine_conversazione = {agente: False for agente in self.coppia_conversante}
        self.personaggi={}
        
        self.posti = ['campo di Andrea', 'casa di Luca', 'casa di Anna','casa di Andrea','negozio', 'piazza', 'spiaggia']
        
    def crea_messaggio(self):
        messaggio = "-dove vuoi andare?\n"
        for indice, luogo in enumerate(self.posti, start=1):
            messaggio += f" {indice}) {luogo}\n"
        messaggio += "- per quanto tempo vuoi stare lì [tempo in secondi]\n\nusa la forma:\n    -posizione: XXX\n    -tempo: XXX"
        return messaggio

    def evoAgenti(self, agente1,agente2):
        agenti={}
        # Primo, leggiamo il contenuto del file agenti.json
        with open('caratteristiche_agenti/agenti.json', 'r') as file:
            agenti_data = json.load(file)

        # Adesso iteriamo sul dizionario agenti_data per creare ogni agente
        for nome_agente, dettagli in agenti_data.items():
            if nome_agente==agente1 or nome_agente==agente2:

                # Configuriamo le impostazioni per ogni agente basate sui valori del JSON
                config = ccat.Config(
                    base_url="localhost",
                    port=dettagli['port'],
                    user_id=agente2 if agente1==nome_agente else agente1,
                    auth_key="",
                    secure_connection=False  # o True se necessario
                )

                # Creiamo l'istanza dell'agente
                agente = ccat.CatClient(
                    config=config,
                    on_open=self.create_on_open(nome_agente),
                    on_close=self.create_on_close(nome_agente),
                    on_message=self.create_on_message(nome_agente),
                    # Potresti voler gestire gli errori in maniera personalizzata
                    on_error=lambda exception: print(str(exception))
                )

                # Salviamo l'istanza nell'elenco degli agenti
                agenti[nome_agente] = agente

        #connetimo gli ageti
        tutti_connessi = False
        while not tutti_connessi:
            for nome_agente, agente in agenti.items():
                agente.connect_ws()
                time.sleep(2)
            tutti_connessi = all(agente.is_ws_connected for agente in agenti.values())
            if not tutti_connessi:
                print("Attendiamo che tutti gli agenti siano pronti... 🕰️")
                time.sleep(1)  # Aspetta un secondo prima di controllare di nuovo

        print("Tutti gli agenti sono connessi! La conversazione può iniziare. 🎉")

        return agenti

    def creaConversazione(self,agente1,agente2, scenario):
        self.agenti=self.evoAgenti(agente1,agente2)
        self.coppia_conversante = (agente1, agente2)
        self.fine_conversazione = {agente: False for agente in self.coppia_conversante}
        self.cambia_interlocutore(self.coppia_conversante[0], self.coppia_conversante[1])
        self.cambia_interlocutore(self.coppia_conversante[1], self.coppia_conversante[0])

        # Anna invia il primo messaggio e aspetta una risposta
        self.conversazioneInAtto = True
        self.agenti[self.coppia_conversante[0]].send(message=scenario)

        # Manteniamo la connessione aperta finché non decidiamo di chiuderla
        # Questo è solo un placeholder; dovrai implementare una logica di terminazione
        while self.conversazioneInAtto:
            time.sleep(1)

    def cambia_interlocutore(self,nome_agente, nuovo_interlocutore):

        # Il percorso al file settings.json ora include il nome dell'agente
        path_to_settings = f"agenti/{nome_agente}/core/cat/plugins/cat_advanced_tools/settings.json"

        # Verifichiamo se il file settings.json esiste nel percorso specificato
        if os.path.exists(path_to_settings):
            # Apriamo il file settings.json in modalità lettura
            with open(path_to_settings, "r") as file:
                # Carichiamo il contenuto del file in un dizionario
                settings = json.load(file)

            # Modifichiamo il 'user_name' con il nome del nuovo interlocutore
            settings["user_name"] = nuovo_interlocutore

            # Apriamo il file settings.json in modalità scrittura
            with open(path_to_settings, "w") as file:
                # Scriviamo il dizionario aggiornato nel file
                json.dump(settings, file, indent=4, ensure_ascii=False)

            #cambiare user_id
            #self.agenti[nome_agente]._conn_settings.user_id = nuovo_interlocutore

        else:
            print("Oh no! Il file settings.json non esiste nel percorso indicato. Assicurati che il percorso sia corretto, o che il file non sia stato nascosto da qualche scherzo del destino! 🕵️‍♂️🎩")


    # Funzione per creare una funzione on_open personalizzata per ogni client
    def create_on_open(self,client_name):
        def on_open():
            print(f"Connessione aperta per {client_name}!")
        return on_open

    # Funzione per creare una funzione on_message personalizzata per ogni client
    def create_on_message(self,client_name,):
        def on_message(message: str):
            try:
                # Decodifichiamo il messaggio JSON ricevuto
                message_data = json.loads(message)

                # Controlliamo se il messaggio è di tipo 'chat'
                if message_data.get('type') == 'chat':
                    contenuto_messaggio = message_data.get('content')
                    print(f"{client_name}: {contenuto_messaggio}")
                    destinatario = self.coppia_conversante[1] if client_name == self.coppia_conversante[0] else self.coppia_conversante[0]
                    
                    if self.coppia_conversante[0]==self.coppia_conversante[1]:
                        
                        
                        # Innanzitutto, controlliamo se il messaggio contiene le parole chiave desiderate
                        contiene_posizione = '-posizione:' in contenuto_messaggio
                        contiene_tempo = '-tempo:' in contenuto_messaggio

                        if contiene_posizione and contiene_tempo:
                            # Estraiamo la destinazione desiderata dal messaggio
                            destinazioneDesiderata = contenuto_messaggio.split('-posizione: ')[1].split('\n')[0]
                            
                            # Estraiamo il tempo di attesa dal messaggio
                            tempo_di_attesa = float(contenuto_messaggio.split('-tempo: ')[1].split('\n')[0])/100
                            
                            # Ora, verifichiamo se la posizione desiderata è tra i posti possibili
                            if destinazioneDesiderata not in self.posti:
                                # Se la posizione desiderata non esiste, inviamo un messaggio di errore all'utente
                                self.agenti[destinatario].send(message=f"""mi spiace ma questo posto non esiste ecco i posti possibili: 
                                                                        {', '.join(self.posti)} 
                                                                        
                                                                        usa la forma:
                                                                                -posizione: XXX
                                                                                -tempo: XXX
                                                                        """)
                            else:
                                # Impostiamo il tempo di attesa nel personaggio
                                self.personaggi[client_name].tempo_di_attesa = tempo_di_attesa
                                
                                # Impostiamo la destinazione nel personaggio
                                self.personaggi[client_name].imposta_destinazione(destinazioneDesiderata)

                        else:
                            # Se la posizione esiste, possiamo procedere con la logica successiva...
                            self.agenti[destinatario].send(message=f"""mi spiace ma la risposta non è coretta ecco i posti possibili: 
                                                                    {', '.join(self.posti)} 
                                                                    
                                                                    usa la forma:
                                                                            -posizione: XXX
                                                                            -tempo: XXX
                                                                    """)

                        # Dopo aver gestito la logica per la posizione e il tempo, impostiamo conversazioneInAtto su False
                        self.conversazioneInAtto = False
                        
                        
                    else:

                        # Se tutti gli agenti nella conversazione hanno inviato il segnale di fine
                        if all(self.fine_conversazione.values()):
                            print('Tutti gli agenti hanno segnato la fine della conversazione')
                            self.conversazioneInAtto = False
                        else:
                            # Se il messaggio contiene il segnale di fine conversazione
                            if '§' in contenuto_messaggio:
                                self.fine_conversazione[client_name] = True
                                #contenuto_messaggio = contenuto_messaggio.replace('§', '').strip()

                            # Determiniamo l'agente destinatario basandoci sulla coppia_conversante
                            self.agenti[destinatario].send(message=contenuto_messaggio)


            except json.JSONDecodeError:
                print(f"Il messaggio ricevuto da {client_name} non è un JSON valido.")
                self.conversazioneInAtto = False
        return on_message

    def on_error(exception: Exception):
        print(str(exception))

    # Per la funzione on_close, puoi fare qualcosa di simile:
    def create_on_close(self,client_name):
        def on_close(status_code: int, message: str):
            print(f"Connessione chiusa per {client_name} con codice {status_code}: {message}")
        return on_close

    def chiudiSessione(self):
        # Chiusura delle connessioni
        for nome_agente, agente in self.agenti.items():
            agente.close()


#utilizzo
# con=converection()
# conversazione = con.crea_messaggio()
# con.creaConversazione('Andrea','Andrea',conversazione)
# con.chiudiSessione()

# print(f"Posizione: {con.posizioneDesiderata}, Tempo: {con.tempo}")




# con.creaConversazione('Luca','Anna', '*ti sei trovato con Anna per discutere di Andrea*')
# con.chiudiSessione()
