import os
import shutil
import subprocess
from git import Repo
import yaml
import toml
from packaging import version

# Percorso della cartella degli agenti
agent_folder_path = "agenti"

# URL del repository GitHub
#github_repo_url = "https://github.com/cheshire-cat-ai/core.git"
github_repo_url = "https://github.com/AndreaPesce2002/core_city_of_CCAT.git"

# Nome della cartella scaricata
downloaded_folder_name = "agente_base_2"

# Percorso della cartella dei file modificati
modified_files_path = "fileModificati"

destination_path = os.path.join(agent_folder_path, downloaded_folder_name)

if os.path.exists(destination_path):
    # Gestisci la situazione come preferisci, ad esempio eliminando la cartella esistente
    #shutil.rmtree(destination_path)
    subprocess.run(["sudo","rm","-fr", "./agente_base"], cwd=os.path.join(agent_folder_path), check=True)

repo = Repo.clone_from(github_repo_url, destination_path)

# Rinomina la cartella scaricata
os.rename(os.path.join(agent_folder_path, downloaded_folder_name), os.path.join(agent_folder_path, downloaded_folder_name))

# Sostituisci la cartella plugins
shutil.rmtree(os.path.join(agent_folder_path, downloaded_folder_name, "core", "cat", "plugins"))
shutil.copytree(os.path.join(agent_folder_path,modified_files_path, "plugins"), os.path.join(agent_folder_path, downloaded_folder_name, "core", "cat", "plugins"))


# Costruiamo il percorso del file docker-compose.yml all'interno della cartella
percorso_docker_compose = os.path.join(agent_folder_path, downloaded_folder_name, 'docker-compose.yml')

# Carichiamo il contenuto del file docker-compose.yml
with open(percorso_docker_compose, 'r') as file:
    docker_compose_content = yaml.safe_load(file)

# Modifichiamo il contenuto come necessario
docker_compose_content['services']['cheshire-cat-core']['container_name'] = f"cheshire_cat_core_base"
# Per modificare la porta (decommenta e modifica se necessario)
docker_compose_content['services']['cheshire-cat-core']['environment'][3] = f"CORE_PORT={1866}"
docker_compose_content['services']['cheshire-cat-core']['ports'][0] = f"{1866}:80"

# Sovrascrivi il file docker-compose.yml con le modifiche
with open(percorso_docker_compose, 'w') as file:
    yaml.safe_dump(docker_compose_content, file)

# Esegui la build dell'immagine Docker
subprocess.run(["docker-compose", "build"], cwd=os.path.join(agent_folder_path, downloaded_folder_name), check=True)

print("Operazioni completate con successo.")
