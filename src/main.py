from typing import List

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
