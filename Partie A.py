def init(n): #fonction qui renvoie la liste de la configuration initiale du plateau
    source_init = [] #creation de la sous liste source
    auxilary_init = [] #creation de la sous liste axilary
    destination = [] #creation de la sous liste destination
    plateau_init = [source_init,auxilary_init,destination] #creation de la liste composee des trois sous listes
    for i in range(n,0,-1): #on parcour tous les disques dans du plus grand au plus petit
        source_init.append(i) #on ajoute chaque disque dans l'ordre croissant de taille
    return plateau_init #on retourne la liste de la configuratino initiale

def nombre_disques(plateau, numtour): #fonction qui renvoie la configuration d'une des trois tours du plateau
    return len(plateau[numtour]) #renvoie la longueur de l'element liste d'indice numtour dans la liste plateau

def disque_superieur(plateau,numtour): #fonction qui renvoie le numero du disque superieur
    if len(plateau[numtour]) != 0: #si la liste n'est pas vide
        return plateau[numtour][len(plateau[numtour])-1] #on renvoie l'element avec le plus grand in indice dans la liste choisie, utilisation de l'astuce liste[indice de elem dans liste][indice de elem dans dans elem de liste]
    else: #si la liste est vide on renvoi -1
        return -1

def position_disque(plateau,numdisque): #fonction qui renvoie la tour ou se trouve le disque que l'on cherche
    position = 0 #compteur qui nous permet de donner la position
    for i in plateau: #on parcour les sous listes une par une
        for j in i: #on parcours les elements des sous listes un par un
            if j == numdisque: #si l'element d'une des sous liste correspond à l'element que l'on recherche
                return position #on renvoie la position de la sous liste dans laquelle se trouve le disque que l'on cherche
            position += 1 #sinon on incrémente la position

def verifier_deplacement(plateau,nt1,nt2): #fonction qui verifie si le deplacement effectue repond aux regles du jeu
    if len(nt1) != 0 and (disque_superieur(plateau,nt1) < disque_superieur(plateau,nt2) or len(nt2 == 0)): #si la configuration du jeu est en accord avec les regles du jeu 
        return True #on renvoie le booleen True
    return False #Sinon on renvoie le booleen False

#création d'une fonction intermediaire qui calcule la configuration que l'on doit obtenir à la fin
def liste_gagnante(n):
    liste = []
    for i in range(n,0,-1):
        liste.append(i)
    return liste

def verifier_victoire(plateau, n): #fonction qui verifie si il y a une configuration gagnant
    if len(plateau[2]) == n and plateau[2] == liste_gagnante(n): #on verifie les condition a une victoire
        return True #si oui, on revoie le booleen True
    return False #sinon le booleen False
