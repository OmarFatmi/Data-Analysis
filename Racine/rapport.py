import pandas as pd
import matplotlib.pyplot as plt

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

# Generate text report
report = "Rapport des scores d'anomalies des partis politiques\n"
report += "="*50 + "\n"
for party in party_columns:
    max_outlier_index = data[f'{party}_Outlier_Score'].idxmax()
    max_outlier_row = data.loc[max_outlier_index]
    report += f"\nParti : {party}\n"
    report += f"Unité de vote avec l'anomalie la plus élevée : {max_outlier_row['PU-Name']}\n"
    report += f"Score d'anomalie : {max_outlier_row[f'{party}_Outlier_Score']}\n"
    report += "-"*50 + "\n"

# Save the text report
with open('../anomaly_report.txt', 'w') as file:
    file.write(report)

print("Rapport texte généré et enregistré dans anomaly_report.txt")

# Generate anomaly scores plot
plt.figure(figsize=(10, 6))
for party in party_columns:
    plt.plot(data['PU-Name'], data[f'{party}_Outlier_Score'], label=party)

plt.xlabel('Unité de vote')
plt.ylabel('Score d\'anomalie')
plt.title('Scores d\'anomalie des partis politiques par unité de vote')
plt.legend()
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig('../anomaly_scores.png')
plt.show()

print("Graphique des scores d'anomalie généré et enregistré dans anomaly_scores.png")
