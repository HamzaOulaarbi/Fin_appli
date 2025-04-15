import streamlit as st
import yfinance as yf
import pandas as pd

def calculer_sante_financiere(info):
    crit = []
    score = 0

    pe = info.get("trailingPE", None)
    if pe and 10 <= pe <= 25:
        score += 20
        crit.append("✅ PER entre 10 et 25")
    else:
        crit.append("❌ PER hors zone idéale (10-25)")

    eps = info.get("trailingEps", 0)
    if eps > 0:
        score += 20
        crit.append("✅ Bénéfice positif (EPS > 0)")
    else:
        crit.append("❌ EPS nul ou négatif")

    dividend = info.get("dividendYield", 0)
    if dividend and dividend > 0.02:
        score += 20
        crit.append("✅ Dividende > 2%")
    else:
        crit.append("❌ Dividende faible ou inexistant")

    beta = info.get("beta", 1)
    if 0.8 <= beta <= 1.2:
        score += 15
        crit.append("✅ Volatilité maîtrisée (Beta 0.8-1.2)")
    else:
        crit.append("❌ Beta hors plage recommandée")

    debt = info.get("debtToEquity", None)
    if debt is not None and debt < 100:
        score += 15
        crit.append("✅ Ratio dette/capitaux propres < 100%")
    else:
        crit.append("❌ Dette élevée ou inconnue")

    price = info.get("previousClose", 0)
    target = info.get("targetMeanPrice", 0)
    if price and target and target > price * 1.05:
        score += 10
        crit.append("✅ Potentiel haussier (>5%)")
    else:
        crit.append("❌ Peu ou pas de potentiel haussier")

    return round(score), crit

def afficher_analyse():
    # --- Liste d'entreprises ---
    company_dict = {
        "Apple (AAPL)": "AAPL", "Microsoft (MSFT)": "MSFT", "Amazon (AMZN)": "AMZN",
        "Forvia SE":"0MGR.IL", "NIKE, Inc.":"NKE",
        "Tesla (TSLA)": "TSLA", "Google (GOOGL)": "GOOGL", "Nvidia (NVDA)": "NVDA",
        "Meta (META)": "META", "Netflix (NFLX)": "NFLX", "Adobe (ADBE)": "ADBE",
        "JPMorgan (JPM)": "JPM", "Goldman Sachs (GS)": "GS", "Bank of America (BAC)": "BAC",
        "ExxonMobil (XOM)": "XOM", "Chevron (CVX)": "CVX", "TotalEnergies (TTE)": "TTE.PA", "Shell (SHEL)": "SHEL",
        "LVMH (MC)": "MC.PA", "Hermès (RMS)": "RMS.PA", "Kering (KER)": "KER.PA",
        "Coca-Cola (KO)": "KO", "PepsiCo (PEP)": "PEP",
        "Pfizer (PFE)": "PFE", "Johnson & Johnson (JNJ)": "JNJ", "Moderna (MRNA)": "MRNA",
        "Renault (RNO)": "RNO.PA", "Stellantis (STLA)": "STLAP.PA", "Valeo": "FR.PA",
        "Faurecia": "EO.PA", "Plastic Omnium": "POM.PA"
    }

    period_options = {
        "1 mois": "1mo", "3 mois": "3mo", "6 mois": "6mo",
        "1 an": "1y", "2 ans": "2y", "5 ans": "5y", "10 ans": "10y", "Depuis le début": "max"
    }

    st.title("📈 Analyse Financière Interactive des Actions")
    st.markdown("---")

    # Entrée des paramètres
    st.markdown("## Paramètres d'analyse")
    selected_names = st.multiselect("Entreprises :", list(company_dict.keys()), default=["Apple (AAPL)"])
    selected_period_label = st.selectbox("Période du graphique :", list(period_options.keys()), index=3)
    selected_period = period_options[selected_period_label]
    show_data = st.button("📊 Afficher")


    if show_data:
        st.subheader(f"📊 Cours des actions - {selected_period_label}")
        chart_data = {}
        for name in selected_names:
            symbol = company_dict[name]
            data = yf.Ticker(symbol).history(period=selected_period)
            if not data.empty:
                chart_data[name] = data["Close"]

        if chart_data:
            df = pd.DataFrame(chart_data)
            st.line_chart(df)
        else:
            st.warning("Aucune donnée trouvée pour la période sélectionnée.")

    # --- Résultats détaillés en dessous ---
        st.subheader("📄 Détails Financiers et Analyse de Santé")

        for name in selected_names:
            symbol = company_dict[name]
            ticker = yf.Ticker(symbol)
            info = ticker.info

            st.markdown(f"### {info.get('shortName', name)} ({symbol})")

            col1, col2, col3 = st.columns(3)

            def metric_with_note(title, value, note):
                st.write(f"**{title}**: {value}")
                st.markdown(f"<span style='color:gray; font-size: 0.8em;'>— {note}</span>", unsafe_allow_html=True)

            with col1:
                st.metric("📈 Dernière clôture", round(info.get("previousClose", 0), 2))
                metric_with_note("💵 Prix actuel", round(info.get("currentPrice", 0), 2), "Prix de l'action à l'instant T.")
                metric_with_note("🔮 Objectif 1 an", round(info.get("targetMeanPrice", 0), 2), "Estimation moyenne du prix dans 1 an.")
                metric_with_note("📉 Variation 52 sem.", f"{round(info.get('fiftyTwoWeekLow', 0), 2)} - {round(info.get('fiftyTwoWeekHigh', 0), 2)}", "Fourchette sur un an.")
                metric_with_note("📊 Volume moyen", f"{info.get('averageVolume', 'N/A'):,}", "Titres échangés par jour.")
                metric_with_note("📉 Beta", round(info.get("beta", 0), 2), "Volatilité par rapport au marché.")
                metric_with_note("💰 Capitalisation", f"{info.get('marketCap', 'N/A'):,}", "Valeur totale de l'entreprise.")

            with col2:
                metric_with_note("📊 P/E (ttm)", round(info.get("trailingPE", 0), 2), "Ratio cours/bénéfice passé.")
                metric_with_note("📊 P/E (prévision)", round(info.get("forwardPE", 0), 2), "Ratio basé sur bénéfices futurs.")
                metric_with_note("📈 EPS", round(info.get("trailingEps", 0), 2), "Bénéfice net par action.")
                metric_with_note("📘 Price/Book", round(info.get("priceToBook", 0), 2), "Comparaison au patrimoine net.")
                metric_with_note("📊 Price/Sales", round(info.get("priceToSalesTrailing12Months", 0), 2), "Valorisation par rapport au CA.")
                metric_with_note("💸 Marge nette", f"{round(info.get('profitMargins', 0) * 100, 2)} %", "Part du chiffre d’affaires en profit.")

            with col3:
                metric_with_note("📈 ROE", f"{round(info.get('returnOnEquity', 0) * 100, 2)} %", "Rentabilité des fonds propres.")
                metric_with_note("🏦 ROA", f"{round(info.get('returnOnAssets', 0) * 100, 2)} %", "Rendement sur les actifs.")
                metric_with_note("💰 Dividende", f"{round(info.get('dividendYield', 0) * 100, 2)} %" if info.get('dividendYield') else "N/A", "Rendement du dividende.")
                metric_with_note("📉 Dette / Equity", f"{round(info.get('debtToEquity', 0), 2)} %", "Ratio d’endettement.")
                metric_with_note("💵 Trésorerie", f"{info.get('totalCash', 'N/A'):,}", "Liquidités de l'entreprise.")
                metric_with_note("💼 Free Cashflow", f"{info.get('freeCashflow', 'N/A'):,}", "Cash restant après dépenses.")



            # Score de santé
            score, criteres = calculer_sante_financiere(info)
            st.markdown("**🧠 Note de santé financière**")
            st.metric(label="Score global", value=f"{score}/100")
            st.write("**Critères analysés :**")
            for c in criteres:
                st.write("- ", c)

            if score >= 80:
                st.success("Excellente santé financière")
            elif score >= 60:
                st.info("Bonne santé financière")
            elif score >= 40:
                st.warning("Santé moyenne")
            else:
                st.error("Santé financière faible")

            # Dividendes
            st.markdown("**💸 Historique des dividendes**")
            try:
                div_data = ticker.dividends
                if not div_data.empty:
                    st.bar_chart(div_data)
                else:
                    st.write("Pas de dividendes enregistrés.")
            except:
                st.write("Erreur lors du chargement des dividendes.")
    else:
        st.info("Sélectionnez au moins une entreprise pour commencer.")


    def generate_prompt_from_metrics(info):
        return f"""
    Voici les données financières de {info.get('shortName', 'cette entreprise')} :

    - Prix actuel : {info.get('currentPrice', 'N/A')}
    - Dernière clôture : {info.get('previousClose', 'N/A')}
    - Objectif 1 an : {info.get('targetMeanPrice', 'N/A')}
    - Variation 52 semaines : {info.get('fiftyTwoWeekLow', 'N/A')} - {info.get('fiftyTwoWeekHigh', 'N/A')}
    - P/E : {info.get('trailingPE', 'N/A')}
    - EPS : {info.get('trailingEps', 'N/A')}
    - ROE : {info.get('returnOnEquity', 'N/A')}
    - Dette/Equity : {info.get('debtToEquity', 'N/A')}
    - Free Cashflow : {info.get('freeCashflow', 'N/A')}
    - Dividende : {info.get('dividendYield', 'N/A')}

    Peux-tu fournir une synthèse financière concise et professionnelle de ces données ?
    """


    import requests

    def call_llm_synthesis(prompt):
        HF_API_URL = "https://router.huggingface.co/hf-inference/models/ProsusAI/finbert"
        headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}

        response = requests.post(HF_API_URL, headers=headers, json={"inputs": prompt})
        # return response.json()[0]['generated_text']
        return response.json()

        # if response.status_code == 200:
        #     return response.json()[0]['generated_text']
        # else:
        #     return "❌ Erreur dans la génération de la synthèse."

    if st.button("🧠 Générer une prediction automatique"):
        # selected_names = st.multiselect("Entreprises :", list(company_dict.keys()), default=["Apple (AAPL)"])
        symbol = company_dict[selected_names[0]]
        ticker = yf.Ticker(symbol)
        infog = ticker.info

        with st.spinner(f"Génération en cours pour {selected_names}..."):
            prompt = generate_prompt_from_metrics(infog)
            st.write(prompt)
            synthese = call_llm_synthesis(prompt)
            st.markdown("### 📋 Synthèse Automatisée")
            st.markdown(synthese)


    # from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    # import os
    # os.environ["STREAMLIT_WATCH_USE_POLLING"] = "true"
    # # ⚙️ Cache pour éviter de recharger à chaque fois
    # @st.cache_resource
    # def load_finance_llm():
    #     tokenizer = AutoTokenizer.from_pretrained("AdaptLLM/finance-LLM")
    #     model = AutoModelForCausalLM.from_pretrained("AdaptLLM/finance-LLM")
    #     return pipeline("text-generation", model=model, tokenizer=tokenizer)



    # # 🧠 Prompt dynamique
    # def generate_prompt_from_metrics(info):
    #     return f"""
    # Voici les données financières de {info.get('shortName', 'cette entreprise')} :

    # - Prix actuel : {info.get('currentPrice', 'N/A')}
    # - Dernière clôture : {info.get('previousClose', 'N/A')}
    # - Objectif 1 an : {info.get('targetMeanPrice', 'N/A')}
    # - Variation 52 semaines : {info.get('fiftyTwoWeekLow', 'N/A')} - {info.get('fiftyTwoWeekHigh', 'N/A')}
    # - P/E : {info.get('trailingPE', 'N/A')}
    # - EPS : {info.get('trailingEps', 'N/A')}
    # - ROE : {info.get('returnOnEquity', 'N/A')}
    # - Dette/Equity : {info.get('debtToEquity', 'N/A')}
    # - Free Cashflow : {info.get('freeCashflow', 'N/A')}
    # - Dividende : {info.get('dividendYield', 'N/A')}

    # Peux-tu fournir une synthèse financière concise et professionnelle de ces données ?
    # """

    # # 🎯 Génération locale avec le modèle
    # def call_llm_synthesis_local(prompt):
    #     output = pipe(prompt, max_new_tokens=300, do_sample=True, temperature=0.7)[0]["generated_text"]
    #     return output

    # # 🎬 Bouton dans Streamlit
    # if st.button("🧠 Générer une synthèse automatique"):
    #     symbol = company_dict[selected_names[0]]
    #     ticker = yf.Ticker(symbol)
    #     infog = ticker.info
        
    #     pipe = load_finance_llm()


    #     with st.spinner(f"Génération en cours pour {selected_names[0]}..."):
    #         prompt = generate_prompt_from_metrics(infog)
    #         st.markdown("##### 📝 Prompt envoyé au modèle")
    #         st.code(prompt, language="markdown")
            
    #         synthese = call_llm_synthesis_local(prompt)
            
    #         st.markdown("### 📋 Synthèse Automatisée")
    #         st.write(synthese)
