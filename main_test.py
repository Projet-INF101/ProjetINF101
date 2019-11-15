import main

def test_init():
	plateau = main.init(4)
	assert len(plateau) == 3
