from ui.drawingplane import DrawingPlane
from ui.node import Node

def to_plane(plane_params):
    plane = DrawingPlane()

    plane.width = plane_params["width"]
    plane.height = plane_params["height"]
    plane.name = plane_params["name"]
    plane.nodeList = []
    elements = plane_params["elements"]["edges"]
    for ele in elements:
        node = to_node(ele["node"])
        plane.put_node(node)
    return plane

def to_node(node_params):
    pos = [node_params["posX"], node_params["posY"]]
    node = Node(pos)
    node.name = node_params["name"]
    node.shortDescription = node_params["description"]
    return node
