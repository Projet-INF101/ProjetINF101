from copy import deepcopy
import pickle
import time
from typing import Callable, Tuple

try:
    from turtle import numinput, ontimer, listen, onkey, textinput
except ImportError:
    funcs = ["ontimer", "listen", "onkey"]
    for f in funcs:
        exec("def {}(*args, **kwargs):\n    pass\n".format(f))

    # Dans l'environnement de test, on fait comme si l'utilisateur
    # entrait en boucle 5, 2, 1, 5, 1 et 2
    res = [5, 2, 1, 5, 1, 2]
    messages = [
        "Tour de départ",
        "Entrez une valeur entre 1 et 3.",
        "Tour vide, choisissez en une autre.",
        "Tour d'arrivée",
        "Entrez une valeur entre 1 et 3.",
        "Déplacement incorrect.",
    ]
    x = 0

    def numinput(titre, msg, minval, maxval):
        global x
        x += 1
        assert msg == messages[(x - 1) % 6]
        return res[(x - 1) % 6]

    def textinput(titre, msg):
        return "Zoé"

from src.interface import dessine_config, efface_disque, chrono, \
    afficher_compteur
from src.plateau import Plateau, Historique, verifier_victoire, \
    verifier_deplacement, disque_superieur, init
from src.scores import sauver_score
from src.solution import solution, afficher_solution


def lire_coords(plateau: Plateau) -> Tuple[int, int]:
    """
    Lit et valide les coordonnées d'une tour de départ et d'une tour
    d'arrivée pour un plateau donné.

    # Paramètres

    - plateau : le plateau de jeu actuel
    """
    dep = -1
    message = "Tour de départ"
    while dep == -1:
        entree = int(numinput("Tours de Hanoï", message, minval=1, maxval=3))
        entree -= 1
        if 0 <= entree <= 2:
            if len(plateau[entree]) != 0:
                # On crée un liste contenant les deux tours d'arrivée
                # potentielles
                arrives = [0, 1, 2]
                arrives.pop(entree)

                if verifier_deplacement(plateau, entree, arrives[0]) \
                   or verifier_deplacement(plateau, entree, arrives[1]):
                    dep = entree
                else:
                    message = "Aucun déplacement possible depuis cette tour."
            else:
                message = "Tour vide, choisissez en une autre."
        else:
            message = "Entrez une valeur entre 1 et 3."

    arr = -1
    message = "Tour d'arrivée"
    while arr == -1:
        entree = int(numinput("Tours de Hanoï", message, minval=1, maxval=3))
        entree -= 1
        if 0 <= entree <= 2:
            if verifier_deplacement(plateau, dep, entree):
                arr = entree
            else:
                message = "Déplacement incorrect."
        else:
            message = "Entrez une valeur entre 1 et 3."

    return dep, arr


def jouer_un_coup(plateau: Plateau, n: int):
    """
    Joue un tour dans une partie.

    # Paramètres

    - plateau : le plateau de jeu au début de ce tour
    - n : le nombre de disques sur le plateau
    """
    coords = lire_coords(plateau)

    dep, arr = coords
    efface_disque(disque_superieur(plateau, dep), plateau, n)
    plateau[arr].append(plateau[dep].pop())
    dessine_config(plateau, n)


def dernier_coup(coups: Historique, derniercoup: int) -> Tuple[int, int]:
    """
    Renvoie la tour de départ et la tour d'arrivé joué lors d'un coup donné

    # Paramètres

    - coups : l'historique de jeu
    - derniercoup : le numéro du coup sur lequel on veut des informations
    """
    coup2 = coups[derniercoup]["plateau"]
    coup1 = coups[derniercoup - 1]["plateau"]

    # Ces listes contiennent chacune trois entiers, correspondant
    # à la taille des tours au coup donné et au coup précédent.
    len_config2 = []
    len_config1 = []

    for i in coup2:
        len_config2.append(len(i))
    for j in coup1:
        len_config1.append(len(j))

    tour_depart = None
    tour_arrive = None
    for l in range(3):
        if len_config2[l] < len_config1[l]:
            tour_depart = l
        if len_config2[l] > len_config1[l]:
            tour_arrive = l

    return tour_depart, tour_arrive


def annuler_dernier_coup(
    coups: Historique,
    der_coup: int,
    n: int,
    plateau: Plateau
):
    """
    Cette fonction annule un coup donné et met à jour l'affichage en fonction.

    # Paramètres

    - coups : l'historique de jeu
    - der_coup : le numéro du coup à annuler
    - n : le nombre total de disques sur le plateau
    - plateau : le plateau de jeu actuel
    """
    tour_depart, tour_arrive = dernier_coup(coups, der_coup)
    del coups[der_coup]
    efface_disque(disque_superieur(plateau, tour_arrive), plateau, n)
    plateau[tour_depart].append(plateau[tour_arrive].pop())
    dessine_config(plateau, n)

    # On met à jour le raccourci clavier d'annulation
    onkey(annuler_coup(coups, der_coup - 1, n, plateau), "a")
    listen()


def boucle_jeu(plateau: Plateau, n: int, victoire: Callable[[], None]):
    """
    Boucle de jeu principale.

    # Paramètres

    - plateau : le plateau de jeu au début de la partie
    - n : le nombre de disque sur le plateau
    - victoire : une fonction à appeler au moment de la victoire
    """
    global abandon
    abandon = False
    temps_depart = time.time()
    coups = {0: {"plateau": deepcopy(plateau), "temps": temps_depart}}
    lancer_chrono = chrono(0, lambda: abandon)
    lancer_chrono()

    onkey(voir_solution(n), "v")

    coup(plateau, n, coups, temps_depart, victoire)()


def reprendre_partie(coups: Historique, n: int, victoire: Callable[[], None]):
    """
    Fonction similaire à `boucle_jeu`, mais qui reprend une partie à partir
    d'un certain point.

    # Paramètres

    - coups : l'historique de la partie à reprendre
    - n : le nombre de disques de cette partie
    - victoire : une fonction à appeler au moment de la victoire
    """
    global abandon
    abandon = False
    temps_derniere_partie = round(
        coups[0]["temps"] - coups[nb_tour(coups)]["temps"]
    )
    temps_depart = time.time() - temps_derniere_partie
    lancer_chrono = chrono(temps_derniere_partie, lambda: abandon)
    plateau = coups[nb_tour(coups)]["plateau"]
    lancer_chrono()

    onkey(voir_solution(n), "v")

    coup(plateau, n, coups, temps_depart, victoire)()


def voir_solution(n: int) -> Callable[[], None]:
    """
    Une fonction qui en génère une autre, à appeler quand on veut voir
    la solution.

    # Paramètres

    - n : le nombre de disques à afficher dans la solution
    """
    def v():
        abandonner()
        sol = solution(n, 0, 1, 2)
        afficher_solution(init(n), n, sol)
    return v


"""
Variable globale permettant d'abandonner une partie à tout moment,
malgré le code asynchrone.
"""
abandon = False


def coup(
    plateau: Plateau,
    n: int,
    coups: Historique,
    temps_depart: int,
    victoire: Callable[[], None]
) -> Callable[[], None]:
    """
    Cette fonction est une fonction qui joue un coup si on a pas encore gagné,
    met l'affichage à jour en fonction de l'état actuel du jeu, et affiche
    l'écran de victoire si il le faut.

    Elle retourne une fonction sans paramètres que l'on peut passer
    à turtle.ontimer

    # Paramètres

    - plateau : le plateau au début de ce coup
    - n : le nombre de disques sur le plateau
    - coups : l'historique des coups
    - temps_départ : l'heure de début de la partie
    - victoire : la fonction à appeler au moment de la victoire
    """
    def c():
        """
        La fonction elle-même
        """
        if not(verifier_victoire(plateau, n)) and not abandon:
            afficher_compteur(nb_tour(coups))
            try:
                jouer_un_coup(plateau, n)
                coups[nb_tour(coups) + 1] = {
                    "plateau": deepcopy(plateau),
                    "temps": time.time() - temps_depart
                }

                sauvegarde = open("sauvegarde", "wb")
                pickle.dump(coups, sauvegarde)
                sauvegarde.close()

                # On met à jour le raccourci clavier pour annuler avec
                # le nouvel état de jeu
                onkey(annuler_coup(coups, nb_tour(coups), n, plateau), "a")

                # On laisse 2 secondes entre chaque coup avant d'ouvrir les
                # fenêtres qui demandent les numéros de tours, pour pouvoir
                # utiliser les raccourcis.
                listen()
                ontimer(coup(plateau, n, coups, temps_depart, victoire), 2000)
            except Exception:
                # Si les boites de dialogues sont fermées on aura une erreur.
                # On relance donc le même tour 2s plus tard dans ce cas.
                listen()
                ontimer(coup(plateau, n, coups, temps_depart, victoire), 2000)
        elif not abandon:
            temps = (time.time() - temps_depart) * 1000
            nb_coup = nb_tour(coups)
            if nb_coup == 0:
                nb_coup = 1
            sauver_score(
                textinput("Vous avez gagné !", "Quel est votre nom ?"),
                nb_coup,
                round(temps / nb_coup),
                n
            )
            abandonner()  # On « abandonne » pour arrêter la partie
            victoire()
    return c


def nb_tour(coups: Historique) -> int:
    """
    Renvoie le nombre de tours qui ont été joués pour un historique donné.

    # Paramètres

    - coups : l'historique de jeu
    """
    cles = list(coups.keys())
    cles.sort()
    try:
        return cles[-1]
    except Exception:
        return 0


def annuler_coup(
    coups: Historique,
    der_coup: int,
    n: int,
    plateau: Plateau
) -> Callable[[], None]:
    """
    Génère une fonction qu'on peut utiliser avec turtle.onkey, pour annuler
    un coup.

    # Paramètres

    - coups : l'historique des coups
    - der_coup : le numéro du coup à annuler
    - n : le nombre de disques sur le plateau
    - plateau : le plateau de jeu
    """
    def a():
        """
        La fonction en elle⁻même, qui ne fait qu'un seul appel
        à `annuler_dernier_coup`
        """
        annuler_dernier_coup(coups, der_coup, n, plateau)
    return a


def abandonner():
    """
    Une fonction qui abandonne la partie en cours.
    """
    global abandon
    abandon = True
