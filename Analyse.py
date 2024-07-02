file_path = '../BORNO_neighbors.csv'

import pandas as pd

# Load the dataset and check columns
data = pd.read_csv(file_path)
print(data.columns)
