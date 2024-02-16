# Primo, leggiamo il contenuto del file agenti.json
import json
import os
import shutil
import subprocess
import time
import requests
import yaml

import cheshire_cat_api as ccat


with open('caratteristiche_agenti/agenti.json', 'r') as file:
    agenti_data = json.load(file)

# Creiamo un dizionario per tenere traccia dei nostri agenti creati
agenti = {}
nuovo=False

percorso_base_agenti = "agenti"
percorso_cartella_agente_base = os.path.join(percorso_base_agenti, "agente_base")

for nome_agente, dettagli in agenti_data.items():
    
    # Costruiamo il percorso della cartella specifica per l'agente
    percorso_cartella_agente = os.path.join(percorso_base_agenti, nome_agente)

    # Controlliamo se la cartella esiste
    if not os.path.exists(percorso_cartella_agente):
        nuovo=True
        # Se la cartella non esiste, la creiamo copiando quella di agente_base
        shutil.copytree(percorso_cartella_agente_base, percorso_cartella_agente)
        print(f"Creata la cartella per l'agente {nome_agente}, copiando da agente_base.")
    
    # Costruiamo il percorso del file docker-compose.yml all'interno della cartella
    percorso_docker_compose = os.path.join(percorso_cartella_agente, 'docker-compose.yml')

    # Carichiamo il contenuto del file docker-compose.yml
    with open(percorso_docker_compose, 'r') as file:
        docker_compose_content = yaml.safe_load(file)

    # Modifichiamo il contenuto come necessario
    docker_compose_content['services']['cheshire-cat-core']['container_name'] = f"cheshire_cat_core_{nome_agente}"
    docker_compose_content['services']['cheshire-cat-core']['environment'][3] = f"CORE_PORT={dettagli['port']}"
    docker_compose_content['services']['cheshire-cat-core']['ports'][0] = f"{dettagli['port']}:80"

    # Salviamo il file modificato
    with open(percorso_docker_compose, 'w') as file:
        yaml.safe_dump(docker_compose_content, file)
        
        percorso_settings_json = os.path.join(percorso_cartella_agente, "core", "cat", "plugins", "cat_advanced_tools", "settings.json")
    
    # Controlliamo se il file settings.json esiste
    if os.path.exists(percorso_settings_json) and os.path.isfile(percorso_settings_json):
        # Carichiamo il contenuto del file settings.json
        with open(percorso_settings_json, 'r') as file:
            settings_content = json.load(file)

        # Modifichiamo il contenuto con i dettagli dell'agente
        settings_content['user_name'] = nome_agente
        settings_content.update(dettagli['impostazioni'])

        # Salviamo il file modificato
        with open(percorso_settings_json, 'w') as file:
            json.dump(settings_content, file, indent=4)

        print(f"Il file settings.json per l'agente {nome_agente} è stato aggiornato con successo! 🐱‍💻✨")
    else:
        print(f"Il file settings.json per l'agente {nome_agente} non esiste.")

    # Ora che il file è stato modificato, possiamo avviare il docker-compose
    try:
        result = subprocess.run(["docker-compose", "up","--build","-d"], cwd=percorso_cartella_agente, check=True)
        if result.returncode == 0:
            print(f"Ho avviato il docker-compose per l'agente {nome_agente} con le nuove modifiche! 🐱‍👓✨")          
        else:
            print(f"Errore: docker-compose up ha restituito un codice di uscita non zero.")
    except subprocess.CalledProcessError as e:
        print(f"Qualcosa è andato storto nell'avvio di docker-compose per l'agente {nome_agente}: {e}")
        
    #nuovo=False #temporaneo
    if nuovo:
        
        def on_open():
            # This is triggered when the connection is opened
            print("Connection opened!")

        def on_message(message: str):
            # This is triggered when a new message arrives
            # and grabs the message
            print(message)

        def on_error(exception: Exception):
            # This is triggered when a WebSocket error is raised
            print(str(exception))

        def on_close(status_code: int, message: str):
            # This is triggered when the connection is closed
            print(f"Connection closed with code {status_code}: {message}")
            
            
        # Configuriamo le impostazioni per ogni agente basate sui valori del JSON
        config = ccat.Config(
            base_url="localhost",
            port=dettagli['port'],
            user_id="conscenza",
            auth_key="",
            secure_connection=False  # o True se necessario
        )

        # Creiamo l'istanza dell'agente
        agente = ccat.CatClient(
            config=config,
            on_open=on_open,
            on_close=on_close,
            on_message=on_message,
            on_error=on_error
        )
        
        connsesso=False
        while not connsesso:
            agente.connect_ws()
            time.sleep(3)
            connsesso = agente.is_ws_connected

        print("L'agente è conesso")

    
        #carica file
        # Troviamo il file di caratteristiche specifico per l'agente
        percorso_file_caratteristiche = os.path.join("caratteristiche_agenti", f"{nome_agente}.txt")

        # Impostiamo l'URL e la porta del server del Cheshire Cat
        url = f'http://localhost:{dettagli["port"]}/rabbithole/'

        # Prepariamo il file da inviare senza impostare Content-Type manualmente
        file_data = {
            'file': (os.path.basename(percorso_file_caratteristiche), open(percorso_file_caratteristiche, 'rb'), 'text/plain'),
            'chunk_size': (None, '400'),
            'chunk_overlap': (None, '100')
        }

        # Effettuiamo la richiesta POST al server utilizzando la libreria requests
        response = requests.post(url, files=file_data)

        # Controlliamo la risposta
        if response.status_code == 200:
            print("Il file è stato caricato con successo nel Rabbit Hole.")
        else:
            print(f"Errore durante il caricamento del file: {response.status_code} - {response.text}")

        # Chiudiamo il file per evitare perdite di risorse
        file_data['file'][1].close()

        # Ricordati di chiudere anche l'agente se non lo userai più
        agente.close()