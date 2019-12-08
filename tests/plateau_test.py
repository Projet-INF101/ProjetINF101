import pytest

import src.plateau as plat


def test_init():
    plateau = plat.init(4)

    assert len(plateau) == 3
    assert plateau == [
        [4, 3, 2, 1],
        [],
        []
    ]


def test_nombre_disques():
    plateau = plat.init(5)

    assert plat.nombre_disques(plateau, 0) == 5
    assert plat.nombre_disques(plateau, 1) == 0
    assert plat.nombre_disques(plateau, 2) == 0

    with pytest.raises(IndexError):
        plat.nombre_disques(plateau, 3)


def test_disque_superieur():
    plateau = [[4, 3, 1], [], [2]]

    assert plat.disque_superieur(plateau, 0) == 1
    assert plat.disque_superieur(plateau, 2) == 2
    assert plat.disque_superieur(plateau, 1) == -1


def test_position_disque():
    plateau = [[3, 1], [2], [4]]

    assert plat.position_disque(plateau, 3) == 0
    assert plat.position_disque(plateau, 1) == 0
    assert plat.position_disque(plateau, 2) == 1
    assert plat.position_disque(plateau, 4) == 2


def test_verifier_deplacement():
    plateau = [[3, 1], [2], [4]]

    assert plat.verifier_deplacement(plateau, 0, 1)
    assert plat.verifier_deplacement(plateau, 0, 2)
    assert plat.verifier_deplacement(plateau, 1, 2)

    assert not plat.verifier_deplacement(plateau, 2, 0)
    assert not plat.verifier_deplacement(plateau, 2, 1)
    assert not plat.verifier_deplacement(plateau, 1, 0)


def test_verifier_victoire():
    assert plat.verifier_victoire([[], [], [3, 2, 1]], 3)
    assert plat.verifier_victoire([[], [], [4, 3, 2, 1]], 4)

    assert not plat.verifier_victoire([[], [1], [3, 2]], 3)
