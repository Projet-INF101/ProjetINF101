import time
from typing import List, Tuple

from src.interface import efface_disque, dessine_config
from src.plateau import Plateau, disque_superieur


def solution(n: int, src: int, aux: int, dest: int) -> List[Tuple[int, int]]:
    """
    Trouve la solution pour un nombre de disque donné,
    de manière récursive.

    Chaque élément de la liste retourné est un couple
    formé de la tour de départ et de la tour d'arrivée.

    # Paramètres

    - n : le nombre de disques sur le plateau
    - src : la tour numéro 0
    - aux : la tour numéro 1
    - dest : la tour numéro 2

    Ces paramètres ne correspondent à ces valeurs que pour
    le premier appel de cette fonction, n diminue ensuite
    à chaque itération, et les tours sont parfois inversées.
    """
    if n == 1:
        return [(src, dest)]
    else:
        return (solution(n - 1, src, dest, aux) +
                [(src, dest)] +
                solution(n - 1, aux, src, dest))


def afficher_solution(plateau: Plateau, n: int, coups: List[Tuple[int, int]]):
    """
    Cette fonction affiche la solution à l'écran.

    # Paramètres

    - plateau : le plateau de jeu initial (on affiche la solution depuis
      le début de la partie)
    - n : le nombre de disques sur le plateau
    - coups : la liste des coups à jouer, sous la même forme que ce
      que donne `solution`
    """
    for dep, arr in coups:
        efface_disque(disque_superieur(plateau, dep), plateau, n)
        plateau[arr].append(plateau[dep].pop())
        dessine_config(plateau, n)
        time.sleep(1)
