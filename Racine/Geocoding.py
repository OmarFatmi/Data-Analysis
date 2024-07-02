import pandas as pd
import requests
import time
from urllib.parse import quote

# Fonction pour obtenir des coordonnées à partir de l'API OpenStreetMap Nominatim
def get_coordinates_nominatim(address):
    base_url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': address,
        'format': 'json',
        'limit': 1
    }
    try:
        response = requests.get(base_url, params=params, headers={'User-Agent': 'MyGeocodingApp/1.0 (email@example.com)'})
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        if data:  # Check if the data is not empty
            location = data[0]
            return location['lat'], location['lon']
        else:
            print(f"No results for '{address}'")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching coordinates for '{address}': {e}")
        return None, None

# Fonction pour nettoyer et formater les adresses
def clean_address(address):
    address = address.strip()  # Supprimer les espaces en trop
    address = address.replace('PRI. SCH.', 'Primary School')  # Remplacer les abréviations courantes
    return address

# Charger les données depuis le fichier CSV
data = pd.read_csv('../BORNO_crosschecked.csv')

# Ajouter de nouvelles colonnes pour latitude et longitude
data['Latitude'] = None
data['Longitude'] = None

# Géocoder chaque unité de vote
for index, row in data.iterrows():
    address = clean_address(f"{row['PU-Name']}, {row['Ward']}, {row['LGA']}, {row['State']}, Nigeria")
    lat, lng = get_coordinates_nominatim(address)
    if not lat or not lng:  # Si l'adresse complète ne donne pas de résultat, essayer des composants
        address = clean_address(f"{row['Ward']}, {row['LGA']}, {row['State']}, Nigeria")
        lat, lng = get_coordinates_nominatim(address)
    if not lat or not lng:  # Encore si pas de résultat, essayer avec seulement LGA et State
        address = clean_address(f"{row['LGA']}, {row['State']}, Nigeria")
        lat, lng = get_coordinates_nominatim(address)
    data.at[index, 'Latitude'] = lat
    data.at[index, 'Longitude'] = lng
     # Pour éviter de dépasser la limite de requêtes de l'API

    # Afficher le progrès (optionnel)
    print(f"Géocodage de '{address}' - Latitude: {lat}, Longitude: {lng}")

# Enregistrer le jeu de données mis à jour
data.to_csv('../BORNO_geocoded.csv', index=False)

print("Géocodage terminé. Données enregistrées dans BORNO_geocoded.csv.")

