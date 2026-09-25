"""
Streamlit page for the statistics of a player.

Provides navigation to available actions such as informations or game history for logged-in users.
"""
import pandas as pd
import streamlit as st

from utils.api_client import api_client
from utils.auth_guard import check_authentification
from utils.log_init import get_page_logger

st.title("Informations, stats, history")
logger = get_page_logger("player_stats")

check_authentification()

player = st.session_state.get("player")
print(player)
id_player = player["id_player"]
print(id_player)
infos_player = api_client.get(f"/player/{id_player}")["data"]
print(infos_player)
st.subheader(infos_player["username"])

col1, col2 = st.columns(2)
with col1:
    st.metric(label="elo", value=infos_player["elo"])
with col2:
    st.write(f"Email: {infos_player["email"]}")
    st.checkbox(label="Fan de Pokemon", value=infos_player["pokemon_fan"] )

dice_player = api_client.get(f"/game/?id_player={id_player}&game_mode=dice")["data"]
print(dice_player)
coinflip_player = api_client.get(f"/game/?id_player={id_player}&game_mode=coinflip")["data"]
print(coinflip_player)


def ligne_histo(game: dict, id_player: int) -> dict:
    if game["player1"]["id_player"] == id_player:
        opp = game["player2"]
    else:
        opp = game["player1"]
    opponent = f"{opp["username"]} ({opp["elo"]})"
    winner_id = game["winner"]["id_player"]
    if winner_id == id_player:
        result = "Win"
    elif winner_id == opp["id_player"]:
        result = "Loss"
    else:
        result = "Draw"
    return {"Mode": game["game_mode"], "Opponent": opponent, "Result": result}


st.subheader("Coin Games")
if len(dice_player) == 0:
    logger.info("No dice game found.")
    st.info("No dice game found.")
else:
    st.write(f"{len(dice_player)} dice game(s) played.")
    df = pd.DataFrame([ligne_histo(g, id_player) for g in dice_player])
    st.dataframe(df, hide_index=True)

st.subheader("CoinFlip Games")
if len(coinflip_player) == 0:
    logger.info("No coinflip game found.")
    st.info("No coinflip game found.")
else:
    st.write(f"{len(coinflip_player)} coinflip game(s) played.")
    df = pd.DataFrame([ligne_histo(g, id_player) for g in coinflip_player])
    st.dataframe(df, hide_index=True)

if st.button("Back to menu", type="primary"):
    st.switch_page("pages/player_menu.py")