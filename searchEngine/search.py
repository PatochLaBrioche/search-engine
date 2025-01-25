import numpy as np

# Rechercher les séries les plus pertinentes pour une requête
def rechercher_series(requete, tfidf_matrix, vectorizer, titres_series, top_n=10, seuil=0.001):
    requete_vecteur = vectorizer.transform([requete])
    similarite = tfidf_matrix.dot(requete_vecteur.T).toarray().flatten()
    similarite = similarite / np.max(similarite) if np.max(similarite) > 0 else similarite
    series_pertinentes = sorted(zip(similarite, titres_series), reverse=True, key=lambda x: x[0])
    series_filtrees = [(serie, score) for score, serie in series_pertinentes if score > seuil]
    return series_filtrees[:top_n]
