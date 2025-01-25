import requests
import logging
import json

logging.basicConfig(filename='omdb_fetcher.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def obtenir_informations_tmdb_all():
    logging.info("Début de la fonction obtenir_informations_tmdb_all")
    series = [
        "24", "90210", "alias", "angel", "Battlestar Galactica", "Better Off Ted", "Bionic Woman",
        "Blade", "Blood Ties", "Bones", "Breaking Bad", "Buffy", "Burn Notice", "Californication",
        "Caprica", "Charmed", "Chuck", "Cold Case", "Community", "Criminal Minds", "Cupid",
        "Daybreak", "Demons", "Desperate Housewives", "Dexter", "Dirt", "Dirty Sexy Money",
        "Doctor Who", "Dollhouse", "Eleventh Hour", "Entourage", "Eureka", "Extras", "Fear Itself",
        "Flashforward", "Flashpoint", "Flight of the Conchords", "Friday Night Lights", "Friends",
        "Fringe", "Futurama", "Gary Unmarried", "Ghost Whisperer", "Gossip Girl", "Greek",
        "Grey's Anatomy", "Heroes", "House", "How I Met Your Mother", "In Treatment", "Invasion",
        "Jake", "Jekyll", "Jericho", "John from Cincinnati", "Knight Rider", "Kyle XY", "Legend of the Seeker",
        "Leverage", "Lie to Me", "Life", "Lost", "Mad Men", "Masters of Sci-Fi", "Medium", "Melrose Place",
        "Mental", "Merlin", "Moonlight", "My Name is Earl", "NCIS", "NCIS Los Angeles", "Nip Tuck",
        "One Tree Hill", "Oz", "Painkiller Jane", "Primeval", "Prison Break", "Private Practice",
        "Psych", "Pushing Daisies", "Raines", "Reaper", "Robin Hood", "Rome", "Samantha Who",
        "Sanctuary", "Scrubs", "Sex and the City", "Six Feet Under", "Skins", "Smallville",
        "Sons of Anarchy", "South Park", "Spaced", "Stargate Atlantis", "Stargate SG-1", "Stargate Universe",
        "Supernatural", "Swingtown", "The 4400", "The Big Bang Theory", "The Black Donnellys",
        "The Kill Point", "The Lost Room", "The Mentalist", "The Nine", "The O.C.", "The Pretender",
        "The Riches", "The Sarah Connor Chronicles", "The Shield", "The Sopranos", "The Tudors",
        "The Vampire Diaries", "The Wire", "Torchwood", "Traveler", "Tru Calling", "True Blood",
        "Ugly Betty", "V", "Veronica Mars", "Weeds", "Whitechapel", "Women's Murder Club", "X-Files"
    ]

    
    OMDB_API_KEY = '9a883ce3'
    TMDB_API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2OGRlZTliNDU0NzAyYTUyN2I2NGZiOTkzZGYzZWYxZiIsIm5iZiI6MTczNjA4NDU3OC40MjMsInN1YiI6IjY3N2E4YzYyODJjY2UxNWE3Njc0ZjY1ZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.vUxSHTJb17jGKbuEmtIevhN8w5MpuYPg4b2iB4Fa5PQ'


    all_series_details = []
    for serie in series:
        url = f"https://api.themoviedb.org/3/search/movie?query={serie}&include_adult=true&language=fr-US&page=1"
        headers = {
            'Authorization': f'Bearer {TMDB_API_KEY}',
            'accept': 'application/json'
        }
        logging.info(f"Fetching data for {serie} from TMDB API")
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            if 'results' in data and len(data['results']) > 0:
                all_series_details.append({
                    'poster': f"https://image.tmdb.org/t/p/w500{data['results'][0].get('poster_path')}",
                    'title': data['results'][0].get('title'),
                    'genre_ids': data['results'][0].get('genre_ids'),
                    'overview': data['results'][0].get('overview'),
                    'release_date': data['results'][0].get('release_date'),
                    'vote_average': data['results'][0].get('vote_average'),
                    'popularity': data['results'][0].get('popularity')
                })
                logging.info(f"Data fetched successfully for {serie}")
            else:
                logging.warning(f"No data found for {serie}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data for {serie}: {e}")
    
    try:
        with open("series_details.json", "w", encoding="utf-8") as file:
            json.dump(all_series_details, file, ensure_ascii=False, indent=4)
        logging.info("File written successfully")
    except Exception as e:
        logging.error(f"Error writing to file: {e}")

if __name__ == "__main__":
    obtenir_informations_tmdb_all()
