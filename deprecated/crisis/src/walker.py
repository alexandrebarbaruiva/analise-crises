"""
Citation:
The following code is a modified copy from random_walk.py at
https://github.com/projectmesa/mesa/blob/main/examples/wolf_sheep/wolf_sheep/random_walk.py
Accessed on: July 12, 2022
Original Author: Jackie Kazil

Generalized behavior for random walking, one grid cell at a time.
"""

import mesa
from mesa import time, space, datacollection
import matplotlib.pyplot as plt
import numpy as np


class RandomWalker(mesa.Agent):
    """
    Class implementing random walker methods in a generalized manner.
    Not intended to be used on its own, but to inherit its methods to multiple
    other agents.
    """

    grid = None
    x = None
    y = None
    # use a Moore neighborhood
    moore = True

    def __init__(self, unique_id, pos, model, moore=True):
        """
        grid: The MultiGrid object in which the agent lives.
        x: The agent's current x coordinate
        y: The agent's current y coordinate
        moore: If True, may move in all 8 directions.
                Otherwise, only up, down, left, right.
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore

    def random_move(self):
        """
        Step one cell in any allowable direction.
        """
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.pos, moore=self.moore, include_center=True)
        next_move = self.random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)
