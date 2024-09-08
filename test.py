from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['base_villes']  # Remplacez par le nom de votre base de données

# Créer la collection avec un schéma de validation
try:
    db.create_collection('weatherData', validator={
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['city', 'coordinates', 'time'],  # Ajout de 'time' dans les champs requis
            'properties': {
                'city': {
                    'bsonType': 'string',
                    'description': 'must be a string and is required'
                },
                'coordinates': {
                    'bsonType': 'object',
                    'required': ['longitude', 'latitude'],
                    'properties': {
                        'longitude': {
                            'bsonType': 'double',
                            'description': 'must be a double and is required'
                        },
                        'latitude': {
                            'bsonType': 'double',
                            'description': 'must be a double and is required'
                        }
                    }
                },
                'time': {  # Ajout du champ time
                    'bsonType': 'date',
                    'description': 'must be a date and is required'
                }
            }
        }
    })

    print("Collection 'weatherData' créée avec un schéma de validation.")
except Exception as e:
    print(f"Erreur lors de la création de la collection : {e}")
