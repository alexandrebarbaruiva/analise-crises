from random import choice


def get_cell_color(cell):
    colors = {}
    colors["RED"] = "#2ca02c"
    colors["BLUE"] = "#d62728"
    colors["GREEN"] = "#1f77b4"
    colors["YELLOW"] = "#cbda32"
    colors["WHITE"] = "#ffffff"

    if not cell.is_alive:
        return colors["WHITE"]

    options = list(colors.keys())
    return choice(options)


def portray_cell(cell):
    """
    This function is registered with the visualization server to be called
    each tick to indicate how to draw the cell in its current state.
    :param cell:  the cell in the simulation
    :return: the portrayal dictionary.
    """
    if cell is None:
        raise AssertionError
    portrayal = {}
    portrayal["Shape"] = "rect"
    portrayal["w"] = 1
    portrayal["h"] = 1
    portrayal["Filled"] = "true"
    portrayal["Layer"] = 0
    portrayal["x"] = cell.x
    portrayal["y"] = cell.y
    portrayal["Color"] = get_cell_color(cell)

    # return {
    #     "Shape": "rect",
    #     "w": 1,
    #     "h": 1,
    #     "Filled": "true",
    #     "Layer": 0,
    #     "x": cell.x,
    #     "y": cell.y,
    #     "Color": "black" if cell.isAlive else "white",
    # }
    return portrayal
