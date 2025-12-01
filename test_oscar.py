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

couple_match, distance_min = distance_matching_deux_pieces(Piece1, Piece2)
print(couple_match, distance_min)

# affichage_2contour_renverse(
#     normaliser_contour_complexe(liste_bord1[couple_match[0]]),
#     normaliser_contour_complexe(liste_bord2[couple_match[1]]),
# )
