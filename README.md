# Projet : Recupération et Stockage des Données Météorologiques des Capitales Européennes avec Kafka et Docker

Ce projet utilise Kafka et Docker pour récupérer les données météorologiques en temps réel des capitales européennes. Les données sont envoyées à un consommateur Kafka qui les stocke ensuite dans une base de données MySQL. Les informations météorologiques sont obtenues via l'API d'OpenWeather, puis publiées dans un topic Kafka, permettant leur traitement en temps réel.

Le but de ce projet est de :
Récupérer les données météorologiques en temps réel pour les capitales européennes via l'API d'OpenWeather.
Publier les données dans un topic Kafka (weather_data).
Consommer les données de ce topic et les stocker dans une base de données MySQL pour analyse ultérieure.

## Technologies Utilisées
Python : pour le développement du producteur et du consommateur.\
Kafka : pour la gestion du flux de données en temps réel.\
MySQL : pour stocker les données météorologiques.\
OpenWeather API : pour obtenir les informations météorologiques.\
Docker : pour déployer Kafka, Zookeeper, et MySQL dans des conteneurs.\
dotenv : pour gérer les variables d'environnement de manière sécurisée.


## Prérequis
Compte sur OpenWeather pour obtenir une clé API.
Docker et Docker Compose installés.
Python 3.x installé.

## fichier .env
API_KEY=votre_cle_api_openweather
MYSQL_USER=root
MYSQL_PASSWORD=1234
MYSQL_HOST=localhost
MYSQL_DATABASE=database_name
En fait, 
API_KEY : votre clé API OpenWeather.
MYSQL_USER : nom d'utilisateur MySQL.
MYSQL_PASSWORD : mot de passe MySQL.
MYSQL_HOST : hôte MySQL (en général, localhost).
MYSQL_DATABASE : nom de la base de données MySQL pour stocker les données météorologiques.


## Lancer Docker Compose :
Déployez Kafka, Zookeeper et MySQL en utilisant Docker Compose :
docker-compose up -d
![commandes_bash](https://github.com/user-attachments/assets/56507457-db2d-4903-a65f-255e232cdd46)

## Utilisation

### Lancer le Producteur :
Le producteur récupère les données météorologiques de chaque capitale européenne et les publie dans Kafka.
python producer.py
![execution_producer](https://github.com/user-attachments/assets/c5eb15bf-e034-4572-b3c8-1dbca849779b)

### Lancer le Consommateur :
Le consommateur lit les messages du topic Kafka weather_data et insère les données dans la base de données MySQL.
python consumer.py
![execution_consumer](https://github.com/user-attachments/assets/274ca39f-cfb4-4839-90d8-e8026b08e20b)

Enfin, je suis allé sur pour s'assurer que la base de donnée a été bien créée et les données sont insérées en faisant une 
requête simple "select * from weather_data"
![test_requêtes_SQL](https://github.com/user-attachments/assets/481d2108-7ca4-4549-b349-6035ae70e0ec)

## Vos contributions sont les bienvenues !



