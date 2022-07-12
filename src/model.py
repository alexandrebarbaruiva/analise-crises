"""
The following code was adapted from the Bank Reserves model included in Netlogo
Model information can be found at: http://ccl.northwestern.edu/netlogo/models/BankReserves
Accessed on: July 12, 2022
Author of NetLogo code:
    Wilensky, U. (1998). NetLogo Bank Reserves model.
    http://ccl.northwestern.edu/netlogo/models/BankReserves.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""

import mesa
import numpy as np

from agents import Building, Student, Tree

"""
If you want to perform a parameter sweep, call batch_run.py instead of run.py.
For details see batch_run.py in the same directory as run.py.
"""

# Start of datacollector functions


def get_num_healthy_agents(model):
    """return number of healthy agents"""

    healthy_agents = [
        a for a in model.schedule.agents if a.health >= model.healthy_threshold
    ]
    return len(healthy_agents)


def get_num_sick_agents(model):
    """return number of sick agents"""

    sick_agents = [
        a for a in model.schedule.agents if a.health < model.healthy_threshold
    ]
    return len(sick_agents)


class Charts(mesa.Model):

    # grid height
    grid_h = 20
    # grid width
    grid_w = 20

    """init parameters "init_students", "healthy_threshold"
       are all set via Slider"""

    def __init__(
        self,
        height=grid_h,
        width=grid_w,
        init_students=30,
        init_buildings=10,
        init_trees=20,
        healthy_threshold=1,
    ):
        self.height = height
        self.width = width
        self.init_students = init_students
        self.init_buildings = init_buildings
        self.init_trees = init_trees
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=True)
        # TODO: add resistant_threshold
        # healthy_threshold is the amount of health a person needs to be considered "healthy"
        self.healthy_threshold = healthy_threshold
        # see datacollector functions above
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Healthy": get_num_healthy_agents,
                "Sick": get_num_sick_agents,
            },
            agent_reporters={"Health": lambda x: x.health},
        )

        # create a single bank for the model
        # self.bank = Bank(1, self, self.reserve_percent)
        
        for i in range(self.init_trees):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            t = Tree(unique_id=i, pos=(x, y), model=self)
            self.grid.place_agent(t, (x, y))

        # set building positions
        buildings_positions = []
        for i in range(self.init_buildings):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            buildings_positions.append((x, y))
            b = Building(unique_id=i, pos=(x, y), model=self)
            self.grid.place_agent(b, (x, y))

        # create students for the model according to number of students set by user
        for i in range(self.init_students):
            # set x, y coords randomly within the grid
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)

            # TODO: later use code below for health
            # this_cell = self.grid.get_cell_list_contents([(x, y)])
            # health = len([obj for obj in this_cell if isinstance(obj, Building)])

            health = (
                0 if ((x, y) in buildings_positions or i == (init_students - 1)) else 1
            )
            s = Student(unique_id=i, pos=(x, y), model=self, moore=True, health=health)
            # place the Student object on the grid at coordinates (x, y)
            self.grid.place_agent(s, (x, y))
            # add the Student object to the model schedule
            self.schedule.add(s)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        # tell all the agents in the model to run their step function
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

    def run_model(self):
        for i in range(self.run_time):
            self.step()
