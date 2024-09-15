import random as rd
from manim import *
import sys
import os

# 添加上一级目录到 sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from animation.Robot import Robot


class Tutting(Robot):
    def kingtut(self):
        
        left_wrist_tracker = ValueTracker(90/self.fps*rd.choice([-1, 1, 0]))
        right_wrist_tracker = ValueTracker(90/self.fps*rd.choice([-1, 1, 0]))
        left_elbow_tracker = ValueTracker(90/self.fps*rd.choice([-1, 1, 0]))
        right_elbow_tracker = ValueTracker(90/self.fps*rd.choice([-1, 1, 0]))
        left_shoulder_tracker = ValueTracker(90/self.fps*rd.choice([-1, 1, 0]))
        right_shoulder_tracker = ValueTracker(90/self.fps*rd.choice([-1, 1, 0]))
        

        # y, sr = librosa.load(r"D:\图片\bensound-autoreverse.mp3", duration=22)
        # sf.write(r"D:\图片\bensound-autoreverse.wav", y, sr)
        
        self.play(FadeIn(self.Dancer))

        time_tracker = ValueTracker(0)
        time_tracker.add_updater(lambda x, dt: x.increment_value(1)).suspend_updating()
        self.add(time_tracker)
        def ctrl_direct(mob):
            mob.set_value(90/self.fps*rd.choice([1, -1, 0])) if time_tracker.get_value() % self.fps == 0 else mob.set_value(mob.get_value())

        self.add(
            left_wrist_tracker, left_elbow_tracker, right_wrist_tracker, 
            right_elbow_tracker, left_shoulder_tracker, right_shoulder_tracker, 
            self.Dancer, self.left_leg, self.right_leg, self.left_lowerleg, self.right_lowerleg, 
            self.left_elbow, self.right_elbow, self.left_arm, self.right_arm, 
            )
        

        self.left_arm.add_updater(lambda x: self.roration_restriction(x, angle=left_shoulder_tracker.get_value()*DEGREES, 
                                                     about_point=self.left_shoulder_joint.get_center(), joint_type=self.joint_type[1]))
        self.right_arm.add_updater(lambda x: self.roration_restriction(x, angle=right_shoulder_tracker.get_value()*DEGREES, 
                                                      about_point=self.right_shoulder_joint.get_center(), joint_type=self.joint_type[2]))
        self.left_elbow.add_updater(lambda x: self.roration_restriction(x, angle=left_elbow_tracker.get_value()*DEGREES, 
                                                   about_point=self.left_elbow_joint.get_center(), joint_type=self.joint_type[3]))
        self.right_elbow.add_updater(lambda x: self.roration_restriction(x, angle=right_elbow_tracker.get_value()*DEGREES, 
                                                about_point=self.right_elbow_joint.get_center(), joint_type=self.joint_type[4]))
        self.left_hand.add_updater(lambda x: self.roration_restriction(x, angle=left_wrist_tracker.get_value()*DEGREES, 
                                                      about_point=self.left_wrist.get_center(), joint_type=self.joint_type[5]))
        self.right_hand.add_updater(lambda x: self.roration_restriction(x, angle=right_wrist_tracker.get_value()*DEGREES, 
                                                       about_point=self.right_wrist.get_center(), joint_type=self.joint_type[6]))
        

        time_tracker.resume_updating()
        left_shoulder_tracker.add_updater(lambda x: ctrl_direct(x))
        right_shoulder_tracker.add_updater(lambda x: ctrl_direct(x))
        left_elbow_tracker.add_updater(lambda x: ctrl_direct(x))
        right_elbow_tracker.add_updater(lambda x: ctrl_direct(x))
        left_wrist_tracker.add_updater(lambda x: ctrl_direct(x))
        right_wrist_tracker.add_updater(lambda x: ctrl_direct(x))

        self.thigh_angle_tracker.add_updater(lambda x: x.set_value(self.angle_tracker.get_value()/self.leg_run_time/self.fps))
        # print(angle1/PI*180, angle2/PI*180)

        for _ in range(self.movement):
            choice = rd.choice([i for i in range(1, 9)])
            angle = self.leg_motion(choice)
            self.Dancer.add_updater(self.body_y_move(flag=2))

            self.angle_tracker.set_value(angle)
            self.wait(self.leg_run_time)
            self.Dancer.add_updater(self.body_y_move(flag=1))
            self.angle_tracker.set_value(-angle)
            match choice:
                case 7:
                    self.left_leg.clear_updaters()
                    self.left_leg.add_updater(lambda x: x.become(x.copy()).rotate(angle=-self.angle1/PI*180/self.fps/self.leg_run_time*DEGREES, about_point=self.left_thigh_joint.get_center()))
                case 8:
                    self.right_leg.clear_updaters()
                    self.right_leg.add_updater(lambda x: x.become(x.copy()).rotate(angle=-self.angle2/PI*180/self.fps/self.leg_run_time*DEGREES, about_point=self.right_thigh_joint.get_center()))
                case _:
                    pass
            self.wait(self.leg_run_time)

            self.Dancer.clear_updaters()
            self.left_leg.clear_updaters()
            self.right_leg.clear_updaters()
            self.left_lowerleg.clear_updaters()
            self.right_lowerleg.clear_updaters()
        self.play(FadeOut(self.Dancer))

    def construct(self):
        self.init_configuration()
        self.construct_dancer()
        self.kingtut()