import os
import re
import nltk
from nltk.corpus import stopwords

# Télécharger les stopwords si nécessaire
nltk.download('stopwords')
stop_words_fr = set(stopwords.words('french'))
stop_words_en = set(stopwords.words('english'))

# Fonction de nettoyage des textes
def nettoyer_texte(texte):
    texte = re.sub(r'<[^>]+>', '', texte)  # Supprime les balises HTML
    texte = re.sub(r'[^\w\s]', '', texte)  # Supprime la ponctuation
    mots = texte.lower().split()
    mots_filtres = [mot for mot in mots if mot not in stop_words_fr and mot not in stop_words_en]
    return ' '.join(mots_filtres)

# Fonction pour lire et nettoyer les fichiers
def lire_fichiers_txt(dossier_racine):
    corpus = []
    titres_series = []
    for fichier in os.listdir(dossier_racine):
        if fichier.endswith('.txt') and not fichier.startswith('.'):  # Ignorer les fichiers cachés
            chemin_fichier = os.path.join(dossier_racine, fichier)
            encodages = ['utf-8', 'latin1', 'iso-8859-1']
            for encodage in encodages:
                try:
                    with open(chemin_fichier, 'r', encoding=encodage) as f:
                        texte = f.read()
                        break
                except UnicodeDecodeError:
                    continue
            texte_nettoye = nettoyer_texte(texte)
            corpus.append(texte_nettoye)
            titres_series.append(fichier.rsplit('.', 1)[0])
    return corpus, titres_series
