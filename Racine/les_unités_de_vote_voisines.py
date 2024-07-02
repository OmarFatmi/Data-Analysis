

import pandas as pd
from math import radians, cos, sin, sqrt, atan2

# Define the Haversine formula
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    r = 6371  # Radius of Earth in kilometers
    return r * c

# Load the dataset
data = pd.read_csv('../BORNO_geocoded.CSV')

# Check if 'Latitude' and 'Longitude' columns exist
if 'Latitude' not in data.columns or 'Longitude' not in data.columns:
    raise KeyError("Latitude and Longitude columns are required in the dataset")

# Add a column for neighbors
data['Neighbors'] = None

# Define the distance limit for neighbors in kilometers
distance_limit = 1  # For example, 1 km

# Find neighbors for each polling unit
for index, row in data.iterrows():
    neighbors = []
    for idx, other_row in data.iterrows():
        if index != idx:
            dist = haversine(row['Latitude'], row['Longitude'], other_row['Latitude'], other_row['Longitude'])
            if dist <= distance_limit:
                neighbors.append(other_row['PU-Name'])
    data.at[index, 'Neighbors'] = ", ".join(neighbors)

# Save the updated dataset
data.to_csv('../BORNO_neighbors.csv', index=False)
print("Identification of neighbors completed. Data saved to BORNO_neighbors.csv.")
