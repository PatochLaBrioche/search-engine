import numpy as np
import logging
from app.utils import obtenir_informations_tmdb

def rechercher_series(requete, tfidf_matrix, vectorizer, titres_series, top_n=10, seuil=0.002):
    # Normalisation de la requête (mettre en minuscules pour ignorer la casse)
    requete_normalise = requete.lower()
    
    # Convertir les titres de séries en minuscules pour la comparaison
    titres_series_lower = [titre.lower() for titre in titres_series]
    
    # Vérifier si le titre exact existe dans les titres de séries
    if requete_normalise in titres_series_lower:
        # Si une correspondance exacte est trouvée, le mettre en premier
        index_exact = titres_series_lower.index(requete_normalise)
        titre_exact = titres_series[index_exact]
        logging.info(f"Titre exact trouvé : {titre_exact}")
        details_exact = obtenir_informations_tmdb(titre_exact)
        return [details_exact]  # Retourner directement le résultat exact

    # Si pas de correspondance exacte, calculer la similarité cosinus
    requete_vecteur = vectorizer.transform([requete])  # Transformer la requête en vecteur
    similarite = (tfidf_matrix @ requete_vecteur.T).toarray().flatten()
    
    # Trier les séries en fonction de leur score de similarité
    series_scores = sorted(zip(similarite, titres_series), reverse=True, key=lambda x: x[0])
    series_trouvees = [(titre, score) for score, titre in series_scores if score > seuil]

    # Obtenir les informations sur les séries trouvées (jusqu'à top_n)
    details_series = [obtenir_informations_tmdb(titre) for titre, _ in series_trouvees[:top_n]]
    
    return [d for d in details_series if d]  # Retourner les détails des séries similaires