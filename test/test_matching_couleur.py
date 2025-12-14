from Matching_couleur import cout_min, alignement, alignement_v2, moyenne_couleur
from pytest import approx
import numpy as np

c1 = [(1, 2, 3), (2, 4, 3)]

c2 = [(2, 5, 3), (5, 3, 1), (1, 2, 3)]

c3 = [(6, 5, 4)]


def test_cout_min():
    assert cout_min(c1, c2) == approx(9.14)


def test_alignement():
    assert alignement(c1, c2) == [(0, 0), (1, 1), (1, 2)]


def test_alignement_v2():
    assert alignement_v2(c1, c2) == [(0, 0), (1, 1), (1, 2)]
    assert alignement_v2(c2, c3) == [(0, 0), (1, 0), (2, 0)]


image = [
    [(1, 1, 1), (1, 2, 1), (1, 1, 1)],
    [(2, 2, 2), (1, 1, 1), (2, 2, 2)],
    [(1, 2, 1), (2, 2, 2), (1, 2, 1)],
]


def test_moyenne_couleur1():
    assert moyenne_couleur([(0, 0), (0, 2), (1, 1)], image) == (
        approx(1),
        approx(1),
        approx(1),
    )


def test_moyenne_couleur2():
    assert moyenne_couleur([(0, 1), (2, 0), (2, 2)], image) == (
        approx(1),
        approx(2),
        approx(1),
    )


def test_moyenne_couleur3():
    assert moyenne_couleur([(1, 0), (1, 2), (2, 1)], image) == (
        approx(2),
        approx(2),
        approx(2),
    )
