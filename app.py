import streamlit as st
import pandas as pd
import pdfplumber
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import requests
from io import BytesIO
import sqlite3

from finance_parser import extract_finance_syscohada
from text_analysis import clean_text, tokenize_corpus, word_frequencies, ngrams
from ratios import compute_ratios
from brvm_scraper import get_brvm_reports
from database import save_financials, initialize_db

# ------------------- INITIALISATION BASE -------------------
initialize_db()  # Crée la table financials si elle n'existe pas

# ------------------- CONFIG -------------------
st.set_page_config(page_title="BRVM Analytics Hub", layout="wide")
st.title("BRVM Analytics Hub - Big Data Edition")

# ------------------- Sidebar -------------------
st.sidebar.title("Options")
mode = st.sidebar.selectbox("Mode", ["Analyse PDF unique", "Analyse automatique BRVM"])

# ------------------- FONCTION DE FORMATAGE MONÉTAIRE -------------------
def format_fcfa(amount):
    """
    Formate un montant pour indiquer automatiquement FCFA, millions ou milliards.
    """
    if amount >= 1_000_000_000:
        return f"{round(amount/1_000_000_000,2)} milliards FCFA"
    elif amount >= 1_000_000:
        return f"{round(amount/1_000_000,2)} millions FCFA"
    else:
        return f"{amount} FCFA"

# ------------------- FONCTION DE RÉSUMÉ -------------------
def generate_summary(data, ratios, corpus):
    """
    Génère un résumé automatique d'un rapport financier.
    """
    summary = f"Chiffre d'affaires : {format_fcfa(data['CA'])}\n"
    summary += f"Résultat net : {format_fcfa(data['RN'])}\n"
    summary += f"Marge nette : {round(ratios['marge_nette'],2)} %\n"
    summary += f"BFR : {format_fcfa(data['BFR'])}\n"
    summary += f"DSO : {round(data['DSO'],1)}\n"
    summary += f"ROE : {round(ratios.get('roe',0),2)}\n"
    summary += f"Gearing : {round(ratios.get('gearing',0),2)}\n\n"

    # Mots les plus fréquents
    freq = word_frequencies(pd.Series(corpus))
    top_words = ", ".join(freq.head(5).index.tolist())
    summary += f"Mots les plus fréquents : {top_words}\n"

    return summary

# ------------------- MODE PDF UNIQUE -------------------
if mode == "Analyse PDF unique":
    file = st.sidebar.file_uploader("Upload PDF", type=["pdf"])
    
    if file:
        # Extraction texte
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

        # Analyse financière
        data = extract_finance_syscohada(text)
        ratios = compute_ratios(data)
        corpus = [clean_text(text)]

        # Affichage
        st.subheader("Analyse financière")
        st.metric("Chiffre d'affaires", format_fcfa(data["CA"]))
        st.metric("Résultat net", format_fcfa(data["RN"]))
        st.metric("Marge nette (%)", round(ratios["marge_nette"], 2))
        st.write("BFR :", format_fcfa(data["BFR"]))
        st.write("DSO :", round(data["DSO"],1))
        st.write("ROE :", round(ratios.get("roe",0),2))
        st.write("Gearing :", round(ratios.get("gearing",0),2))

        # Sauvegarde dans SQLite
        save_financials(data, company_name="Entreprise PDF", year=2025)

        # Analyse texte
        st.subheader("Analyse texte")
        freq = word_frequencies(pd.Series(corpus))
        st.write(freq.head(20))

        # WordCloud
        wc = WordCloud(width=800, height=400).generate(" ".join(corpus))
        fig, ax = plt.subplots()
        ax.imshow(wc)
        ax.axis("off")
        st.pyplot(fig)

        # N-grammes
        st.subheader("N-grammes")
        bigrams = ngrams(pd.Series(corpus), 2)
        st.write(bigrams[:10])

        # Diagnostic automatique
        st.subheader("Diagnostic automatique")
        diag = ""
        if data["DSO"] > 90:
            diag += "⚠ Les clients paient lentement, attention au BFR.\n"
        if data["CAF"] < 0:
            diag += "⚠ Flux de trésorerie négatif, risque de liquidité.\n"
        if ratios["marge_nette"] < 5:
            diag += "ℹ Marge nette faible, améliorer l’efficacité.\n"
        st.text(diag)

        # Résumé automatique
        st.subheader("Résumé automatique du rapport")
        st.text(generate_summary(data, ratios, corpus))

# ------------------- MODE ANALYSE AUTOMATIQUE BRVM -------------------
elif mode == "Analyse automatique BRVM":
    st.subheader("Scraper et analyse de tous les PDF BRVM")
    url = st.text_input("URL page rapports BRVM", "https://www.brvm.org/fr/financial-reports")

    def download_pdf_text(pdf_url):
        try:
            r = requests.get(pdf_url)
            r.raise_for_status()
            pdf_file = BytesIO(r.content)
            text = ""
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
            return text
        except:
            return ""

    if st.button("Lancer l'analyse automatique"):
        pdf_links = get_brvm_reports(url)
        st.write(f"{len(pdf_links)} rapports trouvés")
        for pdf_url in pdf_links[:5]:  # limiter pour test
            st.write("Analyse :", pdf_url)
            text = download_pdf_text(pdf_url)
            if text:
                data = extract_finance_syscohada(text)
                ratios = compute_ratios(data)
                corpus = [clean_text(text)]
                
                # Affichage
                st.write(data)
                st.write(ratios)
                
                # Sauvegarde
                save_financials(data, company_name="Nom société", year=2025)
                
                # Résumé automatique
                st.subheader("Résumé automatique du rapport")
                st.text(generate_summary(data, ratios, corpus))

        st.success("Analyse automatique terminée !")

# ------------------- VISUALISATION INTERACTIVE -------------------
st.subheader("Visualisation interactive des entreprises")
conn = sqlite3.connect("brvm_data.db")
df = pd.read_sql("SELECT * FROM financials", conn)

# Vérification colonnes
for col in ["company", "year", "CA"]:
    if col not in df.columns:
        df[col] = None

df["year"] = pd.to_numeric(df["year"], errors="coerce")
df["CA"] = pd.to_numeric(df["CA"], errors="coerce")
df = df.dropna(subset=["year", "CA"])

if not df.empty:
    fig = px.line(df, x="year", y="CA", color="company", markers=True,
                  title="Évolution du Chiffre d'Affaires par entreprise")
    st.plotly_chart(fig)
else:
    st.warning("Aucune donnée valide pour tracer le graphique !")