import json
import cv2
import numpy as np
from PIL import Image


def masque_global(image_path, contour_path, output_path):
    """
    Renvoie le masque de toute l'image de base
    
    :param image_path: path de l'image de base
    :param contour_path: path du fichier json du contour
    :param output_path: path de stockage du masque -> png
    """
    # Chargement données IA
    with open(contour_path, "r") as f:
        data = json.load(f)

    # Chargement image
    image = cv2.imread(image_path)

    # Récupération de toutes les pièces
    predictions = data[0]["predictions"]["predictions"]

    # Création du masque GLOBAL (une seule fois)
    masque = np.zeros(image.shape[:2], dtype=np.uint8)

    # Boucle sur toutes les pièces
    for piece in predictions:
        points = piece["points"]
        contour = np.array([[p["x"], p["y"]] for p in points], dtype=np.int32)

        # Ajout de la pièce au masque global
        cv2.fillPoly(masque, [contour], color=255)

    # Sauvegarde du masque global
    cv2.imwrite(output_path, masque)



masque_global("image1.png", "result.json", "masque.png")
