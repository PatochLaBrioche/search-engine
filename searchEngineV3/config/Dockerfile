# Utilisation de l'image de base Python 3.10
FROM python:3.10-slim

# Définir le répertoire de travail à /app
WORKDIR /app

# Copier les dépendances du fichier requirements.txt
COPY config/requirements.txt /app/requirements.txt

# Installer les dépendances
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copier tous les fichiers du projet dans le conteneur
COPY . /app/

# Télécharger les stopwords pour NLTK (si nécessaire pour TF-IDF)
RUN python -m nltk.downloader stopwords

# Exposer le port 5000 pour Flask
EXPOSE 5000

# Définir la commande par défaut pour exécuter l'application Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--debug"]