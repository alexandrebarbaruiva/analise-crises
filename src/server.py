import mesa

from portrayal import portray_cell
from model import ConwaysGameOfLife


# Make a world that is 50x50, on a 250x250 display.
canvas_element = mesa.visualization.CanvasGrid(portray_cell, 100, 100, 800, 800)

server = mesa.visualization.ModularServer(
    ConwaysGameOfLife, [canvas_element], "Game of Life", {"height": 100, "width": 100}
)
