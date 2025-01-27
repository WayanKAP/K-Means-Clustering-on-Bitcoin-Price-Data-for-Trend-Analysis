# -*- coding: utf-8 -*-
"""K-Means Clustering on Bitcoin Price Data for Trend Analysis

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1oRw9bcnwynmc4CEZNLIz2vfHGMTOg9nG
"""

# Import necessary libraries
import pandas as pd
from google.colab import files

# Session 1: Upload the dataset
uploaded = files.upload()

# Load the dataset (assuming it's a CSV file)
file_name = list(uploaded.keys())[0]  # Get the uploaded file name
data = pd.read_csv(file_name)

# Show the first few rows to verify that it's loaded correctly
data.head()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import silhouette_score

# Load the dataset (adjust the file path if necessary)
data = pd.read_csv('btc-usd-max.csv')

# Ensure that 'snapped_at' is in datetime format
data['snapped_at'] = pd.to_datetime(data['snapped_at'])

# Display the first few rows to verify the dataset
print(data.head())

# Extract the relevant features for clustering (e.g., 'price')
X = data[['price']]

# Normalize the data using MinMaxScaler for better clustering performance
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Elbow Method to determine the optimal number of clusters
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=42)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)

# Plot the Elbow Method graph
plt.figure(figsize=(10, 5))
plt.plot(range(1, 11), wcss, marker='o', color='b')
plt.title('Elbow Method for Optimal K')
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS')
plt.show()

# Choose the optimal number of clusters based on the Elbow method (e.g., 3 clusters)
optimal_clusters = 3

# Perform K-Means clustering with the chosen number of clusters
kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)
data['Cluster'] = kmeans.fit_predict(X_scaled)

# Visualize the clusters with a scatter plot
plt.figure(figsize=(10, 5))
plt.scatter(data['snapped_at'], data['price'], c=data['Cluster'], cmap='viridis')
plt.title('K-Means Clustering of Bitcoin Prices')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.show()

# Print the cluster centroids (prices)
print("Cluster Centroids (Price):")
print(scaler.inverse_transform(kmeans.cluster_centers_))

# Calculate accuracy and error rate (for demonstration, using silhouette score as a proxy for accuracy)
silhouette_avg = silhouette_score(X_scaled, data['Cluster'])
accuracy = silhouette_avg
error_rate = 1 - accuracy

print(f"Accuracy of K-Means Clustering: {accuracy:.2f}")
print(f"Error Rate: {error_rate:.2f}")

# Cluster Analysis
for cluster in range(optimal_clusters):
    print(f"\nCluster {cluster} Statistics:")
    cluster_stats = data[data['Cluster'] == cluster]['price'].describe()
    print(cluster_stats)