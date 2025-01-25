import pickle
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from app.preprocessing import lire_fichiers_txt
from pathlib import Path

# Chemins des fichiers
DOSSIER_RACINE = Path('./data/sous-titres-cleaned')
SAUVEGARDE_TFIDF = Path('./data/tfidf_data.pkl')

def initialiser_tfidf():
    if SAUVEGARDE_TFIDF.exists():
        logging.info("Chargement du modèle TF-IDF...")
        return charger_tfidf()
    
    logging.info("Calcul du modèle TF-IDF...")
    corpus, titres_series = lire_fichiers_txt(DOSSIER_RACINE)
    return calculer_tfidf(corpus, titres_series)

def calculer_tfidf(corpus, titres_series):
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_df=0.95, min_df=0.01)
    tfidf_matrix = vectorizer.fit_transform(corpus)
    termes = vectorizer.get_feature_names_out()

    # Sauvegarde
    with SAUVEGARDE_TFIDF.open('wb') as f:
        pickle.dump((tfidf_matrix, termes, vectorizer, titres_series), f)
    
    return tfidf_matrix, termes, vectorizer, titres_series

def charger_tfidf():
    with SAUVEGARDE_TFIDF.open('rb') as f:
        return pickle.load(f)