import streamlit as st
import requests
from bs4 import BeautifulSoup
from transformers import pipeline

@st.cache_resource
def load_models():
    try:
     
        sentiment_model = pipeline("sentiment-analysis", model="ProsusAI/finbert")
        summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        translator = pipeline("translation_en_to_fr", model="Helsinki-NLP/opus-mt-en-fr")      
        return sentiment_model, translator, summarizer

    except Exception as e:
        st.error(f"Erreur de chargement des modèles : {e}")
        return None, None
sentiment_model,translator, summarizer = load_models()

# Récupérer le texte complet de l'article (basique via Yahoo pour maintenant)
def get_article_text(url):
    try:
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(res.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = " ".join(p.text for p in paragraphs)
        return text[:3000]  # tronqué pour éviter les limites
    except:
        return ""

# Résumer le texte
def summarize(text):
    if not text:
        return "Résumé non disponible."
    summary = summarizer(text, max_length=120, min_length=30, do_sample=False)[0]['summary_text']
    return summary

# Traduction optionnelle
def translate(text):
    if not text:
        return ""
    return translator(text[:512])[0]['translation_text']

# Scraper les titres des news Yahoo Finance
def get_news(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}/news"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        st.error("Erreur d'accès à Yahoo Finance.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    news = []

    for a in soup.find_all('a', href=True):
        h3 = a.find('h3')
        if h3:
            title = h3.text.strip()
            link = a['href']
            news.append({'title': title, 'link': link})

    return news[:5]

# Analyse de sentiment
def analyze_sentiment(text):
    result = sentiment_model(text[:512])[0]
    return result['label'], result['score']

# Traduction
def translate_text(text):
    translation = translation_model(text[:512])[0]['translation_text']
    return translation

# Interprétation des résultats de sentiment
def get_recommendation(sentiments):
    score_map = {'positive': 1, 'neutral': 0, 'negative': -1}
    total = sum(score_map[s[0].lower()] for s in sentiments)
    if total >= 2:
        return total,"Acheter"
    elif total <= -2:
        return total, "Vendre"
    else:
        return total, "Attendre"

# ------------------- Interface Streamlit -------------------
def scrapper():
    st.title("Analyse des Actualités Financières")
    st.write("Entrez le **ticker boursier** (ex : TSLA, AAPL, MSFT) pour voir les dernières news et une suggestion d'achat basée sur l'analyse de sentiment.")

    ticker = st.text_input("Ticker boursier de l'entreprise (ex : TSLA pour Tesla)")

    if ticker:
        st.subheader(f"News pour {ticker.upper()}")
        news_list = get_news(ticker)

        if news_list:
            sentiments = []
            # Case à cocher pour activer la traduction
            translate_option = st.checkbox("Afficher la traduction en français")

            for i, article in enumerate(news_list):
                title_en = article['title']
                link = article['link']
                label, score = analyze_sentiment(title_en)
                # Récupère et résume le contenu de l’article
                full_text = get_article_text(link)
                summary_en = summarize(full_text)
                # Traduction si activée
                if translate_option:
                    title_fr = translate(title_en)
                    summary_fr = translate(summary_en)
                else:
                    title_fr = None
                    summary_fr = None


                # Affichage
                st.markdown(f"**{i+1}. {title_en}**")
                if translate_option and title_fr:
                    st.markdown(f"*Traduction :* {title_fr}")
                
                st.markdown(f"[Lire l'article complet]({link})")
                st.markdown(f"**Résumé (EN)** : {summary_en}")
                if translate_option and summary_fr:
                    st.markdown(f"**Résumé (FR)** : {summary_fr}")
                
                st.write(f"**Sentiment** : {label} ({round(score, 2)})")
                st.markdown("---")
                sentiments.append((label, score))

            total, reco = get_recommendation(sentiments)
            st.subheader(f"Recommandation finale avec un score de **{total}** : **{reco}**")
        else:
            st.warning("Aucune news trouvée pour ce ticker.")
