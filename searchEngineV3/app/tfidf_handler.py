import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os

def calculer_tfidf(corpus, sauvegarde_path='data/tfidf_data.pkl'):
    version_sklearn = sklearn.__version__  # Version actuelle de scikit-learn
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_df=0.95, min_df=0.01, sublinear_tf=True)
    tfidf_matrix = vectorizer.fit_transform(corpus)
    termes = vectorizer.get_feature_names_out()

    # Sauvegarder avec version de scikit-learn
    with open(sauvegarde_path, 'wb') as f:
        pickle.dump((tfidf_matrix, termes, vectorizer, version_sklearn), f)
    
    return tfidf_matrix, termes, vectorizer

def charger_tfidf(sauvegarde_path='data/tfidf_data.pkl'):
    if os.path.exists(sauvegarde_path):
        with open(sauvegarde_path, 'rb') as f:
            tfidf_matrix, termes, vectorizer, saved_version = pickle.load(f)
        
        current_version = sklearn.__version__
        if current_version != saved_version:
            raise ValueError(
                f"Version mismatch: model saved with scikit-learn {saved_version}, "
                f"current version is {current_version}. Please re-save the model."
            )
        return tfidf_matrix, termes, vectorizer
    else:
        raise FileNotFoundError(f"Aucun fichier de sauvegarde trouvé à {sauvegarde_path}")
