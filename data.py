import numpy as np
import json


def lire_dictionnaire(chemin_fichier):
    """Lit un fichier texte contenant un dictionnaire JSON et renvoie le dict Python."""
    with open(chemin_fichier, "r", encoding="utf-8") as f:
        d = json.load(f)
    return d


def conversion(dictionnaire):

    predictions = dictionnaire["predictions"][0]
    couples = predictions["points"]
    L = len(couples)
    liste = np.empty((L, 2))
    for k in range(L):
        couple = couples[k]
        liste[k, 0] = couple["x"]
        liste[k, 1] = couple["y"]
    return liste


def surechantillonage_interpol_np(contour):
    # Calculer la distance cumulative le long du contour, et le nombre de points
    direction = np.diff(contour, axis=0)
    distance_prochain = np.sqrt((direction**2).sum(axis=1))
    pas = np.min(distance_prochain)  # modifiable
    abscisse_curviligne = np.insert(np.cumsum(distance_prochain), 0, 0)
    Longueur_total = abscisse_curviligne[-1]

    M = int(Longueur_total / pas) + 1

    # Longueur totale et positions équidistantes
    L = abscisse_curviligne[-1]
    new_positions = np.linspace(0, L, M)

    # Interpolation linéaire pour x et y, avec numpy
    x_new = np.interp(new_positions, abscisse_curviligne, contour[:, 0])
    y_new = np.interp(new_positions, abscisse_curviligne, contour[:, 1])

    contour_echantillone = np.vstack([x_new, y_new]).T
    return contour_echantillone


def conversion_liste(dictionnaire):
    liste_pieces = []
    for predictions in dictionnaire["predictions"]:
        couples = predictions["points"]
        L = len(couples)
        liste = np.empty((L, 2))
        for k in range(L):
            couple = couples[k]
            liste[k, 0] = couple["x"]
            liste[k, 1] = couple["y"]
        liste_pieces.append(liste)
    return liste_pieces


def Pieces(
    dictionnaire,
    coin_a,
    coin_b,
    coin_c,
    coin_d,
    indice_coin_a,
    indice_coin_b,
    indice_coin_c,
    indice_coin_d,
    liste_indice_bord,
    type_bord_1,
    type_bord_2,
    type_bord_3,
    type_bord_4,
):
    liste_pieces = conversion_liste(dictionnaire)
    liste_dict_pieces = []
    for i, piece in enumerate(liste_pieces):
        piece_dict = {
            "contour": surechantillonage_interpol_np(piece),
            "coins": np.array([coin_a[i], coin_b[i], coin_c[i], coin_d[i]]),
            "indice_coins": np.array(
                [indice_coin_a[i], indice_coin_b[i], indice_coin_c[i], indice_coin_d[i]]
            ),
            "bord_types": {
                "bord": [
                    surechantillonage_interpol_np(piece)[
                        np.array(
                            [liste_indice_bord[0], liste_indice_bord[1]],
                            liste_indice_bord[2],
                            liste_indice_bord[3],
                        )[j] : np.array(
                            [liste_indice_bord[0] + 1, liste_indice_bord[1]] + 1,
                            liste_indice_bord[2] + 1,
                            None,
                        )[
                            j
                        ]
                    ]
                    for j in range(4)
                ],
                "types": [
                    type_bord_1[i],
                    type_bord_2[i],
                    type_bord_3[i],
                    type_bord_4[i],
                ],
            },
        }
        globals()[
            f"Piece{i+1}"
        ] = piece_dict  # permet de nommer Piece1, Piece2, ... dans le dict
        liste_dict_pieces.append(piece_dict)
    return liste_dict_pieces


Piece1 = {
    "contour": surechantillonage_interpol_np(
        conversion(lire_dictionnaire("piece1.txt"))
    ),
    "coins": np.array([[225, 21], [15, 550], [553, 792], [794, 240]]),
    "indice_coins": np.array([1, 754, 1545, 2038]),
    "bord_types": {
        "bord": [
            surechantillonage_interpol_np(conversion(lire_dictionnaire("piece1.txt")))[
                np.array([1, 754, 1545, 2038])[i] : np.array([755, 1546, 2039, None])[i]
            ]
            for i in range(4)
        ],
        "types": ["F", "M", "B", "F"],
    },
}


Piece2 = {
    "contour": surechantillonage_interpol_np(
        conversion(lire_dictionnaire("piece2.txt"))
    ),
    "coins": np.array([[225, 191], [164, 301], [299, 380], [363, 270]]),
    "indice_coins": np.array([0, 136, 412, 654]),
    "bord_types": {
        "bord": [
            surechantillonage_interpol_np(conversion(lire_dictionnaire("piece2.txt")))[
                np.array([0, 136, 412, 654])[i] : np.array([136, 412, 654, None])[i]
            ]
            for i in range(4)
        ],
        "types": ["B", "M", "F", "F"],
    },
}

# print(surechantillonage_interpol_np(conversion(lire_dictionnaire("Test/piece1.txt")))[2038])
# list = np.array([[1,0],[1,1],[2,1],[2,2]])
