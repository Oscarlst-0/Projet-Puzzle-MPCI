# Projet-Puzzle-MPCI
On retrouve sur ce projet les fichiers :
- `DTW.py` rassemblant les fonctions associées à cette dernière
- `fonctions_manipulations_donnees.py`
- `test_oscar.py`
- `data.py` regroupant les pièces en tant que dictionnaire et des fonctions de lectures de fichiers
- `Matching_couleur.py` Fonctions associées au matching couleur
- `test_matching_couleur.py` tests rudimentaires pour les fonctions de Matching_couleur.py
- `yolo.py` qui exécute yolo plusieurs fois : une fois sur l'image entière pour avoir une idée d'où se trouvent les pièces puis une fois pour chaque pièces détecter précédemment pour affiner le contour
- `masque_toutes_pieces.py` qui renvoie la même image que la photo du puzzle mais où tous les pixels où il n'y a pas de pièces sont noirs et ceux où il y a des pièces sont blancs.
- `masque_piece_par_piece.py` qui renvoie un masque (donc noir quand il n'y a pas de pièce et blanc quand il y en a une) par pièce (c'est-à-dire $N$ images avec $N$ le nombre de pièces)

- les fichiers pièces


