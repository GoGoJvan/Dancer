from manim import *
import numpy as np
import random as rd
import librosa
# import soundfile as sf
from components_construction.head import construct_head
from components_construction.trunk import construct_trunk
from components_construction.allfours import construct_allfours

class Robot(Scene):
    def config_window(self):
        self.add(NumberPlane(x_range=[-3, 3, 1], y_range=[-3, 3, 1]))
        # self.camera.background_color = "#ece6e2"

    def construct_dancer(self, width=1.5, height=1.2):
        self.head = construct_head(width, height)
        self.chest, self.waist, self.belly = construct_trunk(self.head)
        self.left_shoulder_joint, self.right_shoulder_joint, self.left_thigh_joint, self.right_thigh_joint, self.left_thigh, self.right_thigh,\
    self.left_big_arm, self.right_big_arm, self.left_elbow_joint, self.right_elbow_joint, self.left_knee_joint, self.right_knee_joint, \
    self.left_forearm, self.right_forearm, self.left_shank, self.right_shank, self.left_wrist, self.right_wrist, self.left_hand, self.right_hand, \
    self.left_ankle_joint, self.right_ankle_joint, self.left_foot, self.right_foot = construct_allfours(self.chest, self.belly)

        self.Dancer = VGroup(self.head, self.waist, self.belly, self.chest, self.left_shoulder_joint, self.right_shoulder_joint, 
                self.left_thigh_joint, self.right_thigh_joint, self.left_big_arm, self.right_big_arm, self.left_thigh, self.right_thigh,
                self.left_elbow_joint, self.right_elbow_joint, self.left_knee_joint, self.right_knee_joint,
                self.left_forearm, self.right_forearm, self.left_shank, self.right_shank, self.left_wrist, self.right_wrist, self.left_hand, self.right_hand,
                self.left_ankle_joint, self.right_ankle_joint, self.left_foot, self.right_foot
                ).scale(0.7).shift(UP*2)
        self.left_arm = VGroup(self.left_big_arm, self.left_forearm, self.left_wrist, self.left_hand, self.left_elbow_joint)
        self.right_arm = VGroup(self.right_big_arm, self.right_forearm, self.right_wrist, self.right_hand, self.right_elbow_joint)

        self.left_elbow = VGroup(self.left_forearm, self.left_wrist, self.left_hand)
        self.right_elbow = VGroup(self.right_forearm, self.right_wrist, self.right_hand)
        self.left_leg = VGroup(self.left_thigh, self.left_foot, self.left_ankle_joint, self.left_shank, self.left_knee_joint)
        self.right_leg = VGroup(self.right_thigh, self.right_foot, self.right_ankle_joint, self.right_shank, self.right_knee_joint)
        self.left_lowerleg = VGroup(self.left_foot, self.left_ankle_joint, self.left_shank)
        self.right_lowerleg = VGroup(self.right_foot, self.right_ankle_joint, self.right_shank)

    def deploy_heart(self):
        self.play(Rotating(self.left_arm, radians=-PI/3.5, about_point=self.left_shoulder_joint.get_center(), rate_func=linear),
                Rotating(self.right_arm, radians=PI/3.5, about_point=self.right_shoulder_joint.get_center(), rate_func=linear),
                run_time=1)
        self.play(Rotating(self.left_hand, radians=-PI/2, about_point=self.left_wrist.get_center(), rate_func=linear),
                Rotating(self.right_hand, radians=PI/2, about_point=self.right_wrist.get_center(), rate_func=linear),
                run_time=0.5)
        self.play(Rotating(self.left_arm, radians=PI/3.5 + PI/2, about_point=self.left_shoulder_joint.get_center(), rate_func=linear),
                Rotating(self.right_arm, radians=-PI/3.5 - PI/2, about_point=self.right_shoulder_joint.get_center(), rate_func=linear),
                run_time=1)
        self.play(Rotating(self.left_hand, radians=PI, about_point=self.left_wrist.get_center(), rate_func=linear),
                Rotating(self.right_hand, radians=-PI, about_point=self.right_wrist.get_center(), rate_func=linear),
                run_time=0.5)
        redraw_hand = ValueTracker(0)
        half_left_hand = [
            [0, 0.1, 0],
            [-0.2, -0.1, 0],
            [-0.2, 0.1, 0],
        ]
        half_right_hand = [
            [0, 0.1, 0],
            [0.2, -0.1, 0],
            [0.2, 0.1, 0],
        ]
        self.left_hand.add_updater(lambda x:x.become(Polygon(*half_left_hand).scale(1.5).\
                                                    set_fill(YELLOW_C, opacity=1).move_to(x.get_center())) if redraw_hand.get_value() == 1 else 
                                                    x.become(Triangle().set_fill(YELLOW_C, opacity=1).scale(0.3).next_to(self.left_wrist, direction=UP, buff=0.05))
                                                    if redraw_hand.get_value() == 2 else x)
        self.right_hand.add_updater(lambda x:x.become(Polygon(*half_right_hand).scale(1.5).\
                                                    set_fill(YELLOW_C, opacity=1).move_to(x.get_center())) if redraw_hand.get_value() == 1 else
                                                    x.become(Triangle().set_fill(YELLOW_C, opacity=1).scale(0.3).next_to(self.left_wrist, direction=UP, buff=0.05))
                                                    if redraw_hand.get_value() == 2 else x)
        self.add(self.left_hand, self.right_hand)
        self.play(redraw_hand.animate.set_value(1), run_time=0.1)
        self.play(Rotating(self.left_elbow, radians=-PI, about_point=self.left_elbow_joint.get_center(), rate_func=linear),
                Rotating(self.right_elbow, radians=PI, about_point=self.right_elbow_joint.get_center(), rate_func=linear),
                run_time=1)
        self.play(redraw_hand.animate.set_value(2), run_time=0.1)
        self.left_hand.clear_updaters()
        self.right_hand.clear_updaters()

    def roration_restriction(self, mob: Mobject, angle, about_point, joint_type, block=True):
        match joint_type:
            case "Lshoulder":
                line1 = Line(self.left_shoulder_joint.get_center(), self.right_shoulder_joint.get_center())
                line2 = Line(self.left_shoulder_joint.get_center(), self.left_elbow_joint.get_center())
                try:
                    measure_angle = Angle(line1, line2).get_value()
                    if (measure_angle <= PI*0.5 and angle < 0) | (measure_angle >= PI*1.5 and angle > 0):
                        angle = 0 if block else -angle
                except ValueError:
                    pass
            case "Rshoulder":
                line1 = Line(self.right_shoulder_joint.get_center(), self.left_shoulder_joint.get_center())
                line2 = Line(self.right_shoulder_joint.get_center(), self.right_elbow_joint.get_center())
                try:
                    measure_angle = Angle(line1, line2).get_value()
                    if (measure_angle <= PI*0.5 and angle < 0) | (measure_angle >= PI*1.5 and angle > 0):
                        angle = 0 if block else -angle
                        
                except ValueError:
                    pass
            case "Lelbow" | "Relbow":
                pass
            case "Lwrist":
                line1 = Line(self.left_wrist.get_center(), self.left_elbow_joint.get_center())
                line2 = Line(self.left_wrist.get_center(), self.left_hand.get_center())
                try:
                    measure_angle = Angle(line1, line2).get_value()
                    if (measure_angle >= PI*1.5 and angle > 0) or (measure_angle <= PI*0.5 and angle < 0):
                        angle = 0 if block else -angle

                except ValueError:
                    pass
            case "Rwrist":
                line1 = Line(self.right_wrist.get_center(), self.right_elbow_joint.get_center())
                line2 = Line(self.right_wrist.get_center(), self.right_hand.get_center())
                try:
                    measure_angle = Angle(line1, line2).get_value()
                    if (measure_angle >= PI*1.5 and angle > 0) or (measure_angle <= PI*0.5 and angle < 0):
                        angle = 0 if block else -angle

                except ValueError:
                    pass
            case "ankle":
                # angle = angle/
                pass
        mob.rotate(angle=angle, about_point=about_point)




