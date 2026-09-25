"""
On veut obtenir les statistiques concernant
un joueur
"""

import pandas as pd
import streamlit as st

from utils.api_client import api_client
from utils.log_init import get_page_logger

st.title("Stats menu")
logger = get_page_logger("stats_menu")

# on récupère l'id_player dans l'url de la page
id_player = st.query_params.id_player

# Je récupère l'identifiant du joueur avec les informations de la session
# player = st.session_state.get("player")
# id_player = player["id_player"]
# ces lignes ont été abandonnées après avoir trouvé comment changer les paramètres de l'url

# permet de lire les infos
#st.info(f"{player}")

# Je récupère les informations auprès de l'API
info_player = api_client.get(f"/player/{id_player}")["data"]

# J'affiche à l'écran les informations de l'utilisateur
# En titre de cette zone
st.subheader(info_player["username"])
# On crée un tableau à 2 colonnes
col1, col2 = st.columns(2)

with col1:
    st.metric("elo : ", info_player["elo"])

with col2:
    st.write(f"email = {info_player["email"]}")
    st.checkbox("Est un fan de pokemon", info_player["pokemon_fan"])

# On cherche maintenant les statistiques des matchs du joueur
info_game_player = api_client.get(path="/game", params={"id_player": id_player})["data"]
#st.info(f"{info_game_player}")
if info_game_player == []:
    st.write("Aucune partie n'a été jouée")
else:
    resultat_complet = pd.DataFrame([])
    for i in info_game_player:
        id_game = i["id_game"]

        if int(i['player1']["id_player"]) == int(id_player):
            player = i['player1']["username"]
            opponent = i['player2']["username"]
            opponent_elo = i['player2']["elo"]
        else:
            player = i['player2']["username"]
            opponent = i['player1']["username"]
            opponent_elo = i['player1']["elo"]
        resultat = {"game mode": i["game_mode"], "Opponent": opponent, "Resultat": i["description"]}
        resultat_complet.append(resultat)
st.dataframe(resultat_complet)
