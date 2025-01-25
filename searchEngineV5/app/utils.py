import requests
import logging
from functools import lru_cache
TMDB_API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2OGRlZTliNDU0NzAyYTUyN2I2NGZiOTkzZGYzZWYxZiIsIm5iZiI6MTczNjA4NDU3OC40MjMsInN1YiI6IjY3N2E4YzYyODJjY2UxNWE3Njc0ZjY1ZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.vUxSHTJb17jGKbuEmtIevhN8w5MpuYPg4b2iB4Fa5PQ'

@lru_cache(maxsize=500)
def obtenir_informations_tmdb(titre):
    url = f"https://api.themoviedb.org/3/search/movie?query={titre}&include_adult=true&language=fr-US&page=1"
    headers = {
        'Authorization': f'Bearer {TMDB_API_KEY}',
        'accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    if response.status_code == 200 and data.get('results'):
        return {
            'poster': f"https://image.tmdb.org/t/p/w500{data['results'][0].get('poster_path')}",
            'title': data['results'][0].get('title'),
            'genre_ids': ', '.join(map(str, data['results'][0].get('genre_ids', []))),
            'overview': data['results'][0].get('overview'),
            'release_date': data['results'][0].get('release_date'),
            'vote_average': data['results'][0].get('vote_average'),
            'popularity': data['results'][0].get('popularity')
        }
    else:
        logging.warning(f"TMDB introuvable pour {titre}")
        return None
