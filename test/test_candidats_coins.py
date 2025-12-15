from coins import meilleur_candidat_middle, meilleur_candidat_max_angle
def test_meilleur_candidat_middle():
    num_candidat1 = [1, 2, 3, 10, 11, 13, 20, 50, 52, 54]
    num_candidat2 = [1, 2, 3, 10, 11, 13, 20, 50, 52, 54, 70]
    assert meilleurs_candidats_middle(num_candidat1) == [2, 11, 20, 52]
    assert meilleurs_candidats_middle(num_candidat2) == [2, 11, 20, 52, 70]


def test_meilleur_candidat_max_angle():
    num_candidat = [1, 2, 3, 9, 10, 12, 20, 26, 28, 30]
    delta_angle = [0,
                   1, 1.1, 0.9,
                   0, 0, 0, 0, 0,
                   2, 0.5, 0, 1,
                   0, 0, 0, 0, 0, 0, 0,
                   4,
                   0, 0, 0, 0, 0,
                   1, 0, 2, 0, 3]
    assert meilleurs_candidats_max_angle(num_candidat, delta_angle) == [2, 9, 20, 30]
