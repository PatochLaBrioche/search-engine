import logging
from flask import Flask
from app.routes import init_routes
from app.tfidf_handler import initialiser_tfidf

# Configuration de la journalisation
logging.basicConfig(level=logging.INFO)

# Création de l'application Flask
app = Flask(__name__)

# Initialisation des données TF-IDF
tfidf_data = initialiser_tfidf()

# Ajout des routes
init_routes(app, tfidf_data)

if __name__ == "__main__":
    logging.info("Lancement de l'application Flask")
    app.run(debug=True)
