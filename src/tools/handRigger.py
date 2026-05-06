from core.MayaWidget import MayaWidget 
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel
import maya.cmds as mc
from maya.OpenMaya import MVector
from PySide6.QtWidgets import QColorDialog

import importlib
import core.MayaUtilities
importlib.reload(core.MayaUtilities)
from core.MayaUtilities import (CreateCircleControllerForJnt,
                                ConfigureCtrlForJnt,
                                )

class HandRigger:
    def __init__(self):
        self.nameBase = " "
        self.controllerSize = 2
        self.blendControllerSize = 4
        self.controlColorRGB = [0,0,0]

    def SetNameBase(self, newNameBase):
        self.nameBase = newNameBase
        print(f"name base is set to: {self.nameBase}")

    def RigFinger(self, fingerJoints, fingerName):
        prevCtrl = None
        firstCtrlGrp = None

        for i, jnt in enumerate(fingerJoints):
            ctrlName = f"{fingerName}_{i}"

            ctrl, ctrlGrp = CreateCircleControllerForJnt(
                jnt,
                ctrlName,
                self.controllerSize
            )


            if i == 0:
                firstCtrlGrp = ctrlGrp

            if prevCtrl:
                mc.parent(ctrlGrp, prevCtrl)
            
            prevCtrl = ctrl


        return firstCtrlGrp
    
    def RigHand(self):
        print("Start Hand Rigging!!!")

        selection = mc.ls(sl=True)

        if not selection:
            mc.error("Select the wrist joint")
            return
        
        wristJnt = selection[0]

        fingers = [
        jnt for jnt in mc.listRelatives(wristJnt, ad=True, type="joint") or []
        if jnt.endswith("_01")
        ]

        if not fingers:
            mc.error("No finger joints found under wrist")
            return
        
        topGrpName = f"{self.nameBase}_handRig_grp"
        mc.group(n=topGrpName, empty=True)

        for finger in fingers:
            fingerChain = mc.listRelatives(finger, ad=True, type="joint") or []
            fingerChain.append(finger)
            fingerChain.reverse()

            fingerGrp = self.RigFinger(fingerChain, finger)

            if fingerGrp:
                mc.parent(fingerGrp, topGrpName)

        shapes = mc.listRelatives(topGrpName, allDescendents=True, type="shape") or []

        for shape in shapes:
            mc.setAttr(f"{shape}.overrideEnabled", 1)
            mc.setAttr(f"{shape}.overrideRGBColors", 1)
            mc.setAttr(
                f"{shape}.overrideColorRGB",
                self.controlColorRGB[0],
                self.controlColorRGB[1],
                self.controlColorRGB[2]
            )

        print("Hand rig Complete!!!!")

class HandRiggerWidget(MayaWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hand Rigger")

        self.rigger = HandRigger()

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Select wrist joint"))

        #name input
        row = QHBoxLayout()
        layout.addLayout(row)

        self.nameInput = QLineEdit()
        row.addWidget(self.nameInput)

        btn = QPushButton("Set Name")
        btn.clicked.connect(self.SetName)
        row.addWidget(btn)

        #color picker button
        colorBtn = QPushButton("Pick Color")
        colorBtn.clicked.connect(self.PickColor)
        layout.addWidget(colorBtn)

        #rig button
        rigBtn = QPushButton("Rig Hand")
        rigBtn.clicked.connect(self.RigHand)
        layout.addWidget(rigBtn)

    def SetName(self):
        self.rigger.SetNameBase(self.nameInput.text())

    def PickColor(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.rigger.controlColorRGB = [
                color.redF(),
                color.greenF(),
                color.blueF()
            ]

    def RigHand(self):
        self.rigger.RigHand()

    def GetWidgetHash(self):
        return "hand_rigger_widget_unique_hash"



def Run():
    widget = HandRiggerWidget()
    widget.show()   

