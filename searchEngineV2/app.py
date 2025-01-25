from preprocessing import lire_fichiers_txt
from tfidf_handler import calculer_tfidf, charger_tfidf
from search import rechercher_series
from utils import enregistrer_resultats
import os

dossier_racine = './sous-titres-cleaned'
sauvegarde_tfidf = 'tfidf_data.pkl'

# Charger ou recalculer TF-IDF
def initialiser_tfidf():
    if os.path.exists(sauvegarde_tfidf):
        print("Chargement de la matrice TF-IDF depuis le fichier de sauvegarde...")
        tfidf_matrix, termes, vectorizer = charger_tfidf(sauvegarde_tfidf)
        return tfidf_matrix, termes, vectorizer, None
    else:
        print("Calcul de la matrice TF-IDF car aucun fichier de sauvegarde n'a été trouvé...")
        corpus, titres_series = lire_fichiers_txt(dossier_racine)
        tfidf_matrix, termes, vectorizer = calculer_tfidf(corpus, sauvegarde_tfidf)
        return tfidf_matrix, termes, vectorizer, titres_series

# Initialiser TF-IDF
tfidf_matrix, termes, vectorizer, titres_series = initialiser_tfidf()

# Vérifier si titres_series est vide et le recalculer si nécessaire
if titres_series is None:
    corpus, titres_series = lire_fichiers_txt(dossier_racine)

# Requête utilisateur
def lancer_recherche():
    requete = input("Entrez votre requête : ")
    print(f"Recherche des séries pertinentes pour : '{requete}'...")
    series_trouvees = rechercher_series(requete, tfidf_matrix, vectorizer, titres_series, top_n=10, seuil=0.002)
    for i, (serie, score) in enumerate(series_trouvees, 1):
        print(f"{i}. {serie} (Score de pertinence: {score:.4f})")
    enregistrer_resultats(series_trouvees, dossier_racine, requete)

# Menu principal
if __name__ == "__main__":
    while True:
        print("\nOptions :")
        print("1. Lancer une recherche")
        print("2. Recalculer et sauvegarder TF-IDF (si le corpus a changé)")
        print("3. Quitter")
        choix = input("Choisissez une option : ")
        
        if choix == "1":
            lancer_recherche()
        elif choix == "2":
            corpus, titres_series = lire_fichiers_txt(dossier_racine)
            tfidf_matrix, termes, vectorizer = calculer_tfidf(corpus, sauvegarde_tfidf)
            print("TF-IDF recalculé et sauvegardé.")
        elif choix == "3":
            print("À bientôt !")
            break
        else:
            print("Option invalide. Réessayez.")
