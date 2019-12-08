# Dans l'environnement de test GitHub on ne peut pas utiliser turtle
# (on a pas accès à une interface grapĥique).
# Si le module turtle ne peut pas être importé, on crée donc de fausses
# fonctions qui ne font rien.

try:
    from turtle import speed, up, bgcolor,       \
        fillcolor, down, goto, begin_fill,       \
        end_fill, pencolor, pensize, update,     \
        tracer, title, setup, hideturtle, write, \
        ontimer
except ImportError:
    # Code très sale, mais ça nous fait gagner quelques lignes répétitives
    funcs = [
        "speed", "up", "bgcolor", "fillcolor", "down", "goto", "begin_fill",
        "end_fill", "pencolor", "pensize", "update", "tracer", "title",
        "setup", "hideturtle", "write", "ontimer"
    ]
    for f in funcs:
        exec("def {}(*args, **kwargs):\n    pass\n".format(f))

from plateau import Plateau, position_disque

# On défini un certain nombre de constantes, pour éviter
# d'avoir des nombres « magiques » dans le code

"""
La largeur du plus petit disque
"""
LARG = 40

"""
La hauteur d'un disque
"""
HAUT = 30

"""
L'écart horizontal entre deux disques sur le plateau
"""
ECART = 20

# Les polices à utiliser par la suite
FONT_TITRE = ("Comic Sans MS", 16, "normal")
FONT = ("Comic Sans MS", 12, "normal")

# On configure d'abord turtle pour avoir un bel affichage.
# On chosit de contrôler manuellement les rafraîchissement de l'écran
# pour éviter d'avoir à attendre trop longtemps que les dessins s'affichent.
speed(0)
bgcolor("#FCFFFC")
pensize(5)
tracer(10000)
title("Un super jeu par Hugo et Ana : les tours de Hanoï")
setup(width=1.0, height=1.0)
hideturtle()
update()


def rectangle(
    x: int,
    y: int,
    lon: int,
    lar: int,
    couleur: str = "#000000",
    bord: bool = True
):
    """
    Fonction auxiliaire pour tracer un rectangle avec turtle.

    # Paramètres

    - x : la coordonée en abscisse du centre du rectangle
    - y : la coordonée en ordonnée du centre du rectangle
    - lon : la longueur du rectangle
    - lar : la largeur du rectangle
    - couleur : la couleur de fond du rectangle
    - bord: indique si il faut tracer la bordure ou non
    """
    fillcolor(couleur)
    if not bord:
        pencolor(couleur)
    else:
        pencolor("#000000")
    gauche = x - lon / 2
    droite = x + lon / 2
    haut = y + lar / 2
    bas = y - lar / 2
    up()
    begin_fill()
    goto(gauche, haut)
    down()
    goto(droite, haut)
    goto(droite, bas)
    goto(gauche, bas)
    goto(gauche, haut)
    end_fill()


def long_disque(n: int) -> int:
    """
    Fonction permettant de calculer la longueur d'un disque donné.

    # Paramètres

    - n : le numéro du disque dont on souhaite connaître la longueur
    """
    return n * LARG


def dessine_plateau(n: int):
    """
    Dessine un plateau de jeu vide.

    # Paramètres :

    - n : le nombre de disque que ce plateau pourra accueillir
    """
    rectangle(0, 0, long_disque(n + 1) * 3, HAUT, couleur="#040F0F")
    dessine_piliers(n)


def dessine_piliers(n: int):
    """
    Dessine les trois piliers du plateau.

    # Paramètres

    - n : le nombre de disque total sur le plateau
    """
    rectangle(
        -long_disque(n) - ECART,
        (n + 2) * HAUT / 2,
        LARG / 2,
        (n + 1) * HAUT,
        couleur="#2D3A3A"
    )
    rectangle(
        0,
        (n + 2) * HAUT / 2,
        LARG / 2,
        (n + 1) * HAUT,
        couleur="#2D3A3A"
    )
    rectangle(
        long_disque(n) + ECART,
        (n + 2) * HAUT / 2,
        LARG / 2,
        (n + 1) * HAUT,
        couleur="#2D3A3A"
    )


def dessine_disque(nd: int, plateau: Plateau, n: int):
    """
    Dessine un disque.

    # Paramètres

    - nd : le numéro du disque à dessiner
    - plateau : le plateau de jeu complet
      (nécéssaire pour connaître l'emplacement du disque)
    - n : le nombre total de disques sur le plateau de jeu
    """
    pos_x = position_disque(plateau, nd) - 1
    pos_y = plateau[pos_x + 1].index(nd) + 1
    rectangle(
        pos_x * (long_disque(n) + ECART),
        pos_y * HAUT,
        nd * LARG,
        HAUT,
        couleur="#248232"
    )
    update()


def efface_disque(nd: int, plateau: Plateau, n: int):
    """
    Efface un disque donné.

    # Paramètres

    - nd : le numéro du disque à dessiner
    - plateau : le plateau de jeu complet
      (nécéssaire pour connaître l'emplacement du disque)
    - n : le nombre total de disques sur le plateau de jeu
    """
    pos_x = position_disque(plateau, nd) - 1
    pos_y = plateau[pos_x + 1].index(nd) + 1
    rectangle(
        pos_x * (long_disque(n) + ECART),
        pos_y * HAUT,
        nd * LARG,
        HAUT,
        couleur="#FCFFFC",
        bord=False
    )
    dessine_piliers(n)
    dessine_plateau(n)
    update()


def dessine_config(plateau: Plateau, n: int):
    """
    Dessine l'ensemble des disques du plateau.

    - plateau : le plateau de jeu complet
    - n : le nombre total de disques sur le plateau de jeu
    """
    for tour in plateau:
        for disque in tour:
            dessine_disque(disque, plateau, n)


def efface_tout(plateau: Plateau, n: int):
    """
    Efface l'ensemble des disques du plateau.

    - plateau : le plateau de jeu complet
    - n : le nombre total de disques sur le plateau de jeu
    """
    for tour in plateau:
        for disque in tour:
            efface_disque(disque, plateau, n)


def chrono(temps: int, stop):
    """
    Fonction qui génère la fonction mettant à jour le chronomètre.

    # Paramètres

    - temps : le temps à afficher quand on mettra le chronomètre à jour
    - stop : une fonction qui permet de savoir si on doit continuer à
      afficher le chronomètre ou non.
    """
    def c():
        rectangle(0, -290, 100, 20, "#FCFFFC", False)
        if not stop():
            up()
            goto(0, -300)
            pencolor("#000000")
            write(str(temps) + "s", font=FONT, align="center")
            update()
            ontimer(chrono(temps + 1, stop), 1000)
    return c


def afficher_compteur(n: int):
    """
    Affiche un compteur de coups

    # Paramètres

    - n : le nombre de coups qui ont été joués
    """
    rectangle(0, -320, 100, 20, "#FCFFFC", False)
    up()
    pencolor("#000000")
    goto(0, -330)
    write(str(n) + " coup" + ("" if n < 2 else "s"), font=FONT, align="center")
    update()
