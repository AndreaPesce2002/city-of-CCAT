import json
import time
import cheshire_cat_api as ccat

# Definiamo delle variabili di stato per controllare il flusso della conversazione
conversazioneInAtto = False

# Funzione per creare una funzione on_open personalizzata per ogni client
def create_on_open(client_name):
    def on_open():
        print(f"Connessione aperta per {client_name}!")
    return on_open

# Funzione per creare una funzione on_message personalizzata per ogni client
def create_on_message(client_name):
    def on_message(message: str):
        global conversazioneInAtto
        try:
            # Decodifichiamo il messaggio JSON ricevuto
            message_data = json.loads(message)

            # Controlliamo se il messaggio è di tipo 'chat'
            if message_data.get('type') == 'chat':
                if '§' not in message_data.get('content'):
                    # Prendiamo il contenuto del messaggio e lo inviamo all'altro client
                    print(f"{client_name}: {message_data.get('content')}")
                    if client_name == "Anna":
                        Andrea.send(message=message_data.get('content'))
                    elif client_name == "Andrea":
                        Anna.send(message=message_data.get('content'))
                else:
                    print('fine conversazione')
                    conversazioneInAtto=False
                    
        except json.JSONDecodeError:
            print(f"Il messaggio ricevuto da {client_name} non è un JSON valido.")
            conversazioneInAtto=False
    return on_message

def on_error(exception: Exception):
    print(str(exception))

# Per la funzione on_close, puoi fare qualcosa di simile:
def create_on_close(client_name):
    def on_close(status_code: int, message: str):
        print(f"Connessione chiusa per {client_name} con codice {status_code}: {message}")
    return on_close
    
# Connection settings with default values
Anna_config = ccat.Config(
    base_url="localhost",
    port=1866,
    user_id="user",
    auth_key="",
    secure_connection=False
)

# Quando crei i client, usa le funzioni create_on_open e create_on_close
Anna = ccat.CatClient(
    config=Anna_config,
    on_open=create_on_open("Anna"),
    on_close=create_on_close("Anna"),
    on_message=create_on_message("Anna"),
    on_error=on_error
)

# Connection settings with default values
Andrea_config = ccat.Config(
    base_url="localhost",
    port=1867,
    user_id="user",
    auth_key="",
    secure_connection=False
)

Andrea = ccat.CatClient(
    config=Andrea_config,
    on_open=create_on_open("Andrea"),
    on_close=create_on_close("Andrea"),
    on_message=create_on_message("Andrea"),
    on_error=on_error
)

# Connessione dei client al WebSocket API
Anna.connect_ws()
Andrea.connect_ws()

# Attendiamo che entrambi i client siano connessi
while not Anna.is_ws_connected or not Andrea.is_ws_connected:
    time.sleep(1)

# Anna invia il primo messaggio e aspetta una risposta
Anna.send(message="Ciao Anna!")
conversazioneInAtto = True

# Manteniamo la connessione aperta finché non decidiamo di chiuderla
# Questo è solo un placeholder; dovrai implementare una logica di terminazione
while conversazioneInAtto:
    time.sleep(1)

# Chiusura delle connessioni
Anna.close()
Andrea.close()