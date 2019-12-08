import src.solution as sol


def test_solution():
    s = sol.solution(3, 0, 1, 2)

    assert s == [
        (0, 2),
        (0, 1),
        (2, 1),
        (0, 2),
        (1, 0),
        (1, 2),
        (0, 2),
    ]


def test_afficher_solution():
    plateau = [[3, 2, 1], [], []]
    sol.afficher_solution(plateau, 3, sol.solution(3, 0, 1, 2))
    assert plateau == [[], [], [3, 2, 1]]
