import streamlit as st
from dascboard import dacshboard, filtre
from trans_type import transct
from vente_date import vente_date_produit

menu = st.sidebar.selectbox(
    "📊 Menu",
    ["Dashboard", "Etude", "Transactions" , "vente"]
)

if menu == "Dashboard":
    dacshboard()

elif menu == "Etude":
    filtre()

elif menu == "Transactions":
    transct()

elif menu == "vente":
    vente_date_produit()