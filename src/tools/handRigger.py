from core.MayaWidget import MayaWidget 
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QPushButton, QLabel
import maya.cmds as mc
from maya.OpenMaya import MVector
from PySide6.QtWidgets import QColorDialog

import importlib
import core.MayaUtilities
importlib.reload(core.MayaUtilities)
from core.MayaUtilities import (CreateCircleControllerForJnt,
                                CreateBoxControllerForJnt, 
                                CreatePlusController, 
                                ConfigureCtrlForJnt,
                                GetObjectPositionAsMVec
                                )

class HandRigger:
    def __init__(self):
        self.nameBase = " "
        self.controllerSize = 10
        self.blendControllerSize = 4
        self.controlColorRGB = [0,0,0]

    def SetNameBase(self, newNameBase):
        self.nameBase = newNameBase
        print(f"name base is set to: {self.nameBase}")

    def SetControllerSize(self, newControllerSize):
        self.controllerSize = newControllerSize

    def SetBlendControllerSize(self, newBlendControllerSize):
        self.blendControllerSize = newBlendControllerSize

    def RigLimb(self):
        print("Start Rigging!!!")
