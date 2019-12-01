from typing import List
from turtle import *
from copy import deepcopy
import pickle
import time

# On définit des types qui permettent de rendre
# plus clairs la signature de nos fonctions par la suite.
Plateau = List[List[int]]

def init(n: int) -> Plateau:
    """
    Renvoie la liste de la configuration initiale du plateau.

    # Paramètres :

    - n : Le nombre de disques
    """
    source_init = [] # creation de la sous liste source
    auxilary_init = [] # creation de la sous liste axilary
    destination = [] # creation de la sous liste destination
    plateau_init = [source_init, auxilary_init, destination] # creation de la liste composee des trois sous listes
    for i in range(n, 0, -1): # on parcour tous les disques dans du plus grand au plus petit
        source_init.append(i) # on ajoute chaque disque dans l'ordre croissant de taille
    return plateau_init # on retourne la liste de la configuratino initiale

def nombre_disques(plateau: Plateau, numtour: int):
    """
    Renvoie la configuration d'une des trois tours du plateau.

    # Paramètres

    - plateau : le plateau de jeu
    - numtour : le numéro de la tour dont on veut connaître la « hauteur »
    """
    return len(plateau[numtour]) # renvoie la longueur de l'élément liste d'indice numtour dans la liste plateau

def disque_superieur(plateau: Plateau, numtour: int):
    """
    Renvoie le numéro du disque supérieur.

    # Paramètres

    - plateau : la plateau de jeu
    - numtour : la tour dont on veut connaître le disque supérieur
    """
    if len(plateau[numtour]) != 0: # si la liste n'est pas vide
        # on renvoie l'élément avec le plus grand in indice dans la liste choisie,
        # utilisation de l'astuce liste[indice de elem dans liste][indice de elem dans elem de liste]
        return plateau[numtour][len(plateau[numtour]) - 1]
    else:
        # si la liste est vide on renvoit -1
        return -1

def position_disque(plateau: Plateau, numdisque: int):
    """
    Renvoie la tour ou se trouve le disque que l'on cherche.

    Paramètres

    - plateau : le plateau de jeu
    - numdisque : le numéro du disque dont on veut connaître la position
    """
    position = 0 # compteur qui nous permet de donner la position
    for i in plateau: # on parcour les sous listes une par une
        for j in i: # on parcours les éléments des sous listes un par un
            if j == numdisque: # si l'élément d'une des sous liste correspond à l'élément que l'on recherche
                return position # on renvoie la position de la sous liste dans laquelle se trouve le disque que l'on cherche
        position += 1 # sinon on incrémente la position

def verifier_deplacement(plateau: Plateau, nt1: int, nt2: int):
    """
    Vérifie si le deplacement effectue repond aux regles du jeu.

    # Paramètres

    - plateau : le plateau de jeu
    - nt1 : le numéro de la tour d'origine
    - nt2 : le numéro de la tour d'arrivée
    """
    return (
        nombre_disques(plateau, nt1) != 0
        and (disque_superieur(plateau, nt1) < disque_superieur(plateau, nt2) or nombre_disques(plateau, nt2) == 0)
    )

def liste_gagnante(n: int):
    """
    Fonction intermédiaire qui calcule la configuration que l'on doit obtenir à la fin.

    # Paramètres

    - n : le nombre de plateaux dans la partie
    """
    liste = []
    for i in range(n, 0, -1):
        liste.append(i)
    return liste

def verifier_victoire(plateau: Plateau, n: int):
    """
    Vérifie si il y a une configuration gagnante.
    """
    return plateau[2] == liste_gagnante(n) # on vérifie les condition d'une victoire

def rectangle(x, y, lon, lar, couleur = "#000000", bord = True):
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
    goto(gauche,haut)
    down()
    goto(droite,haut)
    goto(droite,bas)
    goto(gauche,bas)
    goto(gauche,haut)
    end_fill()

LARG = 40
HAUT = 30
ECART = 20
speed(0)
bgcolor("#FCFFFC")
pensize(5)
tracer(10000)

def long_disque(n):
    return n * LARG

def dessine_plateau(n):
    rectangle(0, 0, long_disque(n + 1) * 3, HAUT, couleur = "#040F0F")
    dessine_piliers(n)

def dessine_piliers(n):
    rectangle(-long_disque(n) - ECART, (n + 2) * HAUT / 2, LARG / 2, (n + 1) * HAUT, couleur = "#2D3A3A")
    rectangle(0,                       (n + 2) * HAUT / 2, LARG / 2, (n + 1) * HAUT, couleur = "#2D3A3A")
    rectangle(long_disque(n) + ECART,  (n + 2) * HAUT / 2, LARG / 2, (n + 1) * HAUT, couleur = "#2D3A3A")

def dessine_disque(nd, plateau, n):
    pos_x = position_disque(plateau, nd) - 1
    pos_y = plateau[pos_x + 1].index(nd) + 1
    rectangle(pos_x * (long_disque(n) + ECART), pos_y * HAUT, nd * LARG, HAUT, couleur = "#248232")
    update()

def efface_disque(nd, plateau, n):
    pos_x = position_disque(plateau, nd) - 1
    pos_y = plateau[pos_x + 1].index(nd) + 1
    rectangle(pos_x * (long_disque(n) + ECART), pos_y * HAUT, nd * LARG, HAUT, couleur = "#FCFFFC", bord = False)
    dessine_piliers(n)
    dessine_plateau(n)
    update()

def dessine_config(plateau, n):
    for tour in plateau:
        for disque in tour:
            dessine_disque(disque, plateau, n)

def efface_tout(plateau: Plateau, n: int):
    for tour in plateau:
        for disque in tour:
            efface_disque(disque, plateau, n)

### PARTIE C ###

def lire_coords(plateau: Plateau) -> (int, int) :
    dep = 3
    while dep == 3:
        entree = int(input("Tour de départ (entrez -1 pour abandonner) : "))
        print(entree)
        if 0 <= entree <= 2:
            if len(plateau[entree]) != 0:
                arrives_possibles = [0, 1, 2]
                arrives_possibles.pop(entree)
                if verifier_deplacement(plateau, entree, arrives_possibles[0]) or verifier_deplacement(plateau, entree, arrives_possibles[1]):
                    dep = entree
                else:
                    print("Aucun déplacement possible depuis cette tour.")
            else:
                print("Tour vide, choisissez en une autre.")
        elif entree == -1:
            print("Abandon.")
            return
        else:
            print("Entrez une valeur entre 0 et 2.")

    arr = 3
    while arr == 3:
        entree = int(input("Tour d'arrivée : "))
        if 0 <= entree <= 2:
            if verifier_deplacement(plateau, dep, entree):
                arr = entree
            else:
                print("Déplacement incorrect")
        else:
            print("Entrez une valeur entre 0 et 2")

    return dep, arr

def jouer_un_coup(plateau: Plateau, n: int) -> bool:
    coords = lire_coords(plateau)
    if coords == None:
        return False # Abandon

    dep, arr = coords
    efface_disque(disque_superieur(plateau, dep), plateau, n)
    plateau[arr].append(plateau[dep].pop())
    dessine_config(plateau, n)
    return True

def dernier_coup(coups, derniercoup):
    coup2 = coups[derniercoup]
    coup1 = coups[derniercoup - 1]

    len_config2 = []
    len_config1 = []

    tour_depart = None
    tour_arrive = None

    for i in coup2:
        len_config2.append(len(i))
    for j in coup1:
        len_config1.append(len(j))

    for l in range(3):
        if len_config2[l] < len_config1[l]:
            tour_depart = l
        if len_config2[l] > len_config1[l]:
            tour_arrive = l

    return tour_depart,tour_arrive

def annuler_dernier_coup(coups,der_coup,n,plateau):
        tour_depart, tour_arrive = dernier_coup(coups,der_coup)
        del coups[der_coup]
        efface_disque(disque_superieur(plateau, tour_arrive), plateau, n)
        plateau[tour_depart].append(plateau[tour_arrive].pop())
        dessine_config(plateau, n)

def boucle_jeu(plateau, n):
    nb_tour = 0
    continuer = True
    coups = { 0: deepcopy(plateau) }
    while not(verifier_victoire(plateau,n)) or not(continuer):
        if input("annuler le dernier coup ?").lower() == "oui":
            annuler_dernier_coup(coups, nb_tour, n, plateau)
        else:
            continuer = jouer_un_coup(plateau,n)
            coups[nb_tour + 1] = deepcopy(plateau)
            nb_tour += 1

        if input("Enregistrer ?").lower() == "oui":
            sauvegarde = open("sauvegarde", "wb")
            pickle.dump(coups, sauvegarde)
            sauvegarde.close()
    return nb_tour

def solution(n, source, aux, dest):
    if n == 1:
        return [ (source, dest) ]
    else:
      return (solution(n - 1, source, dest, aux) +
             [ (source, dest) ] +
             solution(n - 1, aux, source, dest))

def afficher_solution(plateau, n, coups):
    for dep, arr in coups:
        efface_disque(disque_superieur(plateau, dep), plateau, n)
        plateau[arr].append(plateau[dep].pop())
        dessine_config(plateau, n)
        time.sleep(1)

if __name__ == "__main__":
    print("Bonjour ! Bienvenue dans le jeu des tours de Hanoï.")
    if input("Charger la sauvegarde ?").lower() == "oui":
        sauvegarde = open("sauvegarde", "rb")
        coups = pickle.load(sauvegarde)
        plateau = coups[list(coups.keys())[-1]]
        n = len(plateau[0]) + len(plateau[1]) + len(plateau[2])
        sauvegarde.close()
    else:
        n = int(input("Avec combien de disques voulez vous jouer ?"))
        plateau = init(n)
    dessine_plateau(n)
    dessine_config(plateau, n)
    boucle_jeu(plateau, n)
    if input("Afficher la solution ?").lower() == "oui":
        sol = solution(n, 0, 1, 2)
        afficher_solution(init(n), n, sol)
