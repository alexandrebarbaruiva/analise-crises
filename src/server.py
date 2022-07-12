import mesa

from agents import Student, Building, Tree
from model import Charts

"""
Citation:
The following code was adapted from server.py at
https://github.com/projectmesa/mesa/blob/main/examples/wolf_sheep/wolf_sheep/server.py
Accessed on: July 12, 2022
Author of original code: Taylor Mutch
"""

# The colors here are taken from Matplotlib's tab10 palette
# Green
HEALTHY_COLOR = "#2ca02c"
# Red
SICK_COLOR = "#d62728"
# Blue
BUILDING_COLOR = "#1f77b4"


def agents_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if isinstance(agent, Building):
        portrayal["Shape"] = "rect"
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["r"] = 0.5
        portrayal["Layer"] = 0
        portrayal["Filled"] = "true"

        portrayal["Color"] = BUILDING_COLOR

    if isinstance(agent, Tree):
        shape = {
            "On Fire": "resources/tree-fire.png",
            "Fine": "resources/tree.png",
            "Burned Out": "resources/tree-burnt.png",
        }
        portrayal["Shape"] = shape[agent.condition]
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["r"] = 0.5
        portrayal["Layer"] = 1
        portrayal["Filled"] = "true"

        portrayal["Color"] = BUILDING_COLOR

    # update portrayal characteristics for each Student object
    elif isinstance(agent, Student):
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.5
        portrayal["Layer"] = 2
        portrayal["Filled"] = "true"
        portrayal["scale"] = 0.5

        color = HEALTHY_COLOR

        # set agent color based on health status
        if agent.health > 0:
            color = HEALTHY_COLOR
        else:
            color = SICK_COLOR

        portrayal["Color"] = color

    return portrayal


# dictionary of user settable parameters - these map to the model __init__ parameters
model_params = {
    "init_students": mesa.visualization.Slider(
        name="Students",
        value=25,
        min_value=1,
        max_value=200,
        description="Initial Number of Students",
    ),
    "healthy_threshold": mesa.visualization.Slider(
        name="Healthy Threshold",
        value=1,
        min_value=1,
        max_value=5,
        description="Upper End of Random Initial Healthy Students",
    ),
}

# set the portrayal function and size of the canvas for visualization
canvas_element = mesa.visualization.CanvasGrid(agents_portrayal, 20, 20, 500, 500)

# map data to chart in the ChartModule
line_chart = mesa.visualization.ChartModule(
    [
        {"Label": "Healthy", "Color": HEALTHY_COLOR},
        {"Label": "Sick", "Color": SICK_COLOR},
    ]
)

model_bar = mesa.visualization.BarChartModule(
    [
        {"Label": "Healthy", "Color": HEALTHY_COLOR},
        {"Label": "Sick", "Color": SICK_COLOR},
    ]
)

tree_line_chart = mesa.visualization.ChartModule(
    [
        {"Label": "Fine", "Color": HEALTHY_COLOR},
        {"Label": "On Fire", "Color": SICK_COLOR},
        {"Label": "Burned Out", "Color": BUILDING_COLOR},
    ]
)

# agent_bar = mesa.visualization.BarChartModule(
#     [{"Label": "Health", "Color": HEALTHY_COLOR}],
#     scope="agent",
#     sorting="ascending",
#     sort_by="Health",
# )

pie_chart = mesa.visualization.PieChartModule(
    [
        {"Label": "Healthy", "Color": HEALTHY_COLOR},
        {"Label": "Sick", "Color": SICK_COLOR},
    ]
)

# create instance of Mesa ModularServer
server = mesa.visualization.ModularServer(
    Charts,
    [canvas_element, line_chart, model_bar, pie_chart, tree_line_chart],
    "Mesa Charts",
    model_params=model_params,
)
