import logging
import os
from flask import Flask, request, render_template
from app.preprocessing import lire_fichiers_txt
from app.tfidf_handler import calculer_tfidf, charger_tfidf
from app.search import rechercher_series

# Configuration de la journalisation
logging.basicConfig(level=logging.DEBUG)

# Création de l'application Flask
app = Flask(__name__)

dossier_racine = './data/sous-titres-cleaned'
sauvegarde_tfidf = './data/tfidf_data.pkl'

# Variables globales pour stocker la matrice TF-IDF et les autres objets
tfidf_matrix = None
termes = None
vectorizer = None
titres_series = None
corpus = None

# Charger ou recalculer TF-IDF
def initialiser_tfidf():
    global tfidf_matrix, termes, vectorizer, titres_series, corpus
    
    def initialiser_corpus_et_titres():
        logging.info("Initialisation des titres et du corpus ...")
        return lire_fichiers_txt(dossier_racine)
    
    if os.path.exists(sauvegarde_tfidf):
        logging.info("Chargement de la matrice TF-IDF depuis le fichier de sauvegarde...")
        tfidf_matrix, termes, vectorizer = charger_tfidf(sauvegarde_tfidf)
        
        if titres_series is None or corpus is None:
            corpus, titres_series = initialiser_corpus_et_titres()
    else:
        logging.info("Calcul de la matrice TF-IDF car aucun fichier de sauvegarde n'a été trouvé...")
        
        if titres_series is None or corpus is None:
            corpus, titres_series = initialiser_corpus_et_titres()
            
        tfidf_matrix, termes, vectorizer = calculer_tfidf(corpus, sauvegarde_tfidf)
    
    return tfidf_matrix, termes, vectorizer, titres_series

# Initialiser TF-IDF
tfidf_matrix, termes, vectorizer, titres_series = initialiser_tfidf()

# Routes de l'application Flask
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recherche', methods=['POST'])
def recherche():
    global corpus, titres_series
    requete = request.form['requete']
    logging.info(f"Recherche des séries pertinentes pour : '{requete}'...")
    series_trouvees = rechercher_series(requete, tfidf_matrix, vectorizer, titres_series, top_n=10, seuil=0.002)
    logging.info(f"Résultats de la recherche : {series_trouvees}")
    return render_template('resultats.html', details_series=series_trouvees)
    
# Démarrer l'application Flask si ce fichier est exécuté directement
if __name__ == '__main__':        
    logging.info("Lancement de l'application Flask")
    app.run(debug=True)
