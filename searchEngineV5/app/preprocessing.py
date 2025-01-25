import os
import re
import logging
from pathlib import Path
import nltk
from nltk.corpus import stopwords

# Télécharger les stopwords si nécessaire
nltk.download('stopwords')
stop_words = set(stopwords.words('french') + stopwords.words('english'))

# Nettoyage des textes
def nettoyer_texte(texte):
    texte = re.sub(r'<[^>]+>', '', texte)
    texte = re.sub(r'[^\w\s]', '', texte)
    mots = texte.lower().split()
    return ' '.join([mot for mot in mots if mot not in stop_words and len(mot) > 2])

# Lecture des fichiers sous-titres
def lire_fichiers_txt(dossier_racine):
    corpus, titres_series = [], []
    for fichier in Path(dossier_racine).glob("*.txt"):
        try:
            with fichier.open('r', encoding='utf-8') as f:
                texte = nettoyer_texte(f.read())
            corpus.append(texte)
            titres_series.append(fichier.stem)
        except Exception as e:
            logging.warning(f"Impossible de lire {fichier}: {e}")
    return corpus, titres_series
