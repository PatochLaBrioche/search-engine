from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os

# Calcul du TF-IDF et sauvegarde des objets si nécessaire
def calculer_tfidf(corpus, sauvegarde_path='tfidf_data.pkl'):
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_df=0.95, min_df=0.01, sublinear_tf=True)
    tfidf_matrix = vectorizer.fit_transform(corpus)
    termes = vectorizer.get_feature_names_out()

    # Sauvegarder la matrice TF-IDF et le vectorizer
    with open(sauvegarde_path, 'wb') as f:
        pickle.dump((tfidf_matrix, termes, vectorizer), f)
    
    return tfidf_matrix, termes, vectorizer

# Charger le TF-IDF et le vectorizer depuis un fichier
def charger_tfidf(sauvegarde_path='tfidf_data.pkl'):
    if os.path.exists(sauvegarde_path):
        with open(sauvegarde_path, 'rb') as f:
            tfidf_matrix, termes, vectorizer = pickle.load(f)
        return tfidf_matrix, termes, vectorizer
    else:
        raise FileNotFoundError(f"Aucun fichier de sauvegarde trouvé à {sauvegarde_path}")
