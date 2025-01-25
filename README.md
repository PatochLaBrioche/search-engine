    # Avec rebuild dans config
docker compose -f searchEngineV4/config/docker-compose.yml up --build

    # Sans rebuild dans config
docker compose -f config/docker-compose.yml up

    # Start en local pour test
$env:FLASK_APP = "app"
$env:FLASK_ENV = "development"  # Optionnel : active le mode développement
flask run


    # API répertoriant les films/séries et leurs infos
https://www.omdbapi.com/

omdbapi key : 9a883ce3
link exemple : http://www.omdbapi.com/?i=tt3896198&apikey=9a883ce3