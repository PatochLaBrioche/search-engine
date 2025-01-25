import logging
import os
from flask import Flask, request, render_template
from app.preprocessing import lire_fichiers_txt
from app.tfidf_handler import calculer_tfidf, charger_tfidf
from app.search import rechercher_series

# Configuration de la journalisation
logging.basicConfig(level=logging.INFO)

# Création de l'application Flask
app = Flask(__name__)

dossier_racine = './data/sous-titres-cleaned'
sauvegarde_tfidf = './data/tfidf_data.pkl'

# Variables globales pour stocker la matrice TF-IDF et les autres objets
tfidf_matrix = None
termes = None
vectorizer = None
titres_series = None

# Charger ou recalculer TF-IDF
def initialiser_tfidf():
    global tfidf_matrix, termes, vectorizer, titres_series
    if tfidf_matrix is not None:
        return tfidf_matrix, termes, vectorizer, titres_series

    if os.path.exists(sauvegarde_tfidf):
        logging.info("Chargement de la matrice TF-IDF depuis le fichier de sauvegarde...")
        tfidf_matrix, termes, vectorizer = charger_tfidf(sauvegarde_tfidf)
    else:
        logging.info("Calcul de la matrice TF-IDF car aucun fichier de sauvegarde n'a été trouvé...")
        corpus, titres_series = lire_fichiers_txt(dossier_racine)
        tfidf_matrix, termes, vectorizer = calculer_tfidf(corpus, sauvegarde_tfidf)

    return tfidf_matrix, termes, vectorizer, titres_series

# Initialiser TF-IDF
tfidf_matrix, termes, vectorizer, titres_series = initialiser_tfidf()

# Vérifier si titres_series est vide et le recalculer si nécessaire
if titres_series is None:
    corpus, titres_series = lire_fichiers_txt(dossier_racine)

# Routes de l'application Flask

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recherche', methods=['POST'])
def recherche():
    requete = request.form['requete']
    resultats = rechercher_series(requete, tfidf_matrix, vectorizer, titres_series)
    logging.info(f"Requête de recherche : {requete}")
    return render_template('resultats.html', details_series=resultats)

# Démarrer l'application Flask si ce fichier est exécuté directement
if __name__ == '__main__':
    logging.info("Lancement de l'application Flask")
    logging.info("Mode debug : activé")
    logging.info("Application disponible à l'adresse : http://127.0.0.1:5000")
    app.run(debug=True)
