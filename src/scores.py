import requests
import json
from typing import Any, Dict, List

"""
L'URL de l'API pour enregistrer les scores
"""
URL = "https://gelez.xyz/hanoi/api/v1/scores"


def sauver_score(
    nom: str,
    nb_coup: int,
    temps_moyen: int,
    disques: int
) -> Dict[str, Any]:
    """
    Enregistre un nouveau score.

    Renvoie le nouveau score comme enregistré dans la base de donnée.

    # Paramètres :

    - nom : le nom du joueur.
    - nb_coup : le nombre de coups qu'il ou elle a fait.
    - temps_moyen: le temps moyen passé sur un coup, en millisecondes.
    - disques : le nombre de disques de cette partie
    """
    return requests.post(URL, data=json.dumps({
        "player": nom,
        "n_turn": nb_coup,
        "median_time": temps_moyen,
        "disks": disques,
    }), headers={
        "Content-Type": "application/json",
    }).json()


def lire_scores() -> List[Dict[str, Any]]:
    """
    Lis les scores déjà sauvegardés.
    """
    return requests.get(URL).json()
