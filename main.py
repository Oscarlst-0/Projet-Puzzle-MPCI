# Résoudre le puzzle en utilisant les fonctions de matching

import numpy as np
import matplotlib.pyplot as plt
from data import lire_dictionnaire, Pieces
from coins import coins
from fonctions_manipulation_donnees import (
    coord_dictionnaire_into_tab,
    liste_1bords_candidats,
    liste_2bords_candidats,
    matching_1bord,
    matching_2bord,
    trouver_un_coin,
)

nom_fichier = "data/output_complique.json"

donnees = lire_dictionnaire(nom_fichier)
pieces = Pieces(donnees)

coin_depart = trouver_un_coin(pieces)
pieces.remove(coin_depart)

while len(pieces) > 0:
