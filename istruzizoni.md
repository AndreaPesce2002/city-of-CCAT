1) avviare il file `crea_agnte_base.py`
2) avviare il docker compose dell'agente base
4) attivare i plugins e settare il LLM e nel caso caricare file essenziali (come ad esempio mappa)
5) spegnere il docker compose

6) avviare il file `avviDocker.py`
7) se necessario fare un test
    ```python
    import cheshire_cat_api as ccat


import time
import cheshire_cat_api as ccat

# Connection settings with default values
config = ccat.Config(
    base_url="localhost",
    port=1866,
    user_id="user",
    auth_key="",
    secure_connection=False
)

# Cat Client
cat_client = ccat.CatClient(
    config=config,
)

# Connect to the WebSocket API
cat_client.connect_ws()

# Close connection
cat_client.close()
    ```

8) avviare`game/game.py`