import streamlit as st
from portefeuille import afficher_portefeuille
from autres_analyses import afficher_analyse

# Appliquer le style global
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Onglets principaux
tab1, tab2 = st.tabs(["📊 Mon Portefeuille", "📈 Autre Analyse"])

with tab1:
    afficher_portefeuille()

with tab2:
    afficher_analyse()