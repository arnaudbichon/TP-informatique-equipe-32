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

st.subheader("Coin Games")
if len(dice_player) == 0:
    logger.info("No dice game found.")
    st.info("No dice game found.")
else:
    st.write(f"{len(dice_player)} dice game(s) played.")

st.subheader("CoinFlip Games")
if len(coinflip_player) == 0:
    logger.info("No coinflip game found.")
    st.info("No coinflip game found.")
else:
    st.write(f"{len(coinflip_player)} coinflip game(s) played.")

if st.button("Back to menu", type="primary"):
    st.switch_page("pages/player_menu.py")