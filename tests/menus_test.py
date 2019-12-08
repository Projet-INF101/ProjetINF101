import src.menus as menus


def test_scores_par_coup():
    scores = [
        {
            "disks": 2,
            "n_turn": 12,
            "median_time": 600,
            "player": "Alice",
        },
        {
            "disks": 2,
            "n_turn": 14,
            "median_time": 750,
            "player": "Bob",
        },
        {
            "disks": 3,
            "n_turn": 16,
            "median_time": 420,
            "player": "Claude",
        },
    ]

    classement = menus.scores_par_coup(scores)

    assert classement == {
        2: [scores[0], scores[1]],
        3: [scores[2]],
    }


# Les fonctions testées ici sont des fonctions d'affichage,
# et ne sont donc pas réellement testables.
# Ce test évite juste qu'elles faussent le pourcentage de
# code testé
def test_menus():
    menus.menu_principal()
    menus.afficher_scores()
    menus.ecrire_consignes()
    menus.lancer_partie([[], [], []])
    menus.charger_sauvegarde()
    menus.quitter()
