from manim import *

def construct_allfours(chest, belly):
    left_shoulder_joint = Circle().set_stroke(None, 0).set_fill(GREEN_A, opacity=1).scale(0.2).\
        next_to(chest, direction=LEFT, buff=0.05).shift(UP*0.5)
    right_shoulder_joint = Circle().set_stroke(None, 0).set_fill(BLUE_B, opacity=1).scale(0.2).\
        next_to(chest, direction=RIGHT, buff=0.05).shift(UP*0.5)
    left_thigh_joint = Circle().set_stroke(None, 0).set_fill(PURPLE_B, opacity=1).scale(0.2).\
        next_to(belly, direction=DOWN, buff=0.1).shift(LEFT*0.5)
    right_thigh_joint = Circle().set_stroke(None, 0).set_fill(PINK, opacity=1).scale(0.2).\
        next_to(belly, direction=DOWN, buff=0.1).shift(RIGHT*0.5)
    
    left_big_arm = Rectangle(width=1, height=0.3, stroke_width=0, fill_color=GREEN_A, fill_opacity=1).\
    next_to(left_shoulder_joint, direction=LEFT, buff=0.05)
    right_big_arm = Rectangle(width=1, height=0.3, stroke_width=0, fill_color=BLUE_B, fill_opacity=1).\
    next_to(right_shoulder_joint, direction=RIGHT, buff=0.05)
    left_thigh = Rectangle(width=0.5, height=1.4, stroke_width=0, fill_color=PURPLE_B, fill_opacity=1).\
    next_to(left_thigh_joint, direction=DOWN, buff=0.05)
    right_thigh = Rectangle(width=0.5, height=1.4, stroke_width=0, fill_color=PINK, fill_opacity=1).\
    next_to(right_thigh_joint, direction=DOWN, buff=0.05)

    left_elbow_joint = Circle().set_stroke(None, 0).set_fill(PINK, opacity=1).scale(0.15).\
        next_to(left_big_arm, direction=LEFT, buff=0.1)
    right_elbow_joint = Circle().set_stroke(None, 0).set_fill(GREEN_A, opacity=1).scale(0.15).\
        next_to(right_big_arm, direction=RIGHT, buff=0.1)
    left_knee_joint = Circle().set_stroke(None, 0).set_fill(BLUE_B, opacity=1).scale(0.2).\
        next_to(left_thigh, direction=DOWN, buff=0.1)
    right_knee_joint = Circle().set_stroke(None, 0).set_fill(PURPLE_B, opacity=1).scale(0.2).\
        next_to(right_thigh, direction=DOWN, buff=0.1)
    
    left_forearm = Rectangle(width=0.3, height=1, stroke_width=0, fill_color=GREEN_A, fill_opacity=1).\
    next_to(left_elbow_joint, direction=UP, buff=-0.15)
    right_forearm = Rectangle(width=0.3, height=1, stroke_width=0, fill_color=BLUE_B, fill_opacity=1).\
    next_to(right_elbow_joint, direction=UP, buff=-0.15)
    left_leg = Rectangle(width=0.5, height=1.4, stroke_width=0, fill_color=PURPLE_B, fill_opacity=1).\
    next_to(left_knee_joint, direction=DOWN, buff=0.05)
    right_leg = Rectangle(width=0.5, height=1.4, stroke_width=0, fill_color=PINK, fill_opacity=1).\
    next_to(right_knee_joint, direction=DOWN, buff=0.05)

    left_wrist = Circle().set_stroke(None, 0).set_fill(RED, opacity=1).scale(0.12).\
        next_to(left_forearm, direction=UP, buff=0.03)
    right_wrist = Circle().set_stroke(None, 0).set_fill(RED, opacity=1).scale(0.12).\
        next_to(right_forearm, direction=UP, buff=0.03)
    left_hand = Triangle().set_fill(YELLOW_C, opacity=1).scale(0.3).next_to(left_wrist, direction=UP, buff=0.05)
    right_hand = Triangle().set_fill(YELLOW_C, opacity=1).scale(0.3).next_to(right_wrist, direction=UP, buff=0.05)

    left_ankle_joint = Circle().set_stroke(None, 0).set_fill(WHITE, opacity=1).scale(0.15).\
        next_to(left_leg, direction=DOWN, buff=0.05)
    right_ankle_joint = Circle().set_stroke(None, 0).set_fill(WHITE, opacity=1).scale(0.15).\
        next_to(right_leg, direction=DOWN, buff=0.05)
    left_foot_shape = [
        [0.25, 0.15, 0],
        [-0.25, 0.15, 0],
        [-0.35, -0.15, 0],
        [0.25, -0.15, 0],
    ]
    right_foot_shape = [
        [0.25, 0.15, 0],
        [-0.25, 0.15, 0],
        [-0.25, -0.15, 0],
        [0.35, -0.15, 0],
    ]
    left_foot = Polygon(*left_foot_shape, stroke_width=0, fill_color=WHITE, fill_opacity=1).\
    next_to(left_ankle_joint, direction=DOWN, buff=0.05).shift(LEFT*0.1)
    right_foot = Polygon(*right_foot_shape, stroke_width=0, fill_color=WHITE, fill_opacity=1).\
    next_to(right_ankle_joint, direction=DOWN, buff=0.05).shift(RIGHT*0.1)

    return left_shoulder_joint, right_shoulder_joint, left_thigh_joint, right_thigh_joint, left_thigh, right_thigh,\
    left_big_arm, right_big_arm, left_elbow_joint, right_elbow_joint, left_knee_joint, right_knee_joint, \
    left_forearm, right_forearm, left_leg, right_leg, left_wrist, right_wrist, left_hand, right_hand, \
    left_ankle_joint, right_ankle_joint, left_foot, right_foot