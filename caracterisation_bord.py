import numpy as np


def angle_0_2pi(u, v):
    """ Calcule l’angle orienté entre deux vecteurs du plan, compris entre 0 et 2π.

    Cette fonction détermine l’angle orienté permettant de passer du vecteur u
    au vecteur v, en utilisant le produit scalaire et un équivalent du produit
    vectoriel en dimension 2.

    Args:
        u (tuple | list | ndarray): [x, y] premier vecteur du plan
        v (tuple | list | ndarray): [x, y] second vecteur du plan

    Returns:
        float: angle orienté entre u et v, exprimé en radians dans l’intervalle
               [0, 2π[
    """
    u = np.asarray(u)
    v = np.asarray(v)

    dot = np.dot(u, v)
    cross = u[0]*v[1] - u[1]*v[0]

    angle = np.arctan2(cross, dot)   # angle signé entre -pi et pi
    angle = angle % (2*np.pi)        # on ramène entre 0 et 2pi

    return angle

def caract_bords(coins, contour):
    """définie le type de chaque bord du contour, un bord étant un segment du contour entre 2 coins

    Args:
        coins (_type_): nd array (4,1) des indices des coins dans le contour
        contour (_type_): nd array(n, 2) de coordonnées de points. Il doit etre sur-échantilloner et périodique

    Returns:
        bords : ndarray (4,1) liste des 4 bords, qui sont des dictionnaires {"bords" = [points], "type": F, M ou D}
    """
    # commandes de vérification visuelle:
    affiche = True

    # definitions des variables et périodisation de contour et coins:

    coins = np.sort(coins)
    coins_period = np.append(coins, coins[0]+len(contour))
    contour = np.vstack([contour, contour[0:(coins[0]+1), :]])

    bords = [{"bord": contour[coins_period[k]:coins_period[k+1]+1, :],
              "type": None} for k in range(4)]

    for k in range(4):
        bord = bords[k]["bord"]
        coins1, coins2 = bord[0, :], bord[-1, :]

        # vecteur directeur de la droite entre les deux coins du bord
        v = coins2-coins1
        norme_v = np.sqrt(v[0]**2+v[1]**2)
        v_directeur = (1/norme_v)*v

        # vecteur orthongonal a v_directeur
        # dirigé vers l'intérieur de la pièce
        inte = contour[coins[k-1], :]-contour[coins[k], :]

        angle_v_dir_inte = angle_0_2pi(v_directeur, inte)

        if angle_v_dir_inte < np.pi:
            v_ortho = np.array([-v_directeur[1], v_directeur[0]])
        else:
            v_ortho = np.array([v_directeur[1], -v_directeur[0]])

        # calcul de l'écart entre les points du contour et
        # la droite donnée par v_dir
        h_points = np.empty(len(bord))

        for i in range(len(bord)):
            point = bord[i, :]

            # calcul du vecteur entre un point et son projeté H sur la droite
            # entre les deux coins
            v_coin_point = point-coins1
            v_coin_H = np.dot(v_directeur, v_coin_point)*v_directeur
            proj = v_coin_point - v_coin_H
            h_points[i] = np.dot(proj, v_ortho)

        # calcul de h_lim l'ecart max tolérable (à partir de l'écart-type)
        h_lim_max = max(np.max(h_points[:len(h_points)//5]),
                        np.max(h_points[(4*len(h_points))//5:]))
        h_lim_min = min(np.min(h_points[:len(h_points)//5]),
                        np.min(h_points[(4*len(h_points))//5:]))
        if affiche:
            print("bord", k, "lim", h_lim_max, h_lim_min)
            print("max", np.max(h_points), "min", np.min(h_points), "mean", np.mean(h_points))

        # comptage du nombre de point hors de cette limite
        n_inte = 0
        n_exte = 0
        n_align = 0

        for h_i in h_points:
            if h_i < h_lim_min:
                n_exte += 1
            elif h_i > h_lim_max:
                n_inte += 1
            else:
                n_align += 1
        if affiche:
            print("inte", n_inte, "exte", n_exte, "align", n_align, len(bord))
            print("")
        if n_inte > 0.2*len(bord):
            bords[k]["type"] = "F"
        elif n_exte > 0.2*len(bord):
            bords[k]["type"] = "M"
        else:
            bords[k]["type"] = "D"
    return bords
