import random as rd
import numpy as np
import librosa
from manim import *
import sys
import os

# 添加上一级目录到 sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from animation.Robot import Robot

class Popping(Robot):
    def popping(self, movement=5):
        self.play(FadeIn(self.Dancer))
        self.play(FadeOut(self.Dancer))