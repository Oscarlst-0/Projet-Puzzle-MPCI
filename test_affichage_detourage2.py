import numpy as np
import matplotlib.pyplot as plt
from data import lire_dictionnaire
from fonctions_manipulation_donnees import coord_dictionnaire_into_tab

donnees = lire_dictionnaire("output_complique.json")
liste_predictions = donnees[0]["predictions"]["predictions"]

plt.figure()

for pred in liste_predictions:
    # points de la pièce courante -> tableau (N, 2)
    contour = coord_dictionnaire_into_tab(pred["points"])
    x = contour[:, 0]
    y = contour[:, 1]

    # si tu veux fermer la pièce, décommente :
    # x = np.append(x, x[0])
    # y = np.append(y, y[0])

    # on relie les points de la pièce (comme affichage_contour, mais sans show)
    plt.plot(x, y, marker=".", linestyle="-")  # une couleur automatique par pièce

plt.gca().invert_yaxis()  # comme ton image Roboflow (origine en haut)
plt.axis("equal")
plt.grid()
plt.title("Toutes les pièces, points reliés")
plt.show()
