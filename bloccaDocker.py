# Primo, leggiamo il contenuto del file agenti.json
import json
import os
import subprocess


with open('caratteristiche_agenti/agenti.json', 'r') as file:
    agenti_data = json.load(file)

# Creiamo un dizionario per tenere traccia dei nostri agenti creati
agenti = {}

percorso_base_agenti = "agenti"
for nome_agente, dettagli in agenti_data.items():
    
    # Costruiamo il percorso della cartella specifica per l'agente
    percorso_cartella_agente = os.path.join(percorso_base_agenti, nome_agente)

    # Controlliamo se la cartella esiste
    if os.path.exists(percorso_cartella_agente) and os.path.isdir(percorso_cartella_agente):
        # Costruiamo il percorso del file docker-compose.yml all'interno della cartella
        percorso_docker_compose = os.path.join(percorso_cartella_agente, 'docker-compose.yml')

        # Verifichiamo se il file docker-compose.yml esiste
        if os.path.exists(percorso_docker_compose) and os.path.isfile(percorso_docker_compose):
            # Se il file esiste, eseguiamo il comando per rimuovere i container specifici con docker-compose rm
            try:
                subprocess.run(["docker-compose", "down"], cwd=percorso_cartella_agente, check=True)
                subprocess.run(["docker-compose", "rm", "-f"], cwd=percorso_cartella_agente, check=True)
                print(f"Ho rimosso i container per l'agente {nome_agente}! 🗑️✨")
            except subprocess.CalledProcessError as e:
                print(f"Qualcosa è andato storto nella rimozione dei container per l'agente {nome_agente}: {e}")
        else:
            print(f"Il file docker-compose.yml non esiste nella cartella di {nome_agente}.")
    else:
        print(f"La cartella per l'agente {nome_agente} non esiste.")