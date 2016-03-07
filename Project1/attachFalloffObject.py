#create a simple falloffObject
import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds
import pymel.core.general as pm

kPluginCmdName = "attachFalloffObject"

#Create flags for width and default value
kFalloffNameFlag = '-fn'
kFalloffNameLongFlag = '-falloffname'
defaultName = 'Falloff_Obj'


kFeatherGroupNameFlag = '-fgn'
kFeatherGroupNameLongFlag = '-feathergroupname'
defaultGroupName = 'FeatherGroup'

# Populate Command
class attachCommand(OpenMayaMPx.MPxCommand):
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)
    
    #parseArguments handles the input flags and sets self variables
    def parseArguments(self, args):
        argData = OpenMaya.MArgParser( self.syntax(), args )
        global defaultName
        self.falloffName= defaultName
        if argData.isFlagSet( kFalloffNameFlag ):
            flagValue = argData.flagArgumentString( kFalloffNameFlag, 0 )
            self.falloffName = flagValue
        global defaultGroupName
        self.feathergroupName = defaultGroupName
        if argData.isFlagSet( kFeatherGroupNameFlag ):
            flagValue = argData.flagArgumentString( kFeatherGroupNameFlag, 0)
            self.feathergroupName = flagValue
    # Invoked when the command is run.
    def doIt(self,args):
        self.parseArguments(args)
        cmds.cycleCheck(e=0)
        controllerShapeName = self.falloffName+'Shape'
        counter = 0
        theSet = ''
        feathers = cmds.listRelatives(self.feathergroupName)
        for featherCNTRL in feathers:
            initialScaleX = cmds.getAttr(featherCNTRL+'.scaleX')
            initialScaleY = cmds.getAttr(featherCNTRL+'.scaleY')
            initialScaleZ = cmds.getAttr(featherCNTRL+'.scaleZ')

            cmds.select(featherCNTRL)
            cmds.pickWalk(d='down')
            featherShape = cmds.ls(selection=True)[0]
            print featherShape
            #Distance between feathers and falloffobject
            distNode = cmds.createNode('distanceBetween', n='distance_'+self.falloffName+str(counter))
            cmds.connectAttr(controllerShapeName+'.worldPosition[0]', distNode+'.point1')
            cmds.connectAttr(featherShape+'_DistanceLoc.worldPosition[0]', distNode+'.point2')

            #Divide Distance/FalloffSize
            multDivNode = cmds.createNode('multiplyDivide', n='MultiDiv_distDiv_'+self.falloffName+str(counter))

            cmds.connectAttr(self.falloffName+'.Falloff_Size', multDivNode+'.input2X')
            cmds.setAttr(multDivNode+'.operation', 2)
            cmds.connectAttr(distNode+'.distance', multDivNode+'.input1X')

            #Clamp division to max 1 (Value now between 0 and 1)
            clampNode = cmds.createNode('clamp', n='clamp_'+self.falloffName+str(counter))
            cmds.setAttr(clampNode+'.maxR', 1)
            cmds.connectAttr(multDivNode+'.outputX', clampNode+'.inputR')

            #Scale it with 1-ClampOutput
            plusMinNode = cmds.createNode('plusMinusAverage', n='plusMinAv_'+self.falloffName+str(counter))
            cmds.setAttr(plusMinNode+'.operation', 2)
            cmds.setAttr(plusMinNode+'.input2D[0].input2Dx', 1)
            cmds.connectAttr(clampNode+'.outputR', plusMinNode+'.input2D[1].input2Dx')

            #Make scaling correct and stuffz
            remapPlusMinNode = cmds.createNode('plusMinusAverage', n='remapPlusMinAv_'+self.falloffName+str(counter))
            cmds.setAttr(remapPlusMinNode+'.operation', 2)
            cmds.connectAttr(self.falloffName+'.scaleX', remapPlusMinNode+'.input3D[0].input3Dx')
            cmds.connectAttr(self.falloffName+'.scaleY', remapPlusMinNode+'.input3D[0].input3Dy')
            cmds.connectAttr(self.falloffName+'.scaleZ', remapPlusMinNode+'.input3D[0].input3Dz')
            cmds.setAttr(remapPlusMinNode+'.input3D[1].input3Dx', 1)
            cmds.setAttr(remapPlusMinNode+'.input3D[1].input3Dy', 1)
            cmds.setAttr(remapPlusMinNode+'.input3D[1].input3Dz', 1)

            

            #Rotation and scaling stuff going strong
            multRotNode = cmds.createNode('multiplyDivide', n='MultiDiv_multRot_'+self.falloffName+str(counter))
            multScaleNode = cmds.createNode('multiplyDivide', n='MultiDiv_multScale_'+self.falloffName+str(counter))

            cmds.connectAttr(plusMinNode+'.output2Dx', multRotNode+'.input1X')
            cmds.connectAttr(plusMinNode+'.output2Dx', multScaleNode+'.input1X')

            multReverseNode = cmds.createNode('multiplyDivide', n='MultiDiv_multReverse_'+self.falloffName+str(counter))
            cmds.setAttr(multReverseNode+'.input2X', -1)

            cmds.connectAttr(multRotNode+'.outputX', multReverseNode+'.input1X')

            #Ranges, ranges, ranges...
            rotRangeNode = cmds.createNode('setRange', n='setRange_RotRange_'+self.falloffName+str(counter))
            scaleRangeNode = cmds.createNode('setRange', n='setRange_ScaleRange_'+self.falloffName+str(counter))

            cmds.setAttr(rotRangeNode+'.oldMinX', -360)
            cmds.setAttr(rotRangeNode+'.oldMaxX', 360)
            cmds.setAttr(rotRangeNode+'.oldMinY', -360)
            cmds.setAttr(rotRangeNode+'.oldMaxY', 360)
            cmds.setAttr(rotRangeNode+'.oldMinZ', -360)
            cmds.setAttr(rotRangeNode+'.oldMaxZ', 360)

            cmds.setAttr(scaleRangeNode+'.minX', 0)
            cmds.setAttr(scaleRangeNode+'.minY', 0)
            cmds.setAttr(scaleRangeNode+'.minZ', 0)

            cmds.setAttr(scaleRangeNode+'.oldMinX', 0)
            cmds.setAttr(scaleRangeNode+'.oldMinY', 0)
            cmds.setAttr(scaleRangeNode+'.oldMinZ', 0)

            cmds.setAttr(scaleRangeNode+'.oldMaxX', 25)
            cmds.setAttr(scaleRangeNode+'.oldMaxY', 25)
            cmds.setAttr(scaleRangeNode+'.oldMaxZ', 25)
            
            #Connect this..
            cmds.connectAttr(multReverseNode+'.outputX', rotRangeNode+'.minX')
            cmds.connectAttr(multReverseNode+'.outputX', rotRangeNode+'.minY')
            cmds.connectAttr(multReverseNode+'.outputX', rotRangeNode+'.minZ')

            cmds.connectAttr(multRotNode+'.outputX', rotRangeNode+'.maxX')
            cmds.connectAttr(multRotNode+'.outputX', rotRangeNode+'.maxY')
            cmds.connectAttr(multRotNode+'.outputX', rotRangeNode+'.maxZ')

            cmds.connectAttr(multScaleNode+'.outputX', scaleRangeNode+'.maxX')
            cmds.connectAttr(multScaleNode+'.outputX', scaleRangeNode+'.maxY')
            cmds.connectAttr(multScaleNode+'.outputX', scaleRangeNode+'.maxZ')

            cmds.connectAttr(rotRangeNode+'.oldMaxX', multRotNode+'.input2X')
            cmds.connectAttr(scaleRangeNode+'.oldMaxX', multScaleNode+'.input2X')
            
            cmds.connectAttr(self.falloffName+'.rotateX', rotRangeNode+'.valueX')
            cmds.connectAttr(self.falloffName+'.rotateY', rotRangeNode+'.valueY')
            cmds.connectAttr(self.falloffName+'.rotateZ', rotRangeNode+'.valueZ')

            #Connect to feather shape
            cmds.connectAttr(rotRangeNode+'.outValueX', featherCNTRL+'.rotateX')
            cmds.connectAttr(rotRangeNode+'.outValueY', featherCNTRL+'.rotateY')
            cmds.connectAttr(rotRangeNode+'.outValueZ', featherCNTRL+'.rotateZ')

            endPlusMinNode = cmds.createNode('plusMinusAverage', n='endPlusMinAv_'+self.falloffName+str(counter))
            
            cmds.setAttr(endPlusMinNode+'.operation', 1)
            cmds.setAttr(endPlusMinNode+'.input3D[0].input3Dx', initialScaleX)
            cmds.setAttr(endPlusMinNode+'.input3D[0].input3Dy', initialScaleY)
            cmds.setAttr(endPlusMinNode+'.input3D[0].input3Dz', initialScaleZ)
            cmds.connectAttr(remapPlusMinNode+'.output3Dx', scaleRangeNode+'.valueX')
            cmds.connectAttr(remapPlusMinNode+'.output3Dy', scaleRangeNode+'.valueY')
            cmds.connectAttr(remapPlusMinNode+'.output3Dz', scaleRangeNode+'.valueZ')

            cmds.connectAttr(scaleRangeNode+'.outValueX', endPlusMinNode+'.input3D[1].input3Dx')
            cmds.connectAttr(scaleRangeNode+'.outValueY', endPlusMinNode+'.input3D[1].input3Dy')
            cmds.connectAttr(scaleRangeNode+'.outValueZ', endPlusMinNode+'.input3D[1].input3Dz')

            cmds.connectAttr(endPlusMinNode+'.output3Dx', featherCNTRL+'.scaleX')
            cmds.connectAttr(endPlusMinNode+'.output3Dy', featherCNTRL+'.scaleY')
            cmds.connectAttr(endPlusMinNode+'.output3Dz', featherCNTRL+'.scaleZ')

            
            cmds.select(distNode, r=True)
            cmds.select(multDivNode, add=True)
            cmds.select(clampNode, add=True)
            cmds.select(plusMinNode, add=True)
            cmds.select(multRotNode, add=True)
            cmds.select(multScaleNode, add=True)
            cmds.select(multReverseNode, add=True)
            cmds.select(rotRangeNode, add=True)
            cmds.select(scaleRangeNode, add=True)
            cmds.select(remapPlusMinNode, add=True)
            cmds.select(endPlusMinNode, add=True)
            if cmds.objExists(self.falloffName+'_UtilContainer'):
                cmds.container(self.falloffName+'_UtilContainer', edit=True, includeShapes=True, includeTransform=True, force=True, addNode=cmds.ls(sl=True))
            else:
                cmds.container(n=self.falloffName+'_UtilContainer', includeShapes=True, includeTransform=True, force=True, addNode=cmds.ls(sl=True))

            if cmds.objExists(self.falloffName+'_FeatherfalloffSet'):
                cmds.select(featherCNTRL, r=True)
                cmds.sets(cmds.ls(sl=True), add=theSet)
            else:
                cmds.select(featherCNTRL, r=True)
                theSet = cmds.sets(n=self.falloffName+'_FeatherfalloffSet')
            counter = counter+1




def attachCreator():
    return OpenMayaMPx.asMPxPtr( attachCommand() )

def syntaxCreator():
    syntax = OpenMaya.MSyntax()
    syntax.addFlag( kFalloffNameFlag, kFalloffNameLongFlag, OpenMaya.MSyntax.kString )
    syntax.addFlag( kFeatherGroupNameFlag, kFeatherGroupNameLongFlag, OpenMaya.MSyntax.kString )
    return syntax

# Initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerCommand( kPluginCmdName, attachCreator, syntaxCreator )
    except:
        sys.stderr.write( "Failed to register command: %s\n" % kPluginCmdName )
        raise

# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand( kPluginCmdName )
    except:
        sys.stderr.write( "Failed to unregister command: %s\n" % kPluginCmdName )
