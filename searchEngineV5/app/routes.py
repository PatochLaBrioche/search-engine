import logging
from flask import request, render_template, Blueprint, current_app
from app.search import rechercher_series

bp = Blueprint('routes', __name__)

def init_routes(app, tfidf_data):
    app.register_blueprint(bp)
    app.config['TFIDF_DATA'] = tfidf_data

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/recherche', methods=['POST'])
def recherche():
    requete = request.form['requete']
    tfidf_matrix, termes, vectorizer, titres_series = current_app.config['TFIDF_DATA']
    
    logging.info(f"Recherche des séries pour : '{requete}'...")
    
    # Recherche des séries correspondantes
    series_trouvees = rechercher_series(requete, tfidf_matrix, vectorizer, titres_series, top_n=10, seuil=0.002)

    # Si aucun résultat n'est trouvé (en cas d'absence de correspondance ou de similitude), afficher un message
    if not series_trouvees:
        logging.warning(f"Aucune série trouvée pour '{requete}'")
    
    return render_template('resultats.html', details_series=series_trouvees)
