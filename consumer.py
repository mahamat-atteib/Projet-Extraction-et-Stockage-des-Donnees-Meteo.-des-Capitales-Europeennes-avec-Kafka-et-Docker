##################################### CONSUMER #####################################
# Consommateur (consumer.py) :
        # Se connecte à Kafka, écoute le topic weather_data.
        # À chaque message reçu, il extrait les données et les insère dans la base MySQL.

from kafka import KafkaConsumer
import mysql.connector
import json
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()


# Première connexion à MySQL pour créer la base de données "database_name".
# Charger les variables d'environnement
# Connexion initiale pour créer la base de données si elle n'existe pas
db_init = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD")
)
cursor_init = db_init.cursor()

# Création de la base de données
cursor_init.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('MYSQL_DATABASE')}")
cursor_init.close()
db_init.close()

# Connexion MySQL avec la base de données spécifiée
# Connexion à MySQL pour créer la base de données "database_name"
# MYSQL_HOST, MYSQL_USER et MYSQL_PASSWORD seront récupérées depuis le fichier .env
db = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)
cursor = db.cursor()

# Création de la table "weather_data" avec le champ "city" pour enregistrer les données des différentes villes
cursor.execute("""
CREATE TABLE IF NOT EXISTS weather_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(50),
    temperature FLOAT,
    humidity INT,
    description VARCHAR(100),
    timestamp DOUBLE
);
""")

# Configurer le consommateur Kafka
consumer = KafkaConsumer(
    'weather_data',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    group_id='weather_group'
)

# Insérer les messages dans MySQL
for message in consumer:
    data = message.value
    sql = """
    INSERT INTO weather_data (city, temperature, humidity, description, timestamp)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (data['city'], data['temperature'], data['humidity'], data['description'], data['timestamp'])
    try:
        cursor.execute(sql, values)
        db.commit()
        print(f"Données insérées : {data}")
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'insertion des données : {err}")

