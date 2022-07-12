import mesa
from mesa import time, space, datacollection
import matplotlib.pyplot as plt
import numpy as np


def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    return 1 + (1 / N) - 2 * B


class MoneyAgent(mesa.Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1
        self.sick = 0

    def step(self):
        # The agent's step will go here.
        self.move()

        if self.wealth > 0:
            self.give_money()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=True
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

        self.sick = 0

        # couldn't walk because agent is sick
        if self.pos == new_position:
            self.sick = 1

    def give_money(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = self.random.choice(cellmates)
            other.wealth += 1
            self.wealth -= 1

            if other.sick or self.sick:
                sick_or_not = [0, 1]
                other.sick = self.random.choice(sick_or_not)
                self.sick = self.random.choice(sick_or_not)


class MoneyModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, N, width=10, height=10):
        self.num_agents = N
        self.grid = space.MultiGrid(width, height, torus=True)
        self.schedule = time.RandomActivation(self)
        # Create agents
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)

            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
        
        self.datacollector = datacollection.DataCollector(
            model_reporters={"Gini": compute_gini},
            agent_reporters={"Wealth": "wealth", "Sick": "sick"}
        )

    def step(self):
        """Advance the model by one step."""
        self.datacollector.collect(self)
        self.schedule.step()
        for agent in self.schedule.agents:
            plural = "s" if agent.wealth > 1 else ""
            print(f"Hi, I am agent {agent.unique_id} with {agent.wealth} coin{plural}.")


if __name__ == "__main__":
    model = MoneyModel(50, 10, 10)
    for i in range(100):
        model.step()

    agent_counts = np.zeros((model.grid.width, model.grid.height))

    for cell in model.grid.coord_iter():
        cell_content, x, y = cell
        agent_count = len(cell_content)
        agent_counts[x][y] = agent_count
        
    gini = model.datacollector.get_model_vars_dataframe()
    gini.plot()
    plt.show()
    
    agent = model.datacollector.get_agent_vars_dataframe()
    print(agent.head())
    
    end = agent.xs(99, level="Step")
    # import ipdb; ipdb.set_trace()
    end_wealth = end["Wealth"]
    end_wealth.hist(bins=range(agent.Wealth.max() + 1))
    plt.show()
    
    end_sick = end["Sick"]
    end_sick.hist(bins=range(agent.Sick.max() + 3))
    plt.show()
    
    one_agent_wealth = agent.xs(14, level="AgentID")
    one_agent_wealth.Wealth.plot()
    plt.show()
    one_agent_wealth.Sick.plot()
    plt.show()

    # plt.imshow(agent_counts, interpolation="nearest")
    # plt.colorbar()
    # plt.show()

    # all_wealth = []
    # for j in range(100):
    #     model = MoneyModel(50, 10, 10)
    #     for i in range(10):
    #         model.step()

    #     for agent in model.schedule.agents:
    #         all_wealth.append(agent.wealth)

    # plt.hist(all_wealth, bins=range(max(all_wealth) + 1))
    # plt.show()
