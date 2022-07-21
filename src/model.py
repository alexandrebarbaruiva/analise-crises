import mesa

from cell import Cell


class ConwaysGameOfLife(mesa.Model):
    """
    Represents the 2-dimensional array of cells in Conway's
    Game of Life.
    """

    def __init__(self, width=500, height=500):
        """
        Create a new playing area of (width, height) cells.
        """

        # Set up the grid and schedule.

        # Use SimultaneousActivation which simulates all the cells
        # computing their next state simultaneously.  This needs to
        # be done because each cell's next state depends on the current
        # state of all its neighbors -- before they've changed.
        self.schedule = mesa.time.SimultaneousActivation(self)

        # Use a simple grid, where edges wrap around.
        self.grid = mesa.space.Grid(width, height, torus=True)

        # Place a cell at each location, with some initialized to
        # ALIVE and some to DEAD.
        for (contents, x, y) in self.grid.coord_iter():
            cell = Cell((x, y), self)
            if self.random.random() < 0.1:
                cell.state = cell.ALIVE
            self.grid.place_agent(cell, (x, y))
            self.schedule.add(cell)

        self.running = True
        
    def generate_random_cells(self, new_cells=60):
        for (contents, x, y) in self.grid.coord_iter():
            # if added new_cells, end
            if new_cells == 0:
                print("added all cells")
                return
            
            # if already has cell, skip
            # breakpoint()
            cell = self.grid.get_cell_list_contents((x, y))[0]
            if cell.state == Cell.ALIVE:
                continue

            if self.random.random() < 0.01:
                cell.state = Cell.ALIVE
                new_cells -= 1

    def step(self):
        """
        Have the scheduler advance each cell by one step
        """
        if self.random.random() < 0.1:
            self.generate_random_cells()
        self.schedule.step()

