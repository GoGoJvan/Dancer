import random as rd
import numpy as np
import librosa
from manim import *
import sys
import os

# 添加上一级目录到 sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from animation.Robot import Robot


class Tutting(Robot):
    def kingtut(self, movement=5, fps=config.frame_rate, music_path=r"D:\图片\bensound-autoreverse.wav"):
        
        left_wrist_tracker = ValueTracker(90/fps*rd.choice([-1, 1, 0]))
        right_wrist_tracker = ValueTracker(90/fps*rd.choice([-1, 1, 0]))
        left_elbow_tracker = ValueTracker(90/fps*rd.choice([-1, 1, 0]))
        right_elbow_tracker = ValueTracker(90/fps*rd.choice([-1, 1, 0]))
        left_shoulder_tracker = ValueTracker(90/fps*rd.choice([-1, 1, 0]))
        right_shoulder_tracker = ValueTracker(90/fps*rd.choice([-1, 1, 0]))
        
        joint_type = {
            1: "Lshoulder",
            2: "Rshoulder",
            3: "Lelbow",
            4: "Relbow",
            5: "Lwrist",
            6: "Rwrist",
        }
        # y, sr = librosa.load(r"D:\图片\bensound-autoreverse.mp3", duration=22)
        # sf.write(r"D:\图片\bensound-autoreverse.wav", y, sr)
        self.add_sound(music_path)
        self.play(FadeIn(self.Dancer))

        time_tracker = ValueTracker(0)
        time_tracker.add_updater(lambda x, dt: x.increment_value(1)).suspend_updating()
        self.add(time_tracker)
        def ctrl_direct(mob):
            mob.set_value(90/fps*rd.choice([1, -1, 0])) if time_tracker.get_value() % fps == 0 else mob.set_value(mob.get_value())
        thigh_angle_tracker = ValueTracker(0)
        angle_tracker = ValueTracker(0)

        self.add(
            thigh_angle_tracker, left_wrist_tracker, left_elbow_tracker, right_wrist_tracker, 
            right_elbow_tracker, left_shoulder_tracker, right_shoulder_tracker, self.Dancer, 
            self.left_leg, self.right_leg, self.left_lowerleg, self.right_lowerleg, 
            self.left_elbow, self.right_elbow, self.left_arm, self.right_arm
            )
        
        self.add(angle_tracker)
        y , sr = librosa.load(music_path,sr=None)
        # 计算节拍包络
        onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=512, aggregate=np.median)
        # 跟踪节拍
        tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
        leg_run_time = int(tempo[0]/60)

        self.left_arm.add_updater(lambda x: self.roration_restriction(x, angle=left_shoulder_tracker.get_value()*DEGREES, 
                                                     about_point=self.left_shoulder_joint.get_center(), joint_type=joint_type[1]))
        self.right_arm.add_updater(lambda x: self.roration_restriction(x, angle=right_shoulder_tracker.get_value()*DEGREES, 
                                                      about_point=self.right_shoulder_joint.get_center(), joint_type=joint_type[2]))
        self.left_elbow.add_updater(lambda x: self.roration_restriction(x, angle=left_elbow_tracker.get_value()*DEGREES, 
                                                   about_point=self.left_elbow_joint.get_center(), joint_type=joint_type[3]))
        self.right_elbow.add_updater(lambda x: self.roration_restriction(x, angle=right_elbow_tracker.get_value()*DEGREES, 
                                                about_point=self.right_elbow_joint.get_center(), joint_type=joint_type[4]))
        self.left_hand.add_updater(lambda x: self.roration_restriction(x, angle=left_wrist_tracker.get_value()*DEGREES, 
                                                      about_point=self.left_wrist.get_center(), joint_type=joint_type[5]))
        self.right_hand.add_updater(lambda x: self.roration_restriction(x, angle=right_wrist_tracker.get_value()*DEGREES, 
                                                       about_point=self.right_wrist.get_center(), joint_type=joint_type[6]))
        time_tracker.resume_updating()
        left_shoulder_tracker.add_updater(lambda x: ctrl_direct(x))
        right_shoulder_tracker.add_updater(lambda x: ctrl_direct(x))
        left_elbow_tracker.add_updater(lambda x: ctrl_direct(x))
        right_elbow_tracker.add_updater(lambda x: ctrl_direct(x))
        left_wrist_tracker.add_updater(lambda x: ctrl_direct(x))
        right_wrist_tracker.add_updater(lambda x: ctrl_direct(x))

        thigh_angle_tracker.add_updater(lambda x: x.set_value(angle_tracker.get_value()/leg_run_time/fps))

        def body_y_move(flag):
            match flag:
                case 1:
                    def update_y(x:Mobject):
                        return x.become(x.copy()).shift([0, 2*Line(self.left_thigh_joint.get_center(),
                    self.left_knee_joint.get_center()).get_length()*(1-np.cos(angle_tracker.get_value()/180*PI))/leg_run_time/fps, 0])
                    return update_y
                case 2:
                    def update_y(x:Mobject):
                        return x.become(x.copy()).shift([0, -Line(self.left_thigh_joint.get_center(),
                    self.left_knee_joint.get_center()).get_length()*(1-np.cos(angle_tracker.get_value()/180*PI))/leg_run_time/fps, 0])
                    return update_y

        def body_x_move(flag):
            match flag:
                case 1:
                    def update_x(x:Mobject):
                        return x.become(x.copy()).shift([Line(self.left_thigh_joint.get_center(),
                                    self.left_knee_joint.get_center()).get_length()*(np.sin(angle_tracker.get_value()/180*PI))/leg_run_time/fps, 0, 0])
                    return update_x
                case 2:
                    def update_x(x:Mobject):
                        return x.become(x.copy()).shift([-Line(self.left_thigh_joint.get_center(),
                                        self.left_knee_joint.get_center()).get_length()*(np.sin(angle_tracker.get_value()/180*PI))/leg_run_time/fps, 0, 0])
                    return update_x

        def four_rotation(flag, direction):
            match flag:
                case 1:
                    def rotate_left_leg(x:Mobject):
                        return x.become(x.copy()).rotate(angle=direction*thigh_angle_tracker.get_value()*DEGREES, about_point=self.left_thigh_joint.get_center())
                    return rotate_left_leg
                case 2:
                    def rotate_right_leg(x:Mobject):
                        return x.become(x.copy()).rotate(angle=direction*thigh_angle_tracker.get_value()*DEGREES, about_point=self.right_thigh_joint.get_center())
                    return rotate_right_leg
                case 3:
                    def rotate_left_lowerleg(x:Mobject):
                        return x.become(x.copy()).rotate(angle=direction*thigh_angle_tracker.get_value()*DEGREES, about_point=self.left_knee_joint.get_center())
                    return rotate_left_lowerleg
                case 4:
                    def rotate_right_lowerleg(x:Mobject):
                        return x.become(x.copy()).rotate(angle=direction*thigh_angle_tracker.get_value()*DEGREES, about_point=self.right_knee_joint.get_center())
                    return rotate_right_lowerleg
        angle1 = -np.arccos(
                            Line(self.right_knee_joint.get_center(), self.right_foot.get_center()).get_length()/
                            Line(self.left_thigh_joint.get_center(), self.left_foot.get_center()).get_length()
                            )
        angle2 = np.arccos(
                           Line(self.right_knee_joint.get_center(), self.right_foot.get_center()).get_length()/
                           Line(self.right_thigh_joint.get_center(), self.right_foot.get_center()).get_length()
                           )
        # print(angle1/PI*180, angle2/PI*180)
        
        for _ in range(movement):
            choice = rd.choice([i for i in range(1, 9)])
            match choice:
                case 1 | 2 | 3:
                    match choice:
                        case 1:
                            angle = 60
                        case 2:
                            angle = 45
                        case 3:
                            angle = -10
                        case 4:
                            angle = 90
                    self.left_leg.add_updater(four_rotation(flag=1, direction=-1))
                    self.right_leg.add_updater(four_rotation(flag=2, direction=1))
                    self.left_lowerleg.add_updater(four_rotation(flag=3, direction=1))
                    self.right_lowerleg.add_updater(four_rotation(flag=4, direction=-1))

                case 4:
                    angle = 90
                    self.Dancer.add_updater(body_x_move(flag=1))
                    self.right_leg.add_updater(four_rotation(flag=2, direction=1))
                    self.left_lowerleg.add_updater(four_rotation(flag=3, direction=-1))
                    self.right_lowerleg.add_updater(four_rotation(flag=4, direction=-1))
                case 5:
                    angle = 90
                    self.Dancer.add_updater(body_x_move(flag=2))
                    self.left_leg.add_updater(four_rotation(flag=1, direction=-1))
                    self.left_lowerleg.add_updater(four_rotation(flag=3, direction=1))
                    self.right_lowerleg.add_updater(four_rotation(flag=4, direction=1))
                case 6:
                    angle = 90
                    self.left_lowerleg.add_updater(four_rotation(flag=3, direction=-1))
                    self.right_lowerleg.add_updater(four_rotation(flag=4, direction=1))
                    
                case 7:
                    angle = 90
                    self.Dancer.add_updater(body_x_move(flag=1))
                    self.right_leg.add_updater(four_rotation(flag=2, direction=1))
                    self.right_lowerleg.add_updater(four_rotation(flag=4, direction=-1))
                    self.left_leg.add_updater(lambda x: x.become(x.copy()).rotate(angle=angle1/PI*180/fps/leg_run_time*DEGREES, 
                                                                                  about_point=self.left_thigh_joint.get_center()))
                case 8:
                    angle = 90
                    self.Dancer.add_updater(body_x_move(flag=2))
                    self.left_leg.add_updater(four_rotation(flag=1, direction=-1))
                    self.left_lowerleg.add_updater(four_rotation(flag=3, direction=1))
                    self.right_leg.add_updater(lambda x: x.become(x.copy()).rotate(angle=angle2/PI*180/fps/leg_run_time*DEGREES, 
                                                                                   about_point=self.right_thigh_joint.get_center()))

            self.Dancer.add_updater(body_y_move(flag=2))

            angle_tracker.set_value(angle)
            self.wait(leg_run_time)
            self.Dancer.add_updater(body_y_move(flag=1))
            angle_tracker.set_value(-angle)
            match choice:
                case 7:
                    self.left_leg.clear_updaters()
                    self.left_leg.add_updater(lambda x: x.become(x.copy()).rotate(angle=-angle1/PI*180/fps/leg_run_time*DEGREES, about_point=self.left_thigh_joint.get_center()))
                case 8:
                    self.right_leg.clear_updaters()
                    self.right_leg.add_updater(lambda x: x.become(x.copy()).rotate(angle=-angle2/PI*180/fps/leg_run_time*DEGREES, about_point=self.right_thigh_joint.get_center()))
                case _:
                    pass
            self.wait(leg_run_time)

            self.Dancer.clear_updaters()
            self.left_leg.clear_updaters()
            self.right_leg.clear_updaters()
            self.left_lowerleg.clear_updaters()
            self.right_lowerleg.clear_updaters()
        self.play(FadeOut(self.Dancer))

    def construct(self):
        self.config_window()
        self.construct_dancer()
        self.kingtut()