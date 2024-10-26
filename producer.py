##################################### PRODUCER #####################################
# Producteur (producer.py) :
        # Se connecte à l'API OpenWeather.
        # Récupère les données météo et les publie dans le topic weather_data de Kafka.

# Import des bibliothèques nécessaires
import requests
from kafka import KafkaProducer
import json
import time
from dotenv import load_dotenv
import os

# Dans le producer, on envoie une requête pour récupérer les données météorologiques de la ville spécifiée.
# Les données sont sous format JSON puis converties en un dictionnaire Python avant d'être envoyées à Kafka.  

# Charger les variables d'environnement
load_dotenv()

# Clé API pour OpenWeather
API_KEY = os.getenv("API_KEY")      # la clé sera récupérée depuis le fichier .env

# Liste des capitales européennes
capitales = [
    "Paris", "Berlin", "Madrid", "Rome", "Vienna", "Lisbon", "Athens", 
    "Brussels", "Amsterdam", "Warsaw", "Dublin", "Prague", "Stockholm", 
    "Helsinki", "Oslo", "Copenhagen", "Luxembourg", "Tallinn", "Riga", 
    "Vilnius", "Budapest", "Sofia", "Bucharest", "Zagreb", "Ljubljana", 
    "Nicosia", "Valletta", "Bern", "Minsk"
]

# Configurer Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Fonction pour récupérer et envoyer les données météo de plusieurs capitales
def fetch_weather_data():
    while True:
        for city in capitales:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    'city': data['name'],
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'description': data['weather'][0]['description'],
                    'timestamp': time.time()
                }
                # Envoi des données de chaque ville à Kafka
                producer.send('weather_data', value=weather_data)
                print(f"Données envoyées pour {city} : {weather_data}")
            else:
                print(f"Erreur lors de la récupération des données pour {city} :", response.status_code)
            
            # Attendre 5 secondes avant de passer à la ville suivante pour éviter de surcharger l'API
            time.sleep(5)
        
        # Attendre 10 minutes avant de récupérer à nouveau les données
        time.sleep(600)

if __name__ == "__main__":
    fetch_weather_data()
