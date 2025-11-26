from data import Piece1, Piece2
from fonctions_manipulation_donnees import (
    coord_dictionnaire_into_tab,
    affichage_contour,
    affichage_2contour,
    affichage_2contour_renverse,
    affichage_2contour_renverse_normalisation,
    translation,
    normaliser_contour_complexe,
    distance_matching_deux_pieces,
)
from DTW import cout_min

liste_bord1 = Piece1["bord_types"]["bord"]
liste_bord2 = Piece2["bord_types"]["bord"]

b0_1 = coord_dictionnaire_into_tab(liste_bord1[0])
b1_1 = coord_dictionnaire_into_tab(liste_bord1[1])
b2_1 = coord_dictionnaire_into_tab(liste_bord1[2])
b3_1 = coord_dictionnaire_into_tab(liste_bord1[3])

b0_2 = coord_dictionnaire_into_tab(liste_bord2[0])
b1_2 = coord_dictionnaire_into_tab(liste_bord2[1])
b2_2 = coord_dictionnaire_into_tab(liste_bord2[2])
b3_2 = coord_dictionnaire_into_tab(liste_bord2[3])

b0_1 = translation(b0_1)
b1_1 = translation(b1_1)
b2_1 = translation(b2_1)
b3_1 = translation(b3_1)

b0_2 = translation(b0_2)
b1_2 = translation(b1_2)
b2_2 = translation(b2_2)
b3_2 = translation(b3_2)


b0_1_norm = normaliser_contour_complexe(b0_1)
b1_1_norm = normaliser_contour_complexe(b1_1)
b2_1_norm = normaliser_contour_complexe(b2_1)
b3_1_norm = normaliser_contour_complexe(b3_1)

b0_2_norm = normaliser_contour_complexe(b0_2)
b1_2_norm = normaliser_contour_complexe(b1_2)
b2_2_norm = normaliser_contour_complexe(b2_2)
b3_2_norm = normaliser_contour_complexe(b3_2)


# affichage_2contour(b0_1, b0_1_norm)
# affichage_2contour(b1_1, b1_1_norm)
# affichage_2contour(b2_1, b2_1_norm)
# affichage_2contour(b3_1, b3_1_norm)

# affichage_2contour(b0_1_norm, b1_2_norm)

# affichage_2contour(b0_2, b0_2_norm)
# affichage_2contour(b1_2, b1_2_norm)
# affichage_2contour(b2_2, b2_2_norm)
# affichage_2contour(b3_2, b3_2_norm)

# distance = cout_min(b1_1, b2_1)
# print("Distance DTW entre les deux contours :", distance)

couple_match, distance_min = distance_matching_deux_pieces(Piece1, Piece2)
print(couple_match, distance_min)

affichage_2contour_renverse(
    normaliser_contour_complexe(liste_bord1[couple_match[0]]),
    normaliser_contour_complexe(liste_bord2[couple_match[1]]),
)
affichage_2contour_renverse_normalisation(b0_1_norm, b1_2_norm)
