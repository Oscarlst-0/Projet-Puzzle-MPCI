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

    def rescale_contour2_sur_contour1(contour1, contour2):
        # on adapte le contour2 à la taille du contour1

        L1 = abs(contour1[-1, 0] - contour1[0, 0])
        L2 = abs(contour2[-1, 0] - contour2[0, 0])

        facteur = L1 / L2
        c2_scaled = contour2 * facteur
        return c2_scaled

    contour2_rs = rescale_contour2_sur_contour1(contour, contour2)

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


def normaliser_contour_complexe(contour):  # normalisation d'un contour
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

    # 3) translation pour avoir le milieu de AB à l'origine
    b = z2[-1].real  # coordonnée x de B
    z3 = z2 - b / 2.0  # on décale de b/2 vers la gauche

    contour_norm = np.array([z3.real, z3.imag]).T

    return contour_norm


def normaliser_liste_contour_complexe(liste_contour):  # normalisation d'une liste
    liste_contour_norm = []
    for i in range(4):
        z = liste_contour[i][:, 0] + 1j * liste_contour[i][:, 1]
        zA = z[0]  # coord 1er point A
        zB = z[-1]  # coord dernier point B

        # translation pour ramener A à l'origine
        z1 = z - zA

        # rotation : AB sur l'axe x
        v = zB - zA  # vecteur  AB
        theta = np.angle(v)  # calcul angle entre A et B
        z2 = z1 * np.exp(-1j * theta)

        b = z2[-1].real  # coordonnée x de B
        z3 = z2 - b / 2.0  # on décale de b/2 vers la gauche

        contour_norm = np.array([z3.real, z3.imag]).T
        liste_contour_norm.append(contour_norm)
    return liste_contour_norm


def distance_matching_deux_pieces(piece1, piece2):
    liste_bord1 = piece1["bord_types"]["bord"]
    liste_bord2 = piece2["bord_types"]["bord"]

    liste_type1 = piece1["bord_types"]["types"]
    liste_type2 = piece2["bord_types"]["types"]

    liste_tab_bord1 = [coord_dictionnaire_into_tab(liste_bord1[i]) for i in range(4)]
    liste_tab_bord2 = [coord_dictionnaire_into_tab(liste_bord2[i]) for i in range(4)]

    liste_tab_bord1_norm = normaliser_liste_contour_complexe(liste_tab_bord1)
    liste_tab_bord2_norm = normaliser_liste_contour_complexe(liste_tab_bord2)

    distance_min = 10000000
    couple_match = (0, 0)

    for i in range(4):
        for j in range(4):
            if (liste_type1[i] == "M" and liste_type2[j] == "F") or (
                liste_type1[i] == "F" and liste_type2[j] == "M"
            ):
                cout = cout_min(liste_tab_bord1_norm[i], liste_tab_bord2_norm[j])
                if distance_min > cout:
                    distance_min = cout
                    couple_match = (i, j)

    return couple_match, distance_min


def type_complementaire(type):
    if type == "M":
        type_complementaire = "F"
    elif type == "F":
        type_complementaire = "M"
    else:
        return None
    return type_complementaire


def liste_1bords_candidats(liste_pieces, type):
    candidats = []
    for piece in liste_pieces:
        liste_bord = piece["bord_types"]["bord"]
        liste_type = piece["bord_types"]["types"]
        for i in range(4):
            if liste_type[i] == type:
                bord_tab = coord_dictionnaire_into_tab(liste_bord[i])
                bord_norm = normaliser_contour_complexe(bord_tab)
                candidats.append(bord_norm)
    return candidats


def liste_2bords_candidats(liste_pieces, couple_type):
    type1, type2 = couple_type
    couple_candidats = []
    for piece in liste_pieces:
        liste_bord = piece["bord_types"]["bord"]
        liste_type = piece["bord_types"]["types"]
        for i in range(4):
            if (
                liste_type[i] == type1 and liste_type[(i + 1) % 4] == type2
            ):  # le modulo traite le cas des bords (4,1)
                bords_tab = (
                    coord_dictionnaire_into_tab(liste_bord[i]),
                    coord_dictionnaire_into_tab(liste_bord[(i + 1) % 4]),
                )
                bords_norm = (
                    normaliser_contour_complexe(bords_tab[0]),
                    normaliser_contour_complexe(bords_tab[1]),
                )
                couple_candidats.append(bords_norm)
    return couple_candidats


def matching_1bord(bord, bords_candidats):
    bords_candidats.remove(bord)
    distance_min = 10000000
    bord_match = None
    for bord_candidat in bords_candidats:
        cout = cout_min(bord, bord_candidat)
        if distance_min > cout:
            distance_min = cout
            bord_match = bord_candidat
    return bord_match, distance_min


def matching_2bord(couple_bord, bords_candidats):
    bord1, bord2 = couple_bord
    bords_candidats.remove((bord1, bord2))
    distance_min = 100000000
    couple_bord_match = None
    for couple_bords_candidats in bords_candidats:
        couple_candidats_type_comp = (
            type_complementaire(couple_bords_candidats[0]["bord_types"]["types"][0]),
            type_complementaire(couple_bords_candidats[0]["bord_types"]["types"][1]),
        )
        couple_type_comp = (
            type_complementaire(bord1["bord_types"]["types"][0]),
            type_complementaire(bord2["bord_types"]["types"][1]),
        )
        if couple_candidats_type_comp == couple_type_comp:
            cout1 = cout_min(bord1, couple_bords_candidats[0])
            cout2 = cout_min(bord2, couple_bords_candidats[1])
            if distance_min > cout1 + cout2:
                distance_min = cout1 + cout2
                couple_bord_match = couple_bords_candidats
    return couple_bord_match, distance_min
