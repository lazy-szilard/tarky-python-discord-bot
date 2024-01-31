import requests
import numpy as np
import cv2
from sklearn.cluster import MiniBatchKMeans

def extract_colours(url: str) -> dict:
    # Download and convert the image
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the image. Status code: {response.status_code}")
        return {}

    image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.COLOR_BGR2RGB)
    image_flat = image.reshape(image.shape[0] * image.shape[1], 3)

    # Use MiniBatchKMeans for faster clustering
    clf = MiniBatchKMeans(n_clusters=5)
    labels = clf.fit_predict(image_flat)

    # Get the cluster centers and convert them to hexadecimal colors
    center_colors = clf.cluster_centers_
    hex_colors = ["#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2])) for color in center_colors]

    # Sort hex_colors based on the inertia of clusters (compactness)
    hex_colors_sorted = [hex_color for hex_color in sorted(
        hex_colors, key=lambda x: np.sum((clf.cluster_centers_ - np.mean(image_flat[labels == clf.predict(image_flat)], axis=0))**2), reverse=False)]

    # Categorize colors into dominate, support, and accent
    result = {
        'dominant': hex_colors_sorted[0],
        'support': hex_colors_sorted[1],
        'accent': hex_colors_sorted[2:],
    }

    return result
