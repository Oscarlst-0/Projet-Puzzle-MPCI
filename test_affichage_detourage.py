import matplotlib.pyplot as plt
from data import lire_dictionnaire, conversion_liste
from fonctions_manipulation_donnees import (
    affichage_contour,
    coord_dictionnaire_into_tab,
)

# donnees = lire_dictionnaire("output_complique.json")

# liste_pieces = conversion_liste(donnees)

# for piece in liste_pieces:
#     tab = coord_dictionnaire_into_tab(piece)
#     affichage_contour(tab)

if __name__ == "__main__":

    donnees = lire_dictionnaire("output_complique.json")

    liste_predictions = donnees[0]["predictions"]["predictions"]

    plt.figure()
    for pred in liste_predictions:
        contour = coord_dictionnaire_into_tab(pred["points"])  # -> np.ndarray (N,2)
        plt.plot(contour[:, 0], contour[:, 1], marker=".", linestyle="")

    plt.gca().invert_yaxis()  # optionnel : si tu veux le repère comme l'image
    plt.axis("equal")
    plt.grid()
    plt.grid()
    plt.show()
