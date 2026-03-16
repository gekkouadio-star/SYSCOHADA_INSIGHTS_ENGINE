#SYSCOHADA_INSIGHTS_ENGINE

BRVM Analytics Hub - Big Data Edition est une application Streamlit permettant d’analyser automatiquement les rapports financiers des entreprises de la Bourse Régionale des Valeurs Mobilières (BRVM) et de générer des visualisations et diagnostics financiers interactifs.

#Fonctionnalités

#Analyse PDF unique

Extraction automatique des données financières (Chiffre d’affaires, Résultat Net, BFR, DSO, CAF, etc.) depuis un PDF au format SYSCOHADA.

Calcul des ratios financiers : Marge nette, ROE, Gearing, etc.

Analyse de texte avec :

Nuage de mots (WordCloud)

Fréquence des mots

N-grammes (bigrams, trigrams)

Diagnostic automatique basé sur les ratios (ex. attention au BFR si DSO élevé).

#Analyse automatique BRVM

Récupération et traitement des rapports financiers directement depuis le site BRVM.

Sauvegarde automatique des données dans une base SQLite.

Possibilité de visualiser l’évolution des chiffres d’affaires de toutes les entreprises via des graphiques interactifs Plotly.

#Visualisation interactive

Graphiques dynamiques pour l’évolution du Chiffre d’Affaires par entreprise et par année.

Analyse comparative des ratios financiers entre entreprises.

#Résumé automatique

Génération d’un résumé synthétique des principaux indicateurs financiers et des points d’attention.

#Technologies utilisées

Python 3.13

Streamlit

Pandas, NumPy

Plotly

Matplotlib, WordCloud

SQLite

PDFPlumber pour l’extraction de PDF

NLTK et spaCy pour le traitement du texte