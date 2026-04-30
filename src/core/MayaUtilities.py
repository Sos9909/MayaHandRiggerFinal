import maya.cmds as mc
import maya.mel as ml
from maya.OpenMaya import MVector

def ConfigureCtrlForJnt(jnt, ctrlName, doConstraint=True):
    ctrlGrpName = ctrlName + "_grp"
    mc.group(ctrlName, n=ctrlGrpName)

    mc.matchTransform(ctrlGrpName, jnt)
    if doConstraint:
        mc.orientConstraint(ctrlName, jnt)

    mc.setAttr(f"{ctrlName}.scaleX", lock=True, k=False, cb=False)
    mc.setAttr(f"{ctrlName}.scaleY", lock=True, k=False, cb=False)
    mc.setAttr(f"{ctrlName}.scaleZ", lock=True, k=False, cb=False)

    return ctrlName, ctrlGrpName

def CreateCircleControllerForJnt(jnt, namePrefix, radius=2):
    ctrlName = f"ac_{namePrefix}_{jnt}"

    mc.circle(n=ctrlName, r=radius, nr=(1,0,0))
    
    mc.makeIdentity(ctrlName, apply=True)

    SetCurveLineWidth(ctrlName, 2)

    return ConfigureCtrlForJnt(jnt, ctrlName)

def SetCurveLineWidth(curve, newWidth):
    shapes = mc.listRelatives(curve, s=True) or []

    for shape in shapes:
        mc.setAttr(f"{shape}.lineWidth", newWidth)

