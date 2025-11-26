import numpy as np
import matplotlib.pyplot as plt
from DTW import cout_min


def coord_dictionnaire_into_tab(points):
    if isinstance(points, np.ndarray):
        return points

    return np.array([[p["x"], p["y"]] for p in points])


def affichage_contour(contour):
    x = contour[:, 0]
    y = contour[:, 1]

    plt.plot(x, y, marker=".")
    plt.title("Affichage du bord")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid()
    plt.show()


def affichage_2contour_renverse(contour, contour2):

    x1 = contour[:, 0]
    y1 = contour[:, 1]

    x2 = contour2[:, 0]
    y2 = contour2[:, 1]

    plt.plot(x1, y1, marker=".")
    plt.plot(x2, -y2, marker=".")
    plt.title("Comparaison d'un bord avec son renversement")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid()
    plt.show()


def affichage_2contour_renverse_normalisation(contour, contour2):

    def echelle_contour2_sur_contour1(contour1, contour2):
        # on adapte le contour2 à la taille du contour1

        L1 = abs(contour1[-1, 0] - contour1[0, 0])
        L2 = abs(contour2[-1, 0] - contour2[0, 0])

        facteur = L1 / L2
        c2_scaled = contour2 * facteur
        return c2_scaled

    contour2_rs = echelle_contour2_sur_contour1(contour, contour2)

    x1 = contour[:, 0]
    y1 = contour[:, 1]

    x2 = contour2_rs[:, 0]
    y2 = contour2_rs[:, 1]

    plt.plot(x1, y1, marker=".")
    plt.plot(x2, -y2, marker=".")
    plt.title("Comparaison d'un bord avec son renversement")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid()
    plt.show()


def affichage_2contour(contour1, contour2):
    x1 = contour1[:, 0]
    y1 = contour1[:, 1]

    x2 = contour2[:, 0]
    y2 = contour2[:, 1]

    plt.plot(x1, y1, marker=".")
    plt.plot(x2, y2, marker=".")
    plt.title("Comparaison d'un bord avec sa normalisation")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid()
    plt.show()


def translation(contour):
    z = contour[:, 0] + 1j * contour[:, 1]
    zA = z[0]  # coord 1er point A

    # translation pour ramener A à l'origine
    z1 = z - zA

    contour_norm = np.array([z1.real, z1.imag]).T

    return contour_norm


def normaliser_contour_complexe(contour):
    # convertir en nombres complexes z = x + i*y
    z = contour[:, 0] + 1j * contour[:, 1]
    zA = z[0]  # coord 1er point A
    zB = z[-1]  # coord dernier point B

    # translation pour ramener A à l'origine
    z1 = z - zA

    # rotation : AB sur l'axe x
    v = zB - zA  # vecteur  AB
    theta = np.angle(v)  # calcul angle entre A et B
    z2 = z1 * np.exp(-1j * theta)

    # # 3) translation pour avoir le milieu de AB à l'origine
    # b = z2[-1].real  # coordonnée x de B
    # z3 = z2 - b / 2.0  # on décale de b/2 vers la gauche

    contour_norm = np.array([z2.real, z2.imag]).T

    return contour_norm


def distance_matching_deux_pieces(piece1, piece2):
    liste_bord1 = piece1["bord_types"]["bord"]
    liste_bord2 = piece2["bord_types"]["bord"]

    liste_type1 = piece1["bord_types"]["types"]
    liste_type2 = piece2["bord_types"]["types"]

    b0_1 = coord_dictionnaire_into_tab(liste_bord1[0])
    b1_1 = coord_dictionnaire_into_tab(liste_bord1[1])
    b2_1 = coord_dictionnaire_into_tab(liste_bord1[2])
    b3_1 = coord_dictionnaire_into_tab(liste_bord1[3])

    b0_2 = coord_dictionnaire_into_tab(liste_bord2[0])
    b1_2 = coord_dictionnaire_into_tab(liste_bord2[1])
    b2_2 = coord_dictionnaire_into_tab(liste_bord2[2])
    b3_2 = coord_dictionnaire_into_tab(liste_bord2[3])

    b0_1_norm = normaliser_contour_complexe(b0_1)
    b1_1_norm = normaliser_contour_complexe(b1_1)
    b2_1_norm = normaliser_contour_complexe(b2_1)
    b3_1_norm = normaliser_contour_complexe(b3_1)

    b0_2_norm = normaliser_contour_complexe(b0_2)
    b1_2_norm = normaliser_contour_complexe(b1_2)
    b2_2_norm = normaliser_contour_complexe(b2_2)
    b3_2_norm = normaliser_contour_complexe(b3_2)

    distance_min = 10000000
    couple_match = (0, 0)

    for i in range(4):
        for j in range(4):
            if (liste_type1[i] == "M" and liste_type2[j] == "F") or (
                liste_type1[i] == "F" and liste_type2[j] == "M"
            ):
                if distance_min > cout_min(liste_bord1[i], liste_bord2[j]):
                    distance_min = cout_min(liste_bord1[i], liste_bord2[j])
                    couple_match = (i, j)

    return couple_match, distance_min
