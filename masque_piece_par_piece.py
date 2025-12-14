import json
import cv2
import numpy as np
import os


def masques_par_piece(image_path, contour_path, output_dir):
    # Création du dossier de sortie
    os.makedirs(output_dir, exist_ok=True)

    # Chargement données IA
    with open(contour_path, "r") as f:
        data = json.load(f)

    # Chargement image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image non chargée")

    predictions = data[0]["predictions"]["predictions"]

    for i, piece in enumerate(predictions):
        points = piece["points"]
        contour = np.array([[p["x"], p["y"]] for p in points], dtype=np.int32)

        # Création du masque pour CETTE pièce
        masque = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.fillPoly(masque, [contour], color=255)

        output_path = os.path.join(output_dir, f"piece_{i}.png")
        cv2.imwrite(output_path, masque)

masques_par_piece("image3.png", "result.json", "masque")