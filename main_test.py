import pytest

import src.main as main

# Fichier contenant les tests pour le projet.
#
# Chaque fonction dont le nom commence par "test" est un test,
# correspondant généralement à une fonction du programme que l'on souhaite tester.

def test_init():
	plateau = main.init(4)

	assert len(plateau) == 3
	assert plateau == [
		[4, 3, 2, 1],
        [],
        []
	]

def test_nombre_disques():
    plateau = main.init(5)

    assert main.nombre_disques(plateau, 0) == 5
    assert main.nombre_disques(plateau, 1) == 0
    assert main.nombre_disques(plateau, 2) == 0

    with pytest.raises(IndexError):
        main.nombre_disques(plateau, 3)

def test_disque_superieur():
    plateau = [[4, 3, 1], [], [2]]

    assert main.disque_superieur(plateau, 0) == 1
    assert main.disque_superieur(plateau, 2) == 2
    assert main.disque_superieur(plateau, 1) == -1

def test_position_disque():
    plateau = [[3, 1], [2], [4]]

    assert main.position_disque(plateau, 3) == 0
    assert main.position_disque(plateau, 1) == 0
    assert main.position_disque(plateau, 2) == 1
    assert main.position_disque(plateau, 4) == 2

def test_verifier_deplacement():
    plateau = [[3, 1], [2], [4]]

    assert main.verifier_deplacement(plateau, 0, 1)
    assert main.verifier_deplacement(plateau, 0, 2)
    assert main.verifier_deplacement(plateau, 1, 2)

    assert not main.verifier_deplacement(plateau, 2, 0)
    assert not main.verifier_deplacement(plateau, 2, 1)
    assert not main.verifier_deplacement(plateau, 1, 0)

def test_verifier_victoire():
    assert main.verifier_victoire([[], [], [3, 2, 1]], 3)
    assert main.verifier_victoire([[], [], [4, 3, 2, 1]], 4)

    assert not main.verifier_victoire([[], [1], [3, 2]], 3)
