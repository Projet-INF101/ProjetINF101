import time

import src.interface as interface


# Les fonctions testées ici sont des fonctions d'affichage,
# et ne sont donc pas réellement testables.
# Ce test évite juste qu'elles faussent le pourcentage de
# code testé
def interface_test():
    interface.rectangle(0, 0, 10, 10, "#FF00FF", False)
    interface.dessine_plateau(3)
    interface.dessine_config([[3, 2, 1], [], []], 3)
    interface.efface_tout([[3, 2, 1], [], []], 3)
    interface.afficher_compteur(3)
    interface.chrono(0, lambda: True)
    interface.afficher_compteur(1)
