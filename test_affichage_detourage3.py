import matplotlib.pyplot as plt
import numpy as np

from data import lire_dictionnaire
from fonctions_manipulation_donnees import coord_dictionnaire_into_tab

if __name__ == "__main__":

    img = plt.imread("piece_scan.png")

    donnees = lire_dictionnaire("output_simple1.json")
    bloc = donnees[0]["predictions"]

    img_w_json = bloc["image"]["width"]
    img_h_json = bloc["image"]["height"]

    h_img, w_img = img.shape[:2]

    sx = w_img / img_w_json
    sy = h_img / img_h_json

    fig, ax = plt.subplots(figsize=(6, 8))

    ax.imshow(img)

    for pred in bloc["predictions"]:
        contour = coord_dictionnaire_into_tab(pred["points"])  # -> (N, 2)

        # remettre à l’échelle si besoin
        contour_scaled = contour.copy().astype(float)
        contour_scaled[:, 0] *= sx
        contour_scaled[:, 1] *= sy

        ax.plot(contour_scaled[:, 0], contour_scaled[:, 1], "-", linewidth=1)

    ax.set_xlim(0, w_img)
    ax.set_ylim(h_img, 0)

    ax.set_title("Contours des pièces superposés à l'image")
    ax.grid(False)
    plt.show()
