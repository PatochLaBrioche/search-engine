import numpy as np
import requests

# Fonction de recherche des séries avec appel à l'API OMDB
def rechercher_series(requete, tfidf_matrix, vectorizer, titres_series, top_n, seuil):
    requete_vecteur = vectorizer.transform([requete])
    similarite = tfidf_matrix.dot(requete_vecteur.T).toarray().flatten()
    if similarite.max() > 0:
        similarite /= similarite.max()
    series_scores = list(zip(similarite, titres_series))
    series_exactes = [(titre, 1.0) for titre in titres_series if titre.lower() == requete.lower()]
    series_pertinentes = sorted(series_scores, key=lambda x: x[0], reverse=True)
    series_filtrees = [(titre, score) for score, titre in series_pertinentes if score > seuil]
    series_finales = series_exactes + [s for s in series_filtrees if s not in series_exactes]
    
    # Récupérer les informations OMDB pour chaque série trouvée
    series_details = []
    for titre, score in series_finales[:top_n]:
        details = obtenir_informations_omdb(titre)
        if details:
            series_details.append({
                'title': details['title'],
                'year': details['year'],
                'rated': details['rated'],
                'runtime': details['runtime'],
                'genre': details['genre'],
                'director': details['director'],
                'plot': details['plot'],
                'poster': details['poster'],
                'metascore': details['metascore'],
                'type': details['type']
            })
    
    # Si une seule série est trouvée, recommander des séries similaires
    if len(series_finales) == 1:
        série_trouvée = series_finales[0][0]
        recommandations = recommander_series_similaires(série_trouvée, tfidf_matrix, vectorizer, titres_series, top_n)
        for titre, score in recommandations:
            details = obtenir_informations_omdb(titre)
            if details:
                series_details.append({
                    'title': details['title'],
                    'year': details['year'],
                    'rated': details['rated'],
                    'runtime': details['runtime'],
                    'genre': details['genre'],
                    'director': details['director'],
                    'plot': details['plot'],
                    'poster': details['poster'],
                    'metascore': details['metascore'],
                    'type': details['type']
                })
    
    return series_details

# Fonction pour recommander des séries similaires lorsqu'une seule série est trouvée
def recommander_series_similaires(série_trouvée, tfidf_matrix, vectorizer, titres_series, top_n=5):
    # Trouver l'index de la série trouvée dans la liste des titres
    index_serie_trouvee = titres_series.index(série_trouvée)
    
    # Récupérer le vecteur TF-IDF de la série trouvée
    serie_trouvee_vecteur = tfidf_matrix[index_serie_trouvee]
    
    # Calculer les similarités cosinus entre cette série et toutes les autres séries
    similarites = (tfidf_matrix @ serie_trouvee_vecteur.T).toarray().flatten()
    
    # Trier les séries par similarité décroissante
    series_scores = list(zip(similarites, titres_series))
    series_scores_sorted = sorted(series_scores, key=lambda x: x[0], reverse=True)
    
    # Exclure la série trouvée elle-même des recommandations
    recommendations = [(titre, score) for score, titre in series_scores_sorted if titre != série_trouvée]
    
    # Limiter les résultats au nombre top_n
    return recommendations[:top_n]

# Fonction pour récupérer les informations via l'API OMDB
def obtenir_informations_omdb(titre):
    OMDB_API_KEY = '9a883ce3'
    url = f"http://www.omdbapi.com/?t={titre}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data['Response'] == 'True':
        return {
            'title': data.get('Title'),
            'year': data.get('Year'),
            'rated': data.get('Rated'),
            'runtime': data.get('Runtime'),
            'genre': data.get('Genre'),
            'director': data.get('Director'),
            'plot': data.get('Plot'),
            'poster': data.get('Poster'),
            'metascore': data.get('Metascore'),
            'type': data.get('Type')
        }
    else:
        return None