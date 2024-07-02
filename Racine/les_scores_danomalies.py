import pandas as pd

# Define the function to calculate the outlier score
def calculate_outlier_score(vote_count, neighbor_counts):
    if len(neighbor_counts) == 0:
        return 0  # No neighbors, no outlier score
    neighbor_mean = sum(neighbor_counts) / len(neighbor_counts)
    if neighbor_mean == 0:
        return 0  # Avoid division by zero if the mean of neighbors is zero
    return abs(vote_count - neighbor_mean) / neighbor_mean

# Load the dataset
data = pd.read_csv('../BORNO_neighbors.csv')

# Assume the columns for party results are "APC", "LP", "PDP", "NNPP"
party_columns = ['APC', 'LP', 'PDP', 'NNPP']

# Check if party columns exist
for party in party_columns:
    if party not in data.columns:
        raise KeyError(f"{party} column is required in the dataset")

# Add columns for the outlier scores
for party in party_columns:
    data[f'{party}_Outlier_Score'] = None

# Calculate the outlier scores
for index, row in data.iterrows():
    neighbors = row['Neighbors']
    if isinstance(neighbors, str):
        neighbors = neighbors.split(', ')
        for party in party_columns:
            neighbor_counts = data[data['PU-Name'].isin(neighbors)][party].tolist()
            outlier_score = calculate_outlier_score(row[party], neighbor_counts)
            data.at[index, f'{party}_Outlier_Score'] = outlier_score
    else:
        for party in party_columns:
            data.at[index, f'{party}_Outlier_Score'] = 0  # No neighbors, so no outlier score

# Save the updated dataset
data.to_csv('../BORNO_outliers.csv', index=False)
print("Outlier score calculation completed. Data saved to BORNO_outliers.csv.")
