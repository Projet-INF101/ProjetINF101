import pytest

import src.jeu as jeu


def test_lire_coord():
    dep, arr = jeu.lire_coords()
    assert dep == 1
    assert arr == 2


def test_jouer_un_coup():
    plateau = [[3, 2, 1], [], []]
    jeu.jouer_un_coup(plateau, 3)
    assert plateau == [[3, 2], [1], []]


def test_dernier_coup():
    coups = {
        0: {
            "temps": 0,
            "plateau": [[3, 2, 1], [], []]
        },
        1: {
            "temps": 0,
            "plateau": [[3, 2], [1], []]
        },
        2: {
            "temps": 0,
            "plateau": [[3], [1], [2]]
        }
    }

    dep, arr = jeu.dernier_coup(coups, 2)
    assert dep == 0
    assert arr == 2


def test_annuler_dernier_coup():
    coups = {
        0: {
            "temps": 0,
            "plateau": [[3, 2, 1], [], []]
        },
        1: {
            "temps": 0,
            "plateau": [[3, 2], [1], []]
        },
        2: {
            "temps": 0,
            "plateau": [[3], [1], [2]]
        }
    }
    plateau = [[3], [1], [2]]
    jeu.annuler_dernier_coup(coups, 2, 3, plateau)
    assert plateau == [[3, 2], [1], []]
    with pytest.raises(KeyError):
        coups[2]

def test_nb_tour():
    coups = {
        0: {
            "temps": 0,
            "plateau": [[3, 2, 1], [], []]
        },
        1: {
            "temps": 0,
            "plateau": [[3, 2], [1], []]
        },
        2: {
            "temps": 0,
            "plateau": [[3], [1], [2]]
        }
    }

    n = jeu.nb_tour(coups)
    assert n == 2

def test_abandonner():
    assert not jeu.abandon
    jeu.abandonner()
    assert jeu.abandon

def test_annuler_coup():
    coups = {
        0: {
            "temps": 0,
            "plateau": [[3, 2, 1], [], []]
        },
        1: {
            "temps": 0,
            "plateau": [[3, 2], [1], []]
        },
        2: {
            "temps": 0,
            "plateau": [[3], [1], [2]]
        }
    }
    plateau = [[3], [1], [2]]
    jeu.annuler_coup(coups, 2, 3, plateau)()
    assert plateau == [[3, 2], [1], []]
    with pytest.raises(KeyError):
        coups[2]
