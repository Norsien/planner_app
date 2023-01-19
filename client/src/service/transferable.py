from ui.planepackage import PlanePackage
from ui.drawingplane import DrawingPlane
from ui.node import Node

def to_planePackage(planePackage_params):
    planePackage: PlanePackage = PlanePackage()

    planePackage.name = planePackage_params["name"]
    planePackage.planeList = []
    planes = planePackage_params["planes"]["edges"]
    for pl in planes:
        plane: DrawingPlane = to_plane(pl["node"])
        planePackage.add_plane(plane)
        if plane.name == planePackage_params["topPlane"]:
            planePackage.set_topPlane(plane)
    return planePackage

def to_plane(plane_params) -> DrawingPlane:
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
