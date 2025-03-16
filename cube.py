from build123d import *
from ocp_vscode import show

def make_cube_hole(r: float, h: float, a: float):
    """
    Make a cube with a hole in the center.
    Parameters:
    r (int): Radius of the hole.
    h (int): Height of the cube.
    a (int): Side of the cube.
    """
    if r > a/2:
        raise ValueError("Hole exceeds a size of the cube.")
    cube = Box(a, a, h)
    cylinder = Cylinder(r, h)
    return cube - cylinder

if __name__ == "__main__":
    r = 10
    h = 20
    a = 30
    cube = make_cube_hole(r, h, a)
    show(cube)