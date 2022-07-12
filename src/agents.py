import mesa

from walk import RandomWalker


class Building(mesa.Agent):
    def __init__(self, unique_id: int, pos: tuple, model: mesa.Model):
        super().__init__(unique_id, model)
        self.pos = pos


class Tree(mesa.Agent):
    """
    A tree cell.

    Attributes:
        x, y: Grid coordinates
        condition: Can be "Fine", "On Fire", or "Burned Out"
        unique_id: (x,y) tuple.

    unique_id isn't strictly necessary here, but it's good
    practice to give one to each agent anyway.
    """

    def __init__(self, unique_id: int, pos: tuple, model: mesa.Model):
        super().__init__(unique_id, model)
        self.pos = pos
        self.condition = "Fine"
        self.fire_turn = 0
        self.burn_turn = 0

    def step(self):
        """
        If the tree is on fire, spread it to fine trees nearby.
        """
        if self.condition == "On Fire":
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if isinstance(neighbor, Tree) and neighbor.condition == "Fine":
                    neighbor.condition = "On Fire"
            self.fire_turn += 1

            if self.fire_turn > 10:
                self.fire_turn = 0
                self.condition = "Burned Out"

        if self.condition == "Burned Out":
            self.burn_turn += 1
            if self.burn_turn > 10:
                self.condition = "Fine"

        elif self.random.random() * 100 < 5:
                self.condition = "On Fire"


class Student(RandomWalker):
    def __init__(self, unique_id, pos, model, moore, health=1):
        super().__init__(unique_id, pos, model, moore=moore)
        # health
        # 1 - healthy
        # 0 - unhealthy
        self.health = health
        self.sick_turns = 0

    def check_infection(self):
        if self.health > 0:
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            in_building = (
                len([obj for obj in this_cell if isinstance(obj, Building)]) > 0
            )
            if not in_building:
                return
            sick_cellmate = (
                len([obj.health == 0 for obj in this_cell if isinstance(obj, Student)])
                > 0
            )
            if not sick_cellmate:
                return
            self.health = 0
        else:
            self.increase_sick_turn()

    def increase_sick_turn(self):
        if self.sick_turns < 20 and self.health == 0:
            self.sick_turns += 1
            return
        self.health = 1
        self.sick_turns = 0

    def step(self):
        self.check_infection()
        self.random_move()
