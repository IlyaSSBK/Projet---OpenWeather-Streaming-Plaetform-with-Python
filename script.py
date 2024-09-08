import requests
from kafka import KafkaProducer
import json
import time
from datetime import datetime
# Configurations
OPENWEATHER_API_KEY = '14736f736c45f15b57ca443545f75436'  
KAFKA_BROKER = 'localhost:29092'
KAFKA_TOPIC = 'weather_data'

# Initialiser le producteur Kafka
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    request_timeout_ms=60000,
)

# Fonction pour obtenir des données météorologiques
def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
        return response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None
dict_cities={"cities":[]}


# Charger les données dans Kafka
def load_data_to_kafka(city):
    weather_data = get_weather_data(city)
    
    if weather_data:
        try:
              # Assure que tous les messages sont envoyés
            dic={
                "city": weather_data['name'],
                "time":datetime.now().strftime("%H:%M"),
                "coordinates": {
                    "longitude": weather_data['coord']['lon'],
                    "latitude": weather_data['coord']['lat']
                },
                "weather": {
                    "description": weather_data['weather'][0]['description'],
                    "temperature": weather_data['main'],
                },
                "wind": weather_data['wind'],
                "country":weather_data['sys']['country'] ,
                #"timezone": weather_data['timezone']
                
            }
            producer.send(KAFKA_TOPIC,dic)
            producer.flush()
            print(f"Data sent to Kafka: {dic}")
        except Exception as e:
            print(f"An error occurred while sending data to Kafka: {e}")
    else:
        print("No weather data to send.")

# Exemple d'utilisation
POLL_INTERVAL = 10
while True:
    city = 'Paris'
    load_data_to_kafka(city)
    time.sleep(POLL_INTERVAL)


