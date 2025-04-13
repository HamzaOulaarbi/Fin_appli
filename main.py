# import streamlit as st
# import yfinance as yf
# import pandas as pd

# st.set_page_config(page_title="Analyse Financière d’Actions", layout="wide")

# # --- STYLES ---
# st.markdown("""
#     <style>
#     .main { background-color: #f9f9f9; }
#     .block-container { padding-top: 2rem; padding-bottom: 2rem; }
#     .stMetric { background-color: #fafafa; border-radius: 8px; padding: 1rem; }
#     h1, h2, h3, h4 { color: #003366; }
#     </style>
# """, unsafe_allow_html=True)

# # --- Liste d'entreprises ---
# company_dict = {
#     "Apple (AAPL)": "AAPL", "Microsoft (MSFT)": "MSFT", "Amazon (AMZN)": "AMZN",
#     "Forvia SE":"0MGR.IL", "NIKE, Inc.":"NKE",
#     "Tesla (TSLA)": "TSLA", "Google (GOOGL)": "GOOGL", "Nvidia (NVDA)": "NVDA",
#     "Meta (META)": "META", "Netflix (NFLX)": "NFLX", "Adobe (ADBE)": "ADBE",
#     "JPMorgan (JPM)": "JPM", "Goldman Sachs (GS)": "GS", "Bank of America (BAC)": "BAC",
#     "ExxonMobil (XOM)": "XOM", "Chevron (CVX)": "CVX", "TotalEnergies (TTE)": "TTE.PA", "Shell (SHEL)": "SHEL",
#     "LVMH (MC)": "MC.PA", "Hermès (RMS)": "RMS.PA", "Kering (KER)": "KER.PA",
#     "Coca-Cola (KO)": "KO", "PepsiCo (PEP)": "PEP",
#     "Pfizer (PFE)": "PFE", "Johnson & Johnson (JNJ)": "JNJ", "Moderna (MRNA)": "MRNA",
#     "Renault (RNO)": "RNO.PA", "Stellantis (STLA)": "STLA.PA", "Valeo": "FR.PA",
#     "Faurecia": "EO.PA", "Plastic Omnium": "POM.PA"
# }

# period_options = {
#     "1 mois": "1mo", "3 mois": "3mo", "6 mois": "6mo",
#     "1 an": "1y", "2 ans": "2y", "5 ans": "5y", "10 ans": "10y", "Depuis le début": "max"
# }

# # --- Score de santé financière ---
# def calculer_sante_financiere(info):
#     crit = []
#     score = 0

#     pe = info.get("trailingPE", None)
#     if pe and 10 <= pe <= 25:
#         score += 20
#         crit.append("✅ PER entre 10 et 25")
#     else:
#         crit.append("❌ PER hors zone idéale (10-25)")

#     eps = info.get("trailingEps", 0)
#     if eps > 0:
#         score += 20
#         crit.append("✅ Bénéfice positif (EPS > 0)")
#     else:
#         crit.append("❌ EPS nul ou négatif")

#     dividend = info.get("dividendYield", 0)
#     if dividend and dividend > 0.02:
#         score += 20
#         crit.append("✅ Dividende > 2%")
#     else:
#         crit.append("❌ Dividende faible ou inexistant")

#     beta = info.get("beta", 1)
#     if 0.8 <= beta <= 1.2:
#         score += 15
#         crit.append("✅ Volatilité maîtrisée (Beta 0.8-1.2)")
#     else:
#         crit.append("❌ Beta hors plage recommandée")

#     debt = info.get("debtToEquity", None)
#     if debt is not None and debt < 100:
#         score += 15
#         crit.append("✅ Ratio dette/capitaux propres < 100%")
#     else:
#         crit.append("❌ Dette élevée ou inconnue")

#     price = info.get("previousClose", 0)
#     target = info.get("targetMeanPrice", 0)
#     if price and target and target > price * 1.05:
#         score += 10
#         crit.append("✅ Potentiel haussier (>5%)")
#     else:
#         crit.append("❌ Peu ou pas de potentiel haussier")

#     return round(score), crit

# # --- Barre latérale ---
# st.sidebar.title("🔎 Paramètres")
# selected_names = st.sidebar.multiselect("Entreprises :", list(company_dict.keys()), default=["Apple (AAPL)"])
# selected_period_label = st.sidebar.selectbox("Période du graphique :", list(period_options.keys()), index=3)
# selected_period = period_options[selected_period_label]

# # --- Affichage principal ---
# st.title("📈 Analyse Financière Interactive des Actions")

# # --- Graphique ---
# if selected_names:
#     st.subheader(f"📊 Comparaison du cours des actions - {selected_period_label}")
#     chart_data = {}
#     for name in selected_names:
#         symbol = company_dict[name]
#         data = yf.Ticker(symbol).history(period=selected_period)
#         if not data.empty:
#             chart_data[name] = data["Close"]

#     if chart_data:
#         df = pd.DataFrame(chart_data)
#         st.line_chart(df)
#     else:
#         st.warning("Aucune donnée trouvée pour la période sélectionnée.")

# # --- Résultats détaillés en dessous ---
#     st.subheader("📄 Détails Financiers et Analyse de Santé")

#     for name in selected_names:
#         symbol = company_dict[name]
#         ticker = yf.Ticker(symbol)
#         info = ticker.info

#         st.markdown(f"### {info.get('shortName', name)} ({symbol})")

#         col1, col2, col3 = st.columns(3)
#         with col1:
#             st.metric("Dernière clôture", info.get("previousClose", "N/A"))
#             st.write("**P/E (PER) :**", info.get("trailingPE", "N/A"))
#             st.write("**Bénéfice par action (EPS) :**", info.get("trailingEps", "N/A"))
#             st.write("**Dividende (%) :**", round(info.get("dividendYield", 0), 2) if info.get("dividendYield") else "N/A")
#             st.write("**Beta :**", info.get("beta", "N/A"))



#         with col2:
#             st.write("**Capitalisation :**", info.get("marketCap", "N/A"))
#             st.write("**Volume :**", info.get("volume", "N/A"))
#             st.write("**Objectif 1 an :**", info.get("targetMeanPrice", "N/A"))
#             st.write("**Var 52 sem. :**", f"{info.get('fiftyTwoWeekLow', 'N/A')} - {info.get('fiftyTwoWeekHigh', 'N/A')}")

#         with col3:

#             st.write("Dette/Capitaux propres", f"{info.get('debtToEquity', 'N/A')} %")
#             st.write("Flux de trésorerie libre", f"{info.get('freeCashflow', 'N/A'):,}")
#             st.write("BPA (ttm)", info.get("trailingEps", "N/A"))
#             st.write("Cash total", f"{info.get('totalCash', 'N/A'):,}")
#             st.write("Chiffre d'affaires", f"{info.get('totalRevenue', 'N/A'):,}")
#             st.write("Bénéfice net", f"{info.get('netIncomeToCommon', 'N/A'):,}")
#             st.write("P/E (ttm)", info.get("trailingPE", "N/A"))
#             st.write("P/E (prévision)", info.get("forwardPE", "N/A"))
#             st.write("Rendement fonds propres (ROE)", f"{round(info.get('returnOnEquity', 0) * 100, 2)} %")
#             st.write("Valeur entreprise", f"{info.get('enterpriseValue', 'N/A'):,}")
#             st.write("Cours/Registre comptable", info.get("priceToBook", "N/A"))
#             st.write("Rendement actifs (ROA)", f"{round(info.get('returnOnAssets', 0) * 100, 2)} %")
#             st.write("Cap. boursière", f"{info.get('marketCap', 'N/A'):,}")
#             st.write("Cours/Ventes (ttm)", info.get("priceToSalesTrailing12Months", "N/A"))
#             st.write("Marge bénéficiaire", f"{round(info.get('profitMargins', 0) * 100, 2)} %")

#         # Score de santé
#         score, criteres = calculer_sante_financiere(info)
#         st.markdown("**🧠 Note de santé financière**")
#         st.metric(label="Score global", value=f"{score}/100")
#         st.write("**Critères analysés :**")
#         for c in criteres:
#             st.write("- ", c)

#         if score >= 80:
#             st.success("Excellente santé financière")
#         elif score >= 60:
#             st.info("Bonne santé financière")
#         elif score >= 40:
#             st.warning("Santé moyenne")
#         else:
#             st.error("Santé financière faible")

#         # Dividendes
#         st.markdown("**💸 Historique des dividendes**")
#         try:
#             div_data = ticker.dividends
#             if not div_data.empty:
#                 st.bar_chart(div_data)
#             else:
#                 st.write("Pas de dividendes enregistrés.")
#         except:
#             st.write("Erreur lors du chargement des dividendes.")
# else:
#     st.info("Sélectionnez au moins une entreprise pour commencer.")




# # Portefeuille 
import streamlit as st
import pandas as pd
import yfinance as yf
from forex_python.converter import CurrencyRates
import plotly.graph_objects as go

# Initialisation du convertisseur de devises
c = CurrencyRates()

# Chargement des données depuis le fichier Excel
@st.cache_data
def charger_portefeuille(fichier):
    df = pd.read_excel(fichier)
    symboles_yahoo = {
        "EPA:MC": "MC.PA", "EPA:KER": "KER.PA", "EPA:FRVIA": "FRVIA.PA", "EPA:STLA": "STLA.PA", 
        "AMS:ASML": "ASML.AS", "EPA:TTE": "TTE.PA", "EPA:FR": "FR.PA", "EPA:AF": "AF.PA", 
        "ETR:VBK": "VBK.DE", "NASDAQ:NVDA": "NVDA", "AMS:SHELL": "SHELL.AS", "TYO:7011": "7011.T", 
        "NASDAQ:GOOGL": "GOOGL", "NYSE:NKE": "NKE", "NASDAQ:PYPL": "PYPL", 
        "NYSE:GES": "GES", "NASDAQ:UAL": "UAL"
    }
    df["Symbole_Yahoo"] = df["Symbole (GOOGLEFINANCE)"].map(symboles_yahoo)
    return df

# Récupérer prix et devise de chaque action
def get_infos_yahoo(ticker):
    try:
        t = yf.Ticker(ticker)
        info = t.info
        prix = info.get("regularMarketPrice", None)
        devise = info.get("currency", "EUR")
        return prix, devise
    except:
        return None, "EUR"

# Conversion de devise
@st.cache_data
def convertir_vers_euro(montant, devise):
    try:
        if devise == "EUR":
            return montant
        taux = c.get_rate(devise, "EUR")
        print(taux)
        return montant * taux
    except:
        return montant  # fail-safe

# Calcul des stats du portefeuille
def evaluer_portefeuille(df):
    prix_actuels, devises = [], []

    for ticker in df["Symbole_Yahoo"]:
        prix, devise = get_infos_yahoo(ticker)
        prix_actuels.append(prix)
        devises.append(devise)

    df["Devise"] = devises
    df["Prix Actuel (devise)"] = prix_actuels

    df["Prix Actuel (€)"] = [
        convertir_vers_euro(p, d) if p is not None else None
        for p, d in zip(df["Prix Actuel (devise)"], df["Devise"])
    ]
    df["Prix achat (€)"] = [
        convertir_vers_euro(p, d) if d != "EUR" else p
        for p, d in zip(df["Prix d'achat (€)"], df["Devise"])
    ]

    df["Total Investi (€)"] = df["Prix achat (€)"] * df["Quantité"]
    df["Valeur Actuelle (€)"] = df["Prix Actuel (€)"] * df["Quantité"]
    df["Gain/Perte (€)"] = df["Valeur Actuelle (€)"] - df["Total Investi (€)"]
    df["Gain/Perte (%)"] = (df["Gain/Perte (€)"] / df["Total Investi (€)"]) * 100
    return df

# Interface Streamlit
st.set_page_config(layout="wide")
st.title("📊 Suivi de mon portefeuille d’investissement")

# Sidebar
st.sidebar.header("Paramètres")
fichier_excel = st.sidebar.file_uploader("📁 Téléverser votre fichier Excel", type=["xlsx"])

if fichier_excel:
    df = charger_portefeuille(fichier_excel)
    df = evaluer_portefeuille(df)

    # Résumé global
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

    def colorer(val):
        if isinstance(val, (int, float)):
            if val > 0:
                return "color:green"
            elif val < 0:
                return "color:red"
        return ""

    st.dataframe(df.style.applymap(colorer, subset=["Gain/Perte (€)", "Gain/Perte (%)"]), use_container_width=True)

    st.markdown("### 📊 Répartition du portefeuille")
    pie = go.Figure(data=[go.Pie(labels=df["Entreprise"], values=df["Valeur Actuelle (€)"], hole=.4)])
    st.plotly_chart(pie, use_container_width=True)

    st.markdown("### 📌 Résumé global")
    st.write(f"**Total investi :** {total_investi:,.2f} €")
    st.write(f"**Valeur actuelle :** {total_valeur:,.2f} €")
    st.write(f"**Gain/Perte total :** {total_gain:,.2f} € ({total_pct:.2f} %)")

else:
    st.info("📥 Veuillez téléverser votre fichier Excel pour voir les résultats.")
