# Même astuce que dans interface.py pour les imports
try:
    from turtle import up, goto, pencolor, update, clear, write, \
        window_width, window_height, bye, onkey, listen, numinput
except ImportError:
    funcs = [
        "up", "goto", "pencolor", "update", "clear", "write", "window_width",
        "window_height", "bye", "onkey", "listen", "numinput"
    ]
    for f in funcs:
        exec("def {}(*args, **kwargs):\n    pass\n".format(f))

import pickle
from typing import Any, Dict, List, Optional, Tuple
from interface import FONT_TITRE, FONT, dessine_plateau, dessine_config
from scores import lire_scores
from plateau import Plateau, init
from jeu import boucle_jeu, abandonner


def nouveau_menu() -> Tuple[int, int]:
    """
    Paramètre la fenêtre pour dessiner un nouveau menu.

    Renvoie les coordonées du coin en haut à gauche, pour positionner
    facilement les éléments du menu par la suite
    """
    clear()
    up()
    pencolor("#000000")
    larg = window_width() or 1920
    haut = window_height() or 1080
    # Les coordonnées du coin en haut à gauche
    x = larg / -2
    y = haut / 2
    return x, y


def scores_par_coup(
    scores: List[Dict[str, Any]]
) -> Dict[int, List[Dict[str, Any]]]:
    """
    Classe les scores, en les groupant par nombre de coups.

    # Paramètres

    - scores : la liste des scores, non classés
    """

    # Les clés de ce dictionnaire sont les nombres de disques,
    # et les valeurs les scores pour ce nombre de disques.
    res = {}
    for score in scores:
        if score["disks"] in res:
            res[score["disks"]].append(score)
        else:
            res[score["disks"]] = [score]

    for s in res:
        res[s] = sorted(res[s], key=lambda s: s["n_turn"])

    return res


def afficher_scores():
    """
    Affiche le tableau des scores dans la fenêtre Turtle.
    """
    scores = lire_scores()
    x, y = nouveau_menu()

    # Titre principal, centré en haut
    goto(0, y - 150)
    write(
        "Meilleurs scores",
        align="center",
        font=("Comic Sans MS", 16, "bold")
    )
    goto(0, y - 180)
    write(
        "Pour voir tous les scores, allez sur https://gelez.xyz/hanoi",
        align="center",
        font=FONT
    )
    goto(0, y - 200)
    write("Faites R pour revenir en arrière", align="center", font=FONT)

    # Le premier tableau
    goto(x + 60, y - 250)
    write("Par nombre de coups", font=FONT_TITRE)
    goto(x + 150, y - 280)
    write("Disques", align="right", font=FONT_TITRE)
    goto(x + 200, y - 280)
    write("Nom", font=FONT_TITRE)
    goto(x + 300, y - 280)
    write("Coups", font=FONT_TITRE)
    y -= 300
    par_coups = scores_par_coup(scores)
    n_disque = list(par_coups.keys())
    n_disque.reverse()
    for disques in n_disque:
        goto(x + 150, y)
        write(disques, align="right", font=FONT)
        # On affiche que les 5 premiers, parce que turtle ne permet
        # pas de scroller.
        for score in par_coups[disques][:5]:
            goto(x + 200, y)
            write(score["player"], font=FONT)
            goto(x + 300, y)
            write(score["n_turn"], font=FONT)
            y -= 20

    # Le second tableau
    goto(x + 60, y - 40)
    write("Par temps de rélexion", font=("Comic Sans MS", 16, "normal"))
    goto(x + 150, y - 70)
    write("Temps", align="right", font=FONT_TITRE)
    goto(x + 200, y - 70)
    write("Nom", font=FONT_TITRE)
    y -= 90
    for score in sorted(scores[:5], key=lambda s: s["median_time"]):
        goto(x + 150, y)
        write(
            str(round(score["median_time"] / 1000, 2)) + "s",
            align="right",
            font=FONT
        )
        goto(x + 200, y)
        write(score["player"], font=FONT)

        y -= 20
    update()
    listen()


def menu_principal():
    """
    Affiche le menu principal avec des explications et toutes les options.
    """
    x, y = nouveau_menu()

    # Titre principal, centré en haut
    goto(0, y - 150)
    write(
        "Les tours de Hanoï",
        align="center",
        font=("Comic Sans MS", 16, "bold")
    )
    goto(0, y - 180)
    write("Un super jeu par Hugo et Ana", align="center", font=FONT)

    # Présentation
    larg = window_width() or 1920
    x = (larg - 3000) / 2
    goto(x, y - 250)
    write(
        "Les tours de Hanoi sont un jeu de réflexion consistant à déplacer "
        "des disques de différents diamètres, d’une tour de départ à",
        font=FONT
    )
    goto(x, y - 270)
    write(
        "une tour d’arrivée, en passant par une tour intermédiaire, en un "
        "minimum de coups, tout en respectant les règles suivantes : ",
        font=FONT
    )
    goto(x, y - 290)
    write("  • on ne peut déplacer qu’un seul disque à la fois ;", font=FONT)
    goto(x, y - 310)
    write(
        "  • on ne peut pas placer un disque sur un disque plus "
        "petit que lui ;",
        font=FONT
    )
    goto(x, y - 330)
    write(
        "Dans la configuration de départ, les disques sont empilés en "
        "ordre décroissant de taille sur la tour de gauche. Dans la",
        font=FONT
    )
    goto(x, y - 350)
    write(
        "configuration finale, ils doivent être empilés dans le même "
        "ordre décroissant, mais sur la tour de droite.",
        font=FONT
    )

    # Menu
    goto(x, y - 450)
    write("J : jouer", font=FONT_TITRE)
    goto(x, y - 470)
    write("C : charger la sauvegarde", font=FONT_TITRE)
    goto(x, y - 490)
    write("S : scores", font=FONT_TITRE)
    goto(x, y - 510)
    write("Q : quitter", font=FONT_TITRE)

    onkey(lancer_partie, "j")
    onkey(charger_sauvegarde, "c")
    onkey(afficher_scores, "s")
    onkey(bye, "q")
    # Pour revenir au menu si on est dans le tableau des scores
    onkey(menu_principal, "r")
    update()
    listen()


def ecrire_consignes():
    """
    Affiche les consignes dans l'écran de jeu.

    Initialise aussi les raccourcis claviers pour le jeu.
    """
    x, y = nouveau_menu()
    larg = window_width() or 1920

    goto(larg + x - 100, y - 100)
    write("A : annuler", font=FONT_TITRE, align="right")
    goto(larg + x - 100, y - 120)
    write(
        "V : voir la solution (abandonne la partie)",
        font=FONT_TITRE,
        align="right"
    )
    goto(larg + x - 100, y - 140)
    write("Q : quitter (abandonne la partie)", font=FONT_TITRE, align="right")

    onkey(quitter, "q")
    onkey(charger_sauvegarde, "r")
    update()
    listen()


def quitter():
    """
    Quitte la partie en cours, et reviens au menu principal.
    """
    abandonner()
    menu_principal()


def lancer_partie(plateau: Optional[Plateau] = None):
    """
    Lance une nouvelle partie.

    # Paramètres

    - plateau : le plateau de départ. Si il vaut None, un nouveau plateau
      sera créé.
    """
    if plateau is None:
        n = int(numinput(
            "Tours de Hanoï",
            "Avec combien de disques voulez vous jouer ?",
            minval=1,
            default=3
        ) or 1)
        plateau = init(n)
    n = len(plateau[0]) + len(plateau[1]) + len(plateau[2])

    ecrire_consignes()
    dessine_plateau(n)
    dessine_config(plateau, n)
    boucle_jeu(plateau, n, afficher_scores)


def charger_sauvegarde():
    """
    Charge la sauvegarde de la dernière partie, et la lance.

    Si la sauvegarde ne peut pas être chargée, une nouvelle partie est lancée.
    """
    try:
        sauvegarde = open("sauvegarde", "rb")
        coups = pickle.load(sauvegarde)
        plateau = coups[list(coups.keys())[-1]]
        sauvegarde.close()
        lancer_partie(plateau)
    except Exception:
        lancer_partie()
