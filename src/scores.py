import requests
import json

URL = "https://gelez.xyz/hanoi/api/v1/scores"

def sauver_score(nom, nb_coup, temps_moyen, disques):
    return requests.post(URL, data = json.dumps({
        "player": nom,
        "n_turn": nb_coup,
        "median_time": temps_moyen,
        "disks": disques,
    }), headers = {
        "Content-Type": "application/json",
    }).json()

def lire_scores():
    return requests.get(URL).json()
