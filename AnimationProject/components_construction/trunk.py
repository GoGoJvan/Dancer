from manim import *

def construct_trunk(Head: VGroup):
    body_shape = [
        [0.65, 0, 0],
        [-0.65, 0, 0],
        [-0.5, -2, 0],
        [0.5, -2, 0],
    ]
    chest = Triangle().set_fill(BLUE_A, opacity=1).scale(1).rotate(PI/3).next_to(Head, direction=DOWN, buff=0.1)
    waist = Polygon(*body_shape, color=BLUE_A).next_to(Head, direction=DOWN, buff=0.1).set_fill(TEAL_A, opacity=1)
    belly = Triangle().set_fill(WHITE, opacity=1).scale(0.7).next_to(Head, direction=DOWN, buff=1.3)
    return chest, waist, belly