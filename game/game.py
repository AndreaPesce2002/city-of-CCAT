import json
import os
import random
import threading
import time
import pygame
import networkx as nx

import sys
from os.path import dirname, abspath

# Aggiungi la cartella padre al sys.path
sys.path.append(dirname(dirname(abspath(__file__))))

from collegamento_2 import converection

# Inizializzazione di Pygame
pygame.init()

# Creiamo la rete a partire dal nostro JSON
rete_stradale = nx.Graph()

# Impostazioni della finestra di gioco
larghezza_finestra = 800
altezza_finestra = 600
schermo = pygame.display.set_mode((larghezza_finestra, altezza_finestra))

# Caricamento dell'immagine della mappa
mappa = pygame.image.load('game/asset/map.png')
mappa = pygame.transform.scale(mappa, (larghezza_finestra, altezza_finestra))

# Caricamento dei dati degli agenti
with open('caratteristiche_agenti/agenti.json', 'r') as file:
    agenti = json.load(file)
    
    
# Caricamento dei dati dei punti della mappa
with open('game/punti_mappa.json', 'r') as file:
    punti_mappa = json.load(file)
    

for punto, dati in punti_mappa.items():
    rete_stradale.add_node(punto, pos=dati['pos'])
    for collegato in dati['collegati']:
        rete_stradale.add_edge(punto, collegato)
        
# Ora possiamo usare la rete per trovare il percorso
def trova_percorso(posizione_iniziale, destinazione):
    try:
        percorso = nx.shortest_path(rete_stradale, source=posizione_iniziale, target=destinazione)
        return percorso
    except nx.NetworkXNoPath:
        print(f"Non esiste un percorso tra {posizione_iniziale} e {destinazione}!")
        # Scegliamo una destinazione casuale tra i punti disponibili nella mappa
        destinazione_casuale = random.choice(list(punti_mappa.keys()))
        print(f"Scegliamo una destinazione casuale: {destinazione_casuale}")
        # Tentiamo di trovare un percorso per la nuova destinazione casuale
        try:
            percorso = nx.shortest_path(rete_stradale, source=posizione_iniziale, target=destinazione_casuale)
            return percorso
        except nx.NetworkXNoPath:
            print(f"Curioso! Sembrerebbe che anche {destinazione_casuale} sia irraggiungibile. Che enigma!")
            return None

def creaNuovaConnesione():
    con = converection()
    for nome, dettagli in agenti.items():
        con.personaggi[nome]=personaggio

    return con
# Creazione dei personaggi
class Personaggio:
    def __init__(self, nome, posizione_iniziale, punti_mappa):
        self.nome = nome
        self.posizione = punti_mappa[posizione_iniziale]['pos']
        self.punti_mappa = punti_mappa
        self.destinazione_attuale = None  # Nulla ancora, la definiremo dopo
        self.percorso = []  # Inizialmente vuoto, lo popoleremo con le coordinate
        self.immagine = pygame.image.load(f'game/asset/{nome}.png')
        self.immagine = pygame.transform.scale(self.immagine, (50, 50))
        self.indice_percorso = 0  # Aggiunto per tenere traccia della posizione nel percorso
        self.tempo_di_attesa = 5  # Tempo di attesa in secondi
        self.ultimo_tempo_di_fermo = time.time()
        # Impostiamo la prima destinazione e calcoliamo il percorso
        self.imposta_destinazione(random.choice(list(punti_mappa.keys())))
        self.staComunicando=False
        
    def mostra_mesaggio(self,testo_messaggio):
        if self.staComunicando:
            font = pygame.font.SysFont(None, 24)
            immagine_messaggio = font.render(testo_messaggio, True, (255, 255, 255))
            
            # Calcola le dimensioni del testo per posizionare adeguatamente lo sfondo
            larghezza_testo, altezza_testo = font.size(testo_messaggio)
            
            # Aggiungi uno sfondo nero intorno al messaggio
            sfondo = pygame.Rect(self.posizione[0] - 30, self.posizione[1] - 70, larghezza_testo + 10, altezza_testo + 10)
            pygame.draw.rect(schermo, (0, 0, 0), sfondo)
            
            # Disegna il messaggio sullo sfondo nero
            schermo.blit(immagine_messaggio, (self.posizione[0] - 25, self.posizione[1] - 60))
            
            # Aggiorna il display
            pygame.display.flip()
        
    def trova_nome_per_posizione(self,posizione, punti_mappa):
        for nome, attributi in punti_mappa.items():
            if attributi['pos'] == posizione:
                return nome
        return "Sconosciuto"  # Se non troviamo un nome corrispondente, ritorniamo "Sconosciuto"

    def imposta_destinazione(self, nuova_destinazione):
        self.destinazione_attuale = nuova_destinazione
        # Calcoliamo il percorso verso la nuova destinazione
        posizione_attuale = self.percorso[self.indice_percorso-1] if self.percorso else None
        if posizione_attuale:
        
            nome_luogo_attuale = self.trova_nome_per_posizione(posizione_attuale, self.punti_mappa)
            
            if(nome_luogo_attuale!="sconosciuto"):
                percorso=trova_percorso(nome_luogo_attuale, nuova_destinazione)

        else:
            percorso=trova_percorso(self.percorso[-1] if self.percorso else list(self.punti_mappa.keys())[0], nuova_destinazione)
            
        self.percorso = [rete_stradale.nodes[punto]['pos'] for punto in percorso]
        self.indice_percorso = 0  # Ripartiamo dall'inizio del nuovo percorso


    # Definiamo una funzione che si occuperà della comunicazione asincrona
    def gestisci_comunicazione(self, pers):
            posizione_attuale = self.percorso[self.indice_percorso-1] if self.percorso else None
            if posizione_attuale:
                if not (pers.staComunicando or self.staComunicando):
                    pers.staComunicando=True
                    self.staComunicando=True
                    con=creaNuovaConnesione()
                    con.creaConversazione(self.nome,pers.nome, f'*hai trovato {pers.nome} in {self.trova_nome_per_posizione(posizione_attuale, self.punti_mappa)}*')
                    con.chiudiSessione()
                    pers.staComunicando=False
                    self.staComunicando=False
                    time.sleep(5)  # Aspetta 5 secondi

    def segui_percorso(self):

        if not self.staComunicando:
            
            # Verifichiamo se siamo arrivati all'ultima destinazione
            if self.indice_percorso == len(self.percorso): # Ultima destinazione del percorso
                # Controlliamo se il tempo di attesa è trascorso
                if (time.time() - self.ultimo_tempo_di_fermo) >= self.tempo_di_attesa:
                    
                    con=creaNuovaConnesione()
                    conversazione = con.crea_messaggio()
                    con.creaConversazione(self.nome,self.nome,conversazione)
                    con.chiudiSessione()
                    
                    #self.imposta_destinazione(random.choice(list(punti_mappa.keys())))
                    
                    self.ultimo_tempo_di_fermo = time.time() # Reset del tempo di fermo
                # Non abbiamo bisogno di muoverci finché non è trascorso il tempo di attesa
                return

        
            # Se non è l'ultima destinazione, continuo il percorso come prima
            destinazione = self.percorso[self.indice_percorso]
            if self.posizione == destinazione:
                self.indice_percorso += 1  # Andiamo al prossimo punto del percorso
                if self.indice_percorso == len(self.percorso): # Se abbiamo raggiunto la fine, iniziamo il tempo di attesa
                    self.ultimo_tempo_di_fermo = time.time()
            else:
                self.muovi_verso(destinazione)
        
            #controlla se ci sono altri peronaggi nella stessa posizione
            for pers in personaggi:
                if pers.posizione == self.posizione and pers.nome!= self.nome:
                    if not (pers.staComunicando or self.staComunicando):
                        print(f"{pers.nome} e {self.nome} sono nella stessa poszione")
                        # Creiamo un thread per gestire la comunicazione
                        thread_comunicazione = threading.Thread(target=self.gestisci_comunicazione, args=(pers, ))
                        # Avviamo il thread
                        thread_comunicazione.start()
                        self.indice_percorso=0 

    
    def muovi_verso(self, destinazione):
        # Qui manteniamo la logica di movimento che avevi definito
        soglia = 5
        if abs(self.posizione[0] - destinazione[0]) < soglia and abs(self.posizione[1] - destinazione[1]) < soglia:
            self.posizione = destinazione[:]
        else:
            if self.posizione[0] < destinazione[0]:
                self.posizione[0] += min(1, destinazione[0] - self.posizione[0])
            elif self.posizione[0] > destinazione[0]:
                self.posizione[0] -= min(1, self.posizione[0] - destinazione[0])
            
            if self.posizione[1] < destinazione[1]:
                self.posizione[1] += min(1, destinazione[1] - self.posizione[1])
            elif self.posizione[1] > destinazione[1]:
                self.posizione[1] -= min(1, self.posizione[1] - destinazione[1])

# Inizializzazione dei personaggi
personaggi = []
for nome, dettagli in agenti.items():
    # Supponiamo che ogni agente abbia una posizione iniziale definita nel file JSON, altrimenti scegliamo una casuale
    posizione_iniziale = dettagli.get('posizione_iniziale', random.choice(list(punti_mappa.keys())))
    personaggio = Personaggio(nome, posizione_iniziale, punti_mappa)
    personaggi.append(personaggio)

# Funzione per disegnare gli elementi del gioco
def disegna():
    schermo.blit(mappa, (0, 0))
    for personaggio in personaggi:
        # Centriamo l'immagine rispetto alla posizione del personaggio
        x_centro = personaggio.posizione[0] - 25
        y_centro = personaggio.posizione[1] - 25
        schermo.blit(personaggio.immagine, (x_centro, y_centro))

# Ciclo principale del gioco
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.MOUSEMOTION:
        #     print(event.pos)  # This will print the position of the mouse when it moves

    # Aggiorna la posizione dei personaggi
    for personaggio in personaggi:
        personaggio.segui_percorso()  # Modificato per utilizzare la logica di segui_percorso

    # Disegna gli elementi del gioco sullo schermo
    disegna()

    # Aggiorna il display
    pygame.display.flip()

pygame.quit()
os._exit(0)  # Anche qui, 0 indica una terminazione senza errori