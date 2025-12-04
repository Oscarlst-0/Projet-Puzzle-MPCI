import numpy as np
from scipy.ndimage import median_filter
import matplotlib.pyplot as plt


def affiche_contour_coins(contour, ind_candidats):
    x = contour[:, 0]
    y = contour[:, 1]
    coins = np.array([contour[i, :] for i in ind_candidats])

    plt.plot(x, -y)
    plt.plot(coins[:, 0], -coins[:, 1], label='coins trouvés', marker="o")
    plt.title("Affichage du contour et des coins trouvés")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid()
    plt.show()


def upsample_linear(points, m, key_point_indices=[], loop=False):
    """
    points: (n,2) numpy array
    m: desired number of points
    by_arc_length: if True parametrize by cumulative distance, else by index
    """
    points = np.asarray(points)
    if loop:
        points = np.vstack((points, points[0, :]))
        m += 1
    n = len(points)
    if n < 2:
        raise ValueError("Il faut au moins 2 points.")
    diffs = np.diff(points, axis=0)
    seg_lengths = np.linalg.norm(diffs, axis=1)
    s = np.zeros(n)
    s[1:] = np.cumsum(seg_lengths)
    if s[-1] == 0:
        return np.repeat(points[:1], m, axis=0)
    t_old = s / s[-1]
    key_points_indices = [(m - 1) * s[i] / s[-1] for i in key_point_indices]
    key_points_indices = np.round(key_points_indices).astype(int)
    t_new = np.linspace(0.0, 1.0, m)
    x_new = np.interp(t_new, t_old, points[:, 0])
    y_new = np.interp(t_new, t_old, points[:, 1])
    points_new = np.vstack([x_new, y_new]).T
    if loop:
        points_new = points_new[:-1, :]
    if key_point_indices == []:
        return points_new
    return points_new, key_points_indices


def extract_distance_from_center(points):
    z = points[:, 0] + 1j * points[:, 1]
    z_mean = np.mean(z)
    r = np.sqrt(np.abs(z - z_mean) ** 2)
    return r


def affiche_r(contour, r_piece, d_r):

    fig, ax = plt.subplots(2, 1, figsize=(10, 10))

    # Contour
    ax[0].plot(contour[:, 0], -contour[:, 1])
    ax[0].plot(contour[0, 0], -contour[0, 1], "o", label='depart')
    ax[0].plot(contour[-10, 0], -contour[-10, 1], "o", label='fin')
    ax[0].set_aspect("equal")
    ax[0].set_title("contour de la pièce")
    ax[0].legend()

    # Distance + dérivée sur 2 axes Y
    ax2 = ax[1].twinx()
    ax[1].plot(r_piece, label="distance r_piece")
    ax2.plot(d_r, 'r', label="derivée r_d")
    ax[1].legend()
    ax2.legend()

    plt.tight_layout()
    plt.show()


def meilleurs_candidats_middle(ind_candidats, ecart_max=5):
    """ Réduis les groupes de points qui correspondent à
    la meme formation d'un coin dans r_piece, en gardant seulement
    celui au milieu (le plus cohérent)

    Args:
        ind_candidats (liste): [i] indices des points relevant ayant
            un caractère de coins
        ecart_max (int, optional): nb de points à partir duquel
            on considère que les points n'appartiennent pas à la même formation
            Defaults to 5.

    Returns:
        meilleurs : [i] indices des points au centre de chaque
            formation caractèristqiue d'un coins
    """
  # traiter le cas ou le 1er indice, et les derniers indices de la liste forment un groupe
    groupes_candidats = []
    groupe = [ind_candidats[0]]
    for i in range(1, len(ind_candidats)):
        if np.abs(ind_candidats[i]-ind_candidats[i-1]) < ecart_max:
            groupe.append(ind_candidats[i])
        else:
            groupes_candidats.append(groupe)
            groupe = [ind_candidats[i]]
    groupes_candidats.append(groupe)

    meilleurs = [groupe[len(groupe)//2] for groupe in groupes_candidats]
    return meilleurs


def meilleurs_coins(ind_candidats, r_piece, m):
    """ Elimine les points des attaches males parmi la liste
        d'indices des points ayant un caractères de coins.

    Args:
        ind_candidats (ndarray): [i] liste d'indices de coins
        derive (ndarray): [d_r] dérivé du "rayon" de la pièce
        m (int): nombre de points du contour

    Returns:
        ind_candidats (ndarray): [i] liste des coins de la pièce
    """
    # attention, il manque un modulo, pour traiter les cas ou x+eps > m
    eps = int(m * 0.02)
    if len(ind_candidats) <= 4:
        return ind_candidats
    while len(ind_candidats) > 4:
        worst = ind_candidats[0]
        indices = [(worst + k) % len(r_piece) for k in range(-eps, eps)]
        distance_worst = np.abs(r_piece[worst] -
                                np.mean([r_piece[i] for i in indices]))
        for candidat in ind_candidats:
            indices = [(candidat + k) % len(r_piece) for k in range(-eps, eps)]
            distance_candidat = np.abs(r_piece[candidat] -
                                       np.mean([r_piece[i] for i in indices]))
            if (distance_candidat < distance_worst):
                worst = candidat
                distance_worst = distance_candidat
        ind_candidats.remove(worst)
    return ind_candidats


def coins(contour):
    # commandes de vérification visuelle:
    affiche_verif_r = False
    affiche_verif_candidats = True
    affiche_verif_piece_coins = True

    # périodisation du contour, et definitions des variables
    L = contour.shape[0]
    m = 3 * L
    contour = upsample_linear(contour, m, loop=True)

    # distance entre le contour et le centre, et derivée de cette distance
    r_piece = extract_distance_from_center(contour)
    d_r = np.diff(r_piece, n=1, axis=0)
    d_r = median_filter(d_r, size=int(0.05*m), mode='wrap')

    if affiche_verif_r:
        affiche_r(contour, r_piece, d_r)

    # identification des indices des potentiels coins
    # -> dérivé nulle et croissante :
    # renvoie tout les coins + certains points des attaches mâles
    ind_candidats = []
    if d_r[-1] > 0 and d_r[1] < 0:
        ind_candidats.append(0)
    for n in range(1, m-2):
        if d_r[n-1] > 0 and d_r[n+1] < 0:
            ind_candidats.append(n)

    ind_candidats = meilleurs_candidats_middle(ind_candidats)

    if affiche_verif_candidats:
        affiche_contour_coins(contour, ind_candidats)

    ind_coins = meilleurs_coins(ind_candidats, r_piece, m)

    if affiche_verif_piece_coins:
        affiche_contour_coins(contour, ind_coins)
    return ind_coins
