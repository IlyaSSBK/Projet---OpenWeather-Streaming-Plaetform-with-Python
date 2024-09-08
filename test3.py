from kafka import KafkaConsumer
from kafka import KafkaProducer
from pymongo import MongoClient
import json
mongo_client = MongoClient("mongodb://localhost:27017/")  # URI MongoDB
db = mongo_client['base_villes']                          # Nom de votre base de données
collection = db['weatherData']   
consumer = KafkaConsumer(
    'weather_data',            # Remplacez par le nom de votre topic Kafka
    bootstrap_servers=['localhost:29092'],  # Remplacez par l'adresse de votre serveur Kafka
    auto_offset_reset='earliest', # Pour commencer à lire au début du topic si aucun offset n'est trouvé
    group_id='your_consumer_group', # Identifiant du groupe de consommateurs
    enable_auto_commit=True,      # Permet de commit automatiquement l'offset
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # Désérialise le message en JSON
)
for message in consumer:
    # message.value contient le message désérialisé
    print(f"Received message: {message.value}")
    
    # Insérer le message dans MongoDB
    # collection.drop()
    collection.insert_one(message.value)