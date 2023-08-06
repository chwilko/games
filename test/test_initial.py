import numpy as np

from game.PanGameTree import PanGame


def test_hand():
    ass0 = np.ones(6) * 4
    ass0[0] -= 1
    ass1 = np.ones(2) * 12
    ass1[0] -= 1
    for _ in range(100):
        pg = PanGame.play()
        assert (ass0 == pg.root.params.sum(axis=0)).all()
        assert (ass1 == pg.root.params.sum(axis=1)).all()
        assert pg.root.stack._stack == [0]
