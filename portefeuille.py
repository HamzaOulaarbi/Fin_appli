import streamlit as st
import pandas as pd
import yfinance as yf
import requests
import plotly.graph_objects as go

API_KEY = "06edb4df4cef483a00c0529c"
BASE_CURRENCY = "EUR"

@st.cache_data
def charger_portefeuille(fichier):
    df = pd.read_excel(fichier)
    symboles_yahoo = {
        "EPA:MC": "MC.PA", "EPA:KER": "KER.PA", "EPA:FRVIA": "FRVIA.PA", "EPA:STLA": "STLAP.PA", 
        "AMS:ASML": "ASML.AS", "EPA:TTE": "TTE.PA", "EPA:FR": "FR.PA", "EPA:AF": "AF.PA", 
        "ETR:VBK": "VBK.DE", "NASDAQ:NVDA": "NVDA", "AMS:SHELL": "SHELL.AS", "TYO:7011": "7011.T", 
        "NASDAQ:GOOGL": "GOOGL", "NYSE:NKE": "NKE", "NASDAQ:PYPL": "PYPL", 
        "NYSE:GES": "GES", "NASDAQ:UAL": "UAL",
        "IWLE.DE": "IWLE.DE",        # iShares MSCI World
        "PSP5.PA": "PSP5.PA",       # AMUNDI S&P500
        "PUST.PA": "PUST.PA",       # AMUNDI NASDAQ-100
        }
    df["Symbole_Yahoo"] = df["Symbole (GOOGLEFINANCE)"].map(symboles_yahoo)
    return df

def get_infos_yahoo(ticker):
    try:
        data = yf.Ticker(ticker).info
        return data.get("regularMarketPrice", None), data.get("currency", "EUR")
    except:
        return None, "EUR"

@st.cache_data   
def get_taux_change(devise_source, devise_cible="EUR"):
    if devise_source == devise_cible:
        return 1.0
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/EUR"
    response = requests.get(url)
    data = response.json()
    return data["conversion_rates"].get(devise_source, 1.0)

def evaluer_portefeuille(df):
    prix_actuels, devises, taux_changes = [], [], []

    for ticker in df["Symbole_Yahoo"]:
        prix, devise = get_infos_yahoo(ticker)
        prix_actuels.append(prix)
        devises.append(devise)
        taux_changes.append(get_taux_change(devise))

    df["Devise"] = devises
    df["Taux de change"] = taux_changes
    df["Prix Actuel (devise)"] = prix_actuels
    df["Prix Actuel (€)"] = df["Prix Actuel (devise)"] / df["Taux de change"]

    df["Total Investi (€)"] = df["Prix d'achat (€)"] * df["Quantité"]
    df["Valeur Actuelle (€)"] = df["Prix Actuel (€)"] * df["Quantité"]
    df["Gain/Perte (€)"] = df["Valeur Actuelle (€)"] - df["Total Investi (€)"]
    df["Gain/Perte (%)"] = (df["Gain/Perte (€)"] / df["Total Investi (€)"]) * 100
    return df.round(2)

def colorer(val):
    if isinstance(val, (int, float)):
        if val > 0:
            return "color:green"
        elif val < 0:
            return "color:red"
    return ""

def afficher_portefeuille():
    st.title("📊 Suivi de mon portefeuille d’investissement")
    st.markdown("---")

    fichier_excel = st.file_uploader("📁 Téléverser votre fichier Excel", type=["xlsx"])

    if fichier_excel:
        df = charger_portefeuille(fichier_excel)
        df = evaluer_portefeuille(df)

        total_investi = df["Total Investi (€)"].sum()
        total_valeur = df["Valeur Actuelle (€)"].sum()
        total_gain = total_valeur - total_investi
        total_pct = (total_gain / total_investi) * 100

        st.subheader("📈 Résumé du portefeuille")
        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Total investi", f"{total_investi:,.2f} €")
        col2.metric("📉 Valeur actuelle", f"{total_valeur:,.2f} €")
        col3.metric("🔁 Gain/Perte", f"{total_gain:,.2f} €", f"{total_pct:.2f} %")

        st.markdown("### 📋 Détails par action")
        st.dataframe(
            df.style.applymap(colorer, subset=["Gain/Perte (€)", "Gain/Perte (%)"]),
            use_container_width=True
        )

        st.markdown("### 📊 Répartition du portefeuille")
        pie = go.Figure(data=[
            go.Pie(labels=df["Entreprise"], values=df["Valeur Actuelle (€)"], hole=.4)
        ])
        st.plotly_chart(pie, use_container_width=True)

    else:
        st.info("📥 Veuillez téléverser votre fichier Excel pour voir les résultats.")
