import numpy as np
from data.donnee_puzzle import puzzle1
from coins import coins

if __name__ == "__main__":

    puzzle = puzzle1
    pieces = puzzle[0]["predictions"]["predictions"]
    coins_listes = []
    for piece in pieces:
        couples = piece["points"]
        L = len(couples)
        contour = np.empty((L, 2))
        for k in range(L):
            couple = couples[k]
            contour[k, 0] = couple["x"]
            contour[k, 1] = couple["y"]
        coins_listes.append(coins(contour))
    print(coins_listes)
