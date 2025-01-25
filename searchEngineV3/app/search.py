import logging
import numpy as np

# Rechercher les séries les plus pertinentes pour une requête
def rechercher_series(requete, tfidf_matrix, vectorizer, titres_series, top_n=10, seuil=0.7):
    logging.info(f"Requête de recherche : {requete}")
    
    # Transformation de la requête en vecteur TF-IDF
    requete_vecteur = vectorizer.transform([requete])
    logging.info(f"Vecteur de la requête : {requete_vecteur.toarray()}")

    # Calcul de la similarité
    similarite = tfidf_matrix.dot(requete_vecteur.T).toarray().flatten()
    logging.info(f"Similarité brute : {similarite}")

    # Utilisation d'une normalisation plus souple
    if np.max(similarite) > 0:
        similarite = similarite / (np.max(similarite) if np.max(similarite) > 0 else 1)
    logging.info(f"Similarité normalisée : {similarite}")
    
    # Tri des séries par score de similarité
    series_pertinentes = sorted(zip(similarite, titres_series), reverse=True, key=lambda x: x[0])
    logging.info(f"Séries pertinentes triées : {series_pertinentes}")

    # Filtrage des séries en fonction du seuil
    series_filtrees = [(serie, score) for score, serie in series_pertinentes if score > seuil]
    logging.info(f"Séries filtrées : {series_filtrees}")
    
    # Retourner les top_n séries
    resultats = series_filtrees[:top_n]
    logging.info(f"Résultats de la recherche : {resultats}")
    
    return resultats