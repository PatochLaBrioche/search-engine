import os

# Fonction d'enregistrement des résultats
def enregistrer_resultats(series_trouvees, dossier_racine, requete):
    chemin_fichier_resultat = os.path.join(dossier_racine, '.result.txt')
    with open(chemin_fichier_resultat, 'w', encoding='utf-8') as f_resultat:
        f_resultat.write(f"Résultats de recherche pour la requête: '{requete}'\n")
        f_resultat.write(f"{len(series_trouvees)} résultats trouvés:\n\n")
        for i, (serie, score) in enumerate(series_trouvees, 1):
            f_resultat.write(f"{i}. {serie} (Score de pertinence: {score:.4f})\n")
    print(f"Résultats enregistrés dans {chemin_fichier_resultat}")
