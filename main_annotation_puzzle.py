import numpy as np
from data.donnee_puzzle import puzzle1
from coins import coins

puzzle = puzzle_im1 # choisir quelle puzzle vous voulez annalyser.
# Si les affichages de coins sont à True, vous pourrez vérifier le bon positionnement des coins, et les types de bords

def conversion(piece):
    couples = piece["points"]
    L = len(couples)
    contour = np.empty((L, 2))
    for k in range(L):
        couple = couples[k]
        contour[k, 0] = couple["x"]
        contour[k, 1] = couple["y"]
    return contour

if __name__ == "__main__":    
    pieces = puzzle[0]['predictions']['predictions']
    print(len(pieces))
    coins_listes = []
    for piece in pieces:
        contour = upsample_linear(conversion(piece), 3*len(conversion(piece)), loop=True)
        bords = caract_bords(coins(contour), contour)
        print(bords)
        print(bords[0]["type"])
        print(bords[1]["type"])
        print(bords[2]["type"])
        print(bords[3]["type"])
