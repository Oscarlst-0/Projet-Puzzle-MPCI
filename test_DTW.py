import numpy as np
import matplotlib.pyplot as plt
from data import lire_dictionnaire
from coins import coins
from fonctions_manipulation_donnees import (
    coord_dictionnaire_into_tab,
    liste_1bords_candidats,
    liste_2bords_candidats,
    matching_1bord,
    matching_2bord,
)

if __name__ == "__main__":

    donnees = lire_dictionnaire("data/output_complique.json")
    pieces = donnees[0]["predictions"]["predictions"]

    coins_listes = []
    for piece in pieces:
        couples = piece["points"]
        L = len(couples)
        contour = np.empty((L, 2))
        for k in range(L):
            couple = couples[k]
            contour[k, 0] = couple["x"]
            contour[k, 1] = couple["y"]
        coins_listes.append(coins(contour))

    piece1 = pieces[0]
    couples1 = piece1["points"]

    print(couples1)
