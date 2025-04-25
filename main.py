import streamlit as st
from portefeuille import afficher_portefeuille
from autres_analyses import afficher_analyse
from screener import screener
from webscrapper import scrapper

# Appliquer le style global
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Onglets principaux
tab1, tab2, tab3,tab4 = st.tabs(["📊 Mon Portefeuille", "📈 Autre Analyse" ,"Screener", "Web scrapper"])

with tab1:
    afficher_portefeuille()

with tab2:
    afficher_analyse()

with tab3:
    screener()

with tab4:
    scrapper()