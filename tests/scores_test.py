import src.scores as scores


def test_sauver_score():
    score = scores.sauver_score("Alice", 5, 2500, 10)

    assert score["player"] == "Alice"
    assert score["n_turn"] == 5
    assert score["median_time"] == 2500
    assert score["disks"] == 10


def test_lire_scores():
    liste_scores = scores.lire_scores()
    for s in liste_scores:
        if s["player"] == "Alice":
            assert s["n_turn"] == 5
            assert s["median_time"] == 2500
            assert s["disks"] == 10
