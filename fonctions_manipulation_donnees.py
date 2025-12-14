import numpy as np
import matplotlib.pyplot as plt
from DTW import cout_min


def coord_dictionnaire_into_tab(points):
    """ Convertit des coordonnées issues d’un dictionnaire en tableau NumPy.

    Cette fonction prend en entrée soit un tableau NumPy de coordonnées, soit
    une liste de dictionnaires contenant des clés "x" et "y". Dans ce dernier
    cas, elle convertit les données en un tableau NumPy de coordonnées (x, y).

    Args:
        points (ndarray | list[dict]): coordonnées des points, soit déjà sous
                                       forme de tableau NumPy, soit sous forme
                                       de dictionnaires {"x": ..., "y": ...}

    Returns:
        ndarray: [N, 2] tableau des coordonnées (x, y)
    """
    if isinstance(points, np.ndarray):
        return points

    return np.array([[p["x"], p["y"]] for p in points])


def affichage_contour(contour):
    """ Affiche le contour d’une pièce à partir de ses coordonnées.

    Cette fonction trace les points constituant le contour d’une pièce dans le
    plan, afin de visualiser sa forme globale.

    Args:
        contour (ndarray): [N, 2] ensemble des points du contour de la pièce

    Returns:
        None
    """
    x = contour[:, 0]
    y = contour[:, 1]

    plt.plot(x, y, marker=".")
    plt.title("Affichage du bord")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid()
    plt.show()


def affichage_2contour_renverse(contour, contour2):
    """ Affiche deux contours pour comparer un bord avec son renversement.

    Cette fonction trace deux contours dans le plan : le premier tel quel,
    et le second avec une inversion verticale, afin de visualiser la
    correspondance entre un bord et son renversement.

    Args:
        contour (ndarray): [N, 2] premier contour à afficher
        contour2 (ndarray): [M, 2] second contour, affiché avec renversement

    Returns:
        None
    """
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
    """ Affiche deux contours en comparant un bord avec son renversement normalisé.

    Cette fonction compare deux contours en adaptant d’abord l’échelle du second
    contour à celle du premier, puis en affichant le second avec une inversion
    verticale. Elle permet ainsi de visualiser la similarité entre deux bords
    indépendamment de leur taille.

    Args:
        contour (ndarray): [N, 2] contour de référence
        contour2 (ndarray): [M, 2] contour à comparer, renversé et normalisé

    Returns:
        None
    """
    def rescale_contour2_sur_contour1(contour1, contour2):
        """ Met à l’échelle le second contour pour l’adapter à la longueur du premier.

        Args:
            contour1 (ndarray): contour de référence
            contour2 (ndarray): contour à mettre à l’échelle

        Returns:
            ndarray: contour2 redimensionné selon l’échelle de contour1
        """
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
    """ Affiche deux contours afin de comparer leur forme.

    Cette fonction trace deux contours dans le plan, permettant de visualiser
    et comparer directement leur géométrie, par exemple avant ou après une
    étape de normalisation.

    Args:
        contour1 (ndarray): [N, 2] premier contour à afficher
        contour2 (ndarray): [M, 2] second contour à afficher

    Returns:
        None
    """
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


def affichage_DTW(contour1, contour2, path):
    pass  # à finir


def translation(contour):
    """ Translate un contour pour ramener son premier point à l’origine.

    Cette fonction applique une translation au contour afin que son premier
    point soit placé à l’origine du repère. Elle est utilisée pour normaliser
    la position d’un contour indépendamment de sa localisation initiale.

    Args:
        contour (ndarray): [N, 2] ensemble des points du contour

    Returns:
        ndarray: [N, 2] contour translaté, avec le premier point à l’origine
    """
    z = contour[:, 0] + 1j * contour[:, 1]
    zA = z[0]  # coord 1er point A

    # translation pour ramener A à l'origine
    z1 = z - zA

    contour_norm = np.array([z1.real, z1.imag]).T

    return contour_norm


def normaliser_contour_complexe(contour):
    """ Normalise un contour par translation et rotation dans le plan.

    Cette fonction transforme un contour afin de le rendre invariant par
    translation et rotation. Le premier point est ramené à l’origine, le
    segment reliant le premier et le dernier point est aligné avec l’axe des
    abscisses, puis le milieu de ce segment est centré à l’origine.

    Args:
        contour (ndarray): [N, 2] ensemble des points du contour initial

    Returns:
        ndarray: [N, 2] contour normalisé, invariant par translation et rotation
    """
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


def normaliser_liste_contour_complexe(liste_contour):
    """ Normalise une liste de contours par translation et rotation.

    Cette fonction applique une normalisation géométrique à chacun des contours
    d’une liste. Pour chaque contour, le premier point est ramené à l’origine,
    le segment reliant le premier au dernier point est aligné avec l’axe des
    abscisses, puis le milieu de ce segment est centré à l’origine. Elle est
    notamment utilisée pour comparer des bords indépendamment de leur position
    et orientation.

    Args:
        liste_contour (list[ndarray]): liste de contours [N_i, 2] à normaliser

    Returns:
        list[ndarray]: liste des contours normalisés
    """
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
    """ Calcule la meilleure correspondance de bords entre deux pièces de puzzle.

    Cette fonction compare les bords de deux pièces en tenant compte de leur
    type (mâle ou femelle). Pour chaque paire de bords compatibles, les contours
    sont normalisés puis comparés à l’aide d’un coût d’alignement minimal. La
    fonction retourne la paire de bords la plus similaire ainsi que la distance
    associée.

    Args:
        piece1 (dict): dictionnaire décrivant la première pièce, incluant ses
                       bords et leurs types
        piece2 (dict): dictionnaire décrivant la seconde pièce, incluant ses
                       bords et leurs types

    Returns:
        tuple:
            - tuple(int, int): indices des bords appariés (bord de piece1, bord de piece2)
            - float: distance minimale correspondant au meilleur appariement
    """
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
    """ Renvoie le type de bord complémentaire.

    Cette fonction associe à un type de bord donné son complémentaire :
    un bord mâle est associé à un bord femelle, et inversement. Les autres
    types ne possèdent pas de complémentaire défini.

    Args:
        type (str): type du bord ("M" pour mâle, "F" pour femelle)

    Returns:
        str | None: type complémentaire ("F" ou "M"), ou None si non applicable
    """
    if type == "M":
        type_complementaire = "F"
    elif type == "F":
        type_complementaire = "M"
    else:
        return None
    return type_complementaire


def liste_1bords_candidats(liste_pieces, type):
    """ Extrait et normalise les bords candidats d’un type donné.

    Cette fonction parcourt une liste de pièces et sélectionne tous les bords
    dont le type correspond au type demandé (mâle ou femelle). Chaque bord
    sélectionné est converti en tableau de coordonnées puis normalisé afin de
    faciliter les comparaisons ultérieures.

    Args:
        liste_pieces (list[dict]): liste de dictionnaires décrivant les pièces
        type (str): type de bord recherché ("M" ou "F")

    Returns:
        list[ndarray]: liste des bords normalisés correspondant au type demandé
    """
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
    """ Extrait et normalise des couples de bords consécutifs candidats.

    Cette fonction parcourt une liste de pièces et sélectionne les couples de
    bords consécutifs dont les types correspondent au couple de types demandé.
    Chaque bord est converti en tableau de coordonnées puis normalisé afin de
    permettre des comparaisons géométriques indépendantes de la position et de
    l’orientation.

    Args:
        liste_pieces (list[dict]): liste de dictionnaires décrivant les pièces
        couple_type (tuple[str, str]): couple de types de bords recherchés
                                       (par exemple ("M", "F"))

    Returns:
        list[tuple[ndarray, ndarray]]: liste de couples de bords normalisés
    """
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
    """ Trouve le meilleur appariement pour un bord parmi une liste de candidats.

    Cette fonction compare un bord donné à une liste de bords candidats à l’aide
    d’un coût d’alignement minimal. Le bord identique à celui fourni est retiré
    de la liste des candidats afin d’éviter une auto-correspondance. Le bord
    présentant la distance minimale est retourné avec le coût associé.

    Args:
        bord (ndarray): contour normalisé du bord à apparier
        bords_candidats (list[ndarray]): liste de contours normalisés candidats

    Returns:
        tuple:
            - ndarray: bord candidat présentant la meilleure correspondance
            - float: distance minimale associée à cet appariement
    """
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
    """ Trouve le meilleur appariement pour un couple de bords consécutifs.

    Cette fonction compare un couple de bords donné à une liste de couples de
    bords candidats. Seuls les couples dont les types sont complémentaires
    sont considérés. Le coût total est calculé comme la somme des coûts
    d’alignement minimal de chaque bord du couple. Le couple présentant le
    coût total minimal est retourné.

    Args:
        couple_bord (tuple): couple de bords à apparier
        bords_candidats (list[tuple]): liste de couples de bords candidats

    Returns:
        tuple:
            - tuple: couple de bords candidats présentant la meilleure correspondance
            - float: distance minimale associée à cet appariement
    """
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


def trouver_un_coin(Pieces):
    """ Identifie une pièce de coin parmi une liste de pièces.

    Cette fonction parcourt une liste de pièces et recherche celle qui possède
    exactement deux bords droits. Une telle configuration correspond à une
    pièce de coin dans un puzzle.

    Args:
        Pieces (list[dict]): liste de dictionnaires décrivant les pièces du puzzle

    Returns:
        dict | None: dictionnaire correspondant à une pièce de coin si elle est
                     trouvée, sinon None
    """
    for piece in Pieces:
        compteur = 0
        liste_types = piece["bord_types"]["types"]
        for i in range(4):
            if liste_types[i] == "D":
                compteur += 1
        if compteur == 2:
            return piece
