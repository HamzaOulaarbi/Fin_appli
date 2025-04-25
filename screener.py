# import streamlit as st
# import yfinance as yf
# import pandas as pd
# from company_dict import company_dict
# # Dictionnaire des entreprises avec leurs symboles Yahoo Finance

# def screener ():

#     st.header("🔎 Screener d'Actions")

#     # Filtres
#     st.subheader("🎯 Critères de filtrage")
#     min_revenue = st.number_input("Chiffre d'affaires minimum (en milliards)", value=10.0)
#     max_pe = st.number_input("P/E maximum", value=20.0)
#     min_dividend = st.number_input("Rendement du dividende minimum (%)", value=2.0)
#     max_beta = st.number_input("Bêta maximum", value=1.5)

#     # Bouton pour lancer l'analyse
#     if st.button("🔍 Lancer l'analyse"):
#         with st.spinner("⏳ Analyse en cours..."):
#             # Liste des symboles à analyser
#             tickers_list = list(company_dict.values())
#             # Récupération des données
#             st.subheader("📥 Récupération des données...")
#             selected_companies = []
#             for symbol in tickers_list:
#                 ticker = yf.Ticker(symbol)
#                 info = ticker.info
#                 revenue = info.get('totalRevenue', 0)
#                 pe_ratio = info.get('trailingPE', None)
#                 dividend_yield = info.get('dividendYield', 0)
#                 beta = info.get('beta', None)

#                 # Conversion des valeurs
#                 revenue_billion = revenue / 1e9 if revenue else 0
#                 dividend_percent = dividend_yield * 100 if dividend_yield else 0

#                 # Filtrage selon les critères
#                 if (
#                     revenue_billion >= min_revenue and
#                     pe_ratio is not None and pe_ratio <= max_pe and
#                     dividend_percent >= min_dividend and
#                     beta is not None and beta <= max_beta
#                 ):
#                     selected_companies.append({
#                         'Nom': info.get('shortName', symbol),
#                         'Symbole': symbol,
#                         'Chiffre d\'affaires (Mds)': round(revenue_billion, 2),
#                         'P/E': round(pe_ratio, 2),
#                         'Dividende (%)': round(dividend_percent, 2),
#                         'Bêta': round(beta, 2)
#                     })

#             # Affichage des résultats
#             st.subheader("📊 Entreprises correspondant aux critères")
#             if selected_companies:
#                 df_results = pd.DataFrame(selected_companies)
#                 st.dataframe(df_results)
#             else:
#                 st.warning("Aucune entreprise ne correspond aux critères sélectionnés.")



#     st.header("📈 Analyse temporelle d'une entreprise")

#     st.header("📈 Analyse temporelle d'une entreprise")

#     # Sélection de l'entreprise
#     company_name = st.selectbox("Sélectionnez une entreprise", list(company_dict.keys()))
#     symbol = company_dict[company_name]

#     # Période d'analyse
#     start_date = st.date_input("Date de début", pd.to_datetime("2020-01-01"))
#     end_date = st.date_input("Date de fin", pd.to_datetime("today"))

#     # Indicateurs disponibles
#     indicators = {
#         "Cours de clôture": "Close",
#         "Volume": "Volume",
#         "Moyenne mobile 20 jours": "MA20",
#         "Moyenne mobile 50 jours": "MA50",
#         "Moyenne mobile 200 jours": "MA200",
#         "Chiffre d'affaires": "Revenue",
#         "Bénéfice net": "NetIncome",
#         "Ratio P/E": "PERatio",
#         "Rendement du dividende": "DividendYield",
#         "Bêta": "Beta",
#         "Marge brute": "GrossMargin",
#         "Marge nette": "NetMargin",
#         "EBITDA": "EBITDA",
#         "Flux de trésorerie": "CashFlow",
#         "Ratio d'endettement": "DebtRatio",
#         "Retour sur investissement (ROI)": "ROI",
#         "Retour sur capitaux propres (ROE)": "ROE"
#     }

#     selected_indicators = st.multiselect("Indicateurs à afficher", list(indicators.keys()), default=["Cours de clôture"])

#     # Récupération des données
#     ticker = yf.Ticker(symbol)
#     df = ticker.history(start=start_date, end=end_date)

#     # Calcul des moyennes mobiles si sélectionnées
#     if "Moyenne mobile 20 jours" in selected_indicators:
#         df["MA20"] = df["Close"].rolling(window=20).mean()
#     if "Moyenne mobile 50 jours" in selected_indicators:
#         df["MA50"] = df["Close"].rolling(window=50).mean()
#     if "Moyenne mobile 200 jours" in selected_indicators:
#         df["MA200"] = df["Close"].rolling(window=200).mean()

#     # Affichage du graphique
#     st.subheader(f"📊 Indicateurs pour {company_name}")
#     st.line_chart(df[[indicators[ind] for ind in selected_indicators if indicators[ind] in df.columns]])


import streamlit as st
import yfinance as yf
import pandas as pd
from company_dict import company_dict

def screener():

    st.header("🔎 Screener d'Actions")

    # Filtres
    st.subheader("🎯 Critères de filtrage")
    min_revenue = st.number_input("Chiffre d'affaires minimum (en milliards)", value=10.0)
    max_pe = st.number_input("P/E maximum", value=20.0)
    min_dividend = st.number_input("Rendement du dividende minimum (%)", value=2.0)
    max_beta = st.number_input("Bêta maximum", value=1.5)

    # Bouton pour lancer l'analyse
    if st.button("🔍 Lancer l'analyse"):
        with st.spinner("⏳ Analyse en cours..."):
            # Liste des symboles à analyser
            tickers_list = list(company_dict.values())
            # Récupération des données
            st.subheader("📥 Récupération des données...")
            selected_companies = []
            for symbol in tickers_list:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                revenue = info.get('totalRevenue', 0)
                pe_ratio = info.get('trailingPE', None)
                dividend_yield = info.get('dividendYield', 0)
                beta = info.get('beta', None)

                # Conversion des valeurs
                revenue_billion = revenue / 1e9 if revenue else 0
                dividend_percent = dividend_yield * 100 if dividend_yield else 0

                # Filtrage selon les critères
                if (
                    revenue_billion >= min_revenue and
                    pe_ratio is not None and pe_ratio <= max_pe and
                    dividend_percent >= min_dividend and
                    beta is not None and beta <= max_beta
                ):
                    selected_companies.append({
                        'Nom': info.get('shortName', symbol),
                        'Symbole': symbol,
                        'Chiffre d\'affaires (Mds)': round(revenue_billion, 2),
                        'P/E': round(pe_ratio, 2),
                        'Dividende (%)': round(dividend_percent, 2),
                        'Bêta': round(beta, 2)
                    })

            # Affichage des résultats
            st.subheader("📊 Entreprises correspondant aux critères")
            if selected_companies:
                df_results = pd.DataFrame(selected_companies)
                st.dataframe(df_results)
            else:
                st.warning("Aucune entreprise ne correspond aux critères sélectionnés.")

    st.header("📈 Analyse temporelle d'une entreprise")

    # Sélection de l'entreprise
    company_name = st.selectbox("Sélectionnez une entreprise", list(company_dict.keys()))
    symbol = company_dict[company_name]

    # Période d'analyse
    start_date = st.date_input("Date de début", pd.to_datetime("2020-01-01"))
    end_date = st.date_input("Date de fin", pd.to_datetime("today"))

    # Indicateurs disponibles
    indicators = {
        "Cours de clôture": "Close",
        "Volume": "Volume",
        "Moyenne mobile 20 jours": "MA20",
        "Moyenne mobile 50 jours": "MA50",
        "Moyenne mobile 200 jours": "MA200",
        "Chiffre d'affaires": "Revenue",
        "Bénéfice net": "NetIncome",
        "Ratio P/E": "PERatio",
        "Rendement du dividende": "DividendYield",
        "Bêta": "Beta",
        "Marge brute": "GrossMargin",
        "Marge nette": "NetMargin",
        "EBITDA": "EBITDA",
        "Flux de trésorerie": "CashFlow",
        "Ratio d'endettement": "DebtRatio",
        "Retour sur investissement (ROI)": "ROI",
        "Retour sur capitaux propres (ROE)": "ROE"
    }

    selected_indicators = st.multiselect("Indicateurs à afficher", list(indicators.keys()), default=["Cours de clôture"])

    # Récupération des données de l'entreprise
    ticker = yf.Ticker(symbol)

    # Récupération des états financiers (chiffre d'affaires, bénéfice net, etc.)
    financials = ticker.financials.transpose()
    financials.index = pd.to_datetime(financials.index)

    # Désactiver le fuseau horaire sur les données financières
    financials.index = financials.index.tz_localize(None)

    # Sélection des indicateurs financiers
    revenue = financials["Total Revenue"]
    net_income = financials["Net Income"]

    # Récupération des données historiques des prix
    df = ticker.history(start=start_date, end=end_date)

    # Désactivation du fuseau horaire sur les données boursières
    df.index = df.index.tz_localize(None)

    # Calcul des moyennes mobiles si sélectionnées
    if "Moyenne mobile 20 jours" in selected_indicators:
        df["MA20"] = df["Close"].rolling(window=20).mean()
    if "Moyenne mobile 50 jours" in selected_indicators:
        df["MA50"] = df["Close"].rolling(window=50).mean()
    if "Moyenne mobile 200 jours" in selected_indicators:
        df["MA200"] = df["Close"].rolling(window=200).mean()

    # Affichage des graphiques
    st.subheader(f"📊 Indicateurs pour {company_name}")

    columns_to_plot_price = [indicators[ind] for ind in selected_indicators if indicators[ind] in df.columns]
    df_plot = df.copy()

    # Ajout des indicateurs financiers peu fréquents
    financials_df = pd.DataFrame(index=financials.index)

    if "Chiffre d'affaires" in selected_indicators and "Total Revenue" in financials.columns:
        financials_df["Revenue"] = financials["Total Revenue"] / 1e9  # en milliards

    if "Bénéfice net" in selected_indicators and "Net Income" in financials.columns:
        financials_df["Net Income"] = financials["Net Income"] / 1e9  # en milliards

    # Exemple pour d'autres indicateurs depuis les états financiers
    if "EBITDA" in selected_indicators and "EBITDA" in financials.columns:
        financials_df["EBITDA"] = financials["EBITDA"] / 1e9

    if "GrossMargin" in selected_indicators and "Gross Profit" in financials.columns and "Total Revenue" in financials.columns:
        financials_df["GrossMargin"] = (financials["Gross Profit"] / financials["Total Revenue"]) * 100

    if "NetMargin" in selected_indicators and "Net Income" in financials.columns and "Total Revenue" in financials.columns:
        financials_df["NetMargin"] = (financials["Net Income"] / financials["Total Revenue"]) * 100

    # Informations ponctuelles (non temporelles)
    info = ticker.info
    static_data = {}

    if "Ratio P/E" in selected_indicators and info.get("trailingPE"):
        static_data["P/E"] = info["trailingPE"]

    if "Rendement du dividende" in selected_indicators and info.get("dividendYield"):
        static_data["Dividend Yield (%)"] = info["dividendYield"] * 100

    if "Bêta" in selected_indicators and info.get("beta"):
        static_data["Beta"] = info["beta"]

    if "ROI" in selected_indicators and info.get("returnOnInvestment"):
        static_data["ROI (%)"] = info["returnOnInvestment"] * 100

    if "ROE" in selected_indicators and info.get("returnOnEquity"):
        static_data["ROE (%)"] = info["returnOnEquity"] * 100

    if "Ratio d'endettement" in selected_indicators and info.get("debtToEquity"):
        static_data["Debt Ratio"] = info["debtToEquity"]

    # Affichage des courbes de prix
    if columns_to_plot_price:
        st.line_chart(df_plot[columns_to_plot_price])

    # Affichage des indicateurs financiers (scatter)
    import altair as alt

    # Vérification : au moins un indicateur financier est sélectionné et dispo
    if not financials_df.empty:
        st.write("📍 Indicateurs financiers sélectionnés (dans un seul graphique)")

        # On passe le DataFrame en format long pour Altair (Date, Indicateur, Valeur)
        df_long = financials_df.reset_index().melt(id_vars="index", var_name="Indicateur", value_name="Valeur")
        df_long = df_long.rename(columns={"index": "Date"})

        chart = alt.Chart(df_long).mark_line(point=True).encode(
            x=alt.X("Date:T", title="Date"),
            y=alt.Y("Valeur:Q", title="Valeur"),
            color=alt.Color("Indicateur:N", title="Indicateur"),
            tooltip=["Date:T", "Indicateur:N", "Valeur:Q"]
        ).properties(
            width=700,
            height=400
        ).interactive()

        st.altair_chart(chart, use_container_width=True)
    # Affichage des données ponctuelles (ex: P/E, Beta...)
    if static_data:
        st.write("ℹ️ Indicateurs actuels")
        st.json(static_data)