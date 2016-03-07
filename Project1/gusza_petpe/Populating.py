#populate feathers on object

#guszaas saett att ladda
#unloadPlugin("Populating.py")
#loadPlugin("Users/gzaphf/Sites/Maya-Featherizer/Project1/gusza_petpe/Populating.py")
#MakeFeather()

import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds
import pymel.core as pm
#import featherizer_utility as fu
kPluginCmdName = "makeFeather"

#Create flags for width and default value
kWidthFlag = '-w'
kWidthLongFlag = '-width'
defaultWidth = 5.0

#Create bool flag for duplicating selected object
kIsSelectedItemFlag = '-sel'
kIsSelectedItemLongFlag = '-isselected'
defaultisSelected = False

# Populate Command
class populateCommand(OpenMayaMPx.MPxCommand):
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)
    
    #parseArguments handles the input flags and sets self variables
    def parseArguments(self, args):
        argData = OpenMaya.MArgParser( self.syntax(), args )
        global defaultWidth
        self.width = defaultWidth

        if argData.isFlagSet( kWidthFlag ):
            # In this case, we print the passed flag's value as an integer.
            # We use the '0' to index the flag's first and only parameter.
            flagValue = argData.flagArgumentDouble( kWidthFlag, 0 )
            self.width = flagValue
        global defaultisSelected
        self.isSelected = defaultisSelected
        if argData.isFlagSet( kIsSelectedItemFlag ):
            flagValue = argData.flagArgumentBool( kIsSelectedItemFlag, 0 )
            self.isSelected = flagValue

    # VART SKA VI LaGGA DENNA!!!!!!!!!!!
    def my_range(self, start, end, step):
        while start <= end:
            yield start
            start += step


    # Invoked when the command is run.
    def doIt(self,args):
        #Default values of the feather
        rad = 5.0
        hei = 1.0




        self.parseArguments(args)
        if self.isSelected:
            featherProto = cmds.ls(selection=True)
        else:
            featherProto = cmds.polyPlane(w=self.width, h=hei)[0]

        # main = cmds.polySphere(name = 'main', r=rad)
        # cmds.move(10, 0, 0)

        # #feather2 = cmds.ls( selection=True )
        # #feather1 = cmds.duplicate(feather2)

        # verts = pm.MeshVertex('main.vtx[*]')
        sphere1 = cmds.sphere(name='sphere1', r = 10)[0]

        shp = cmds.listRelatives(sphere1, s=True)[0]
        maxU = cmds.getAttr(shp+'.maxValueU')
        maxV = cmds.getAttr(shp+'.maxValueV')
        minU = cmds.getAttr(shp+'.minValueU')
        minV = cmds.getAttr(shp+'.minValueV')

        cmds.move(10, 0, 0)
        fGrp = cmds.group(n='FeatherGroup', em=True)
        folGrp = cmds.group(n='FollicleGroup', em=True)
        #Loop through the UVs
        for fin_U in self.my_range(minU, 1.0, 0.1):
            for fin_V in self.my_range(minU, 1.0, 0.1):
                CTRLgroup = cmds.group(n='CNTRL_GRP', em=True)
                cmds.select(cl = True)
                cmds.select(featherProto)
                feather = cmds.duplicate(featherProto, n='myPlane')[0]
                cmds.select(cl = True)
                cmds.select(feather)
                if self.isSelected is False:
                    cmds.move(self.width/2.0, 0, 0, ws=True)
                cmds.move(0, 0, 0, feather+".scalePivot",feather+".rotatePivot", absolute=True)
                cmds.rotate(0, -90, 90 )
                cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
                locator = cmds.spaceLocator(n=feather+'_DistanceLoc')
                cmds.parent(locator, feather)
                cmds.setAttr(locator[0]+'.visibility', 0)
                cmds.parent(feather, CTRLgroup)
                #Create follicle and name it
                cmds.createNode('follicle')
                cmds.pickWalk(d='up')
                cmds.rename(cmds.ls(sl=True), sphere1+'_'+feather+'_Follicle')
                cmds.pickWalk(d='down')
                thisFollicle = cmds.ls(sl=True)

                cmds.select(thisFollicle, r=True)
                cmds.pickWalk(d='up')
                thisFollicleTransform = cmds.ls(sl=True)
                #Set follicle UV position
                cmds.setAttr(thisFollicle[0]+'.parameterU', fin_U)
                cmds.setAttr(thisFollicle[0]+'.parameterV', fin_V)
                #Attach follicle to the object
                cmds.connectAttr(sphere1+'.local', thisFollicle[0]+'.inputSurface', f=True)
                cmds.connectAttr(sphere1+'.worldMatrix[0]', thisFollicle[0]+'.inputWorldMatrix', f=True)
                #Attach follicle to itself
                cmds.connectAttr(thisFollicle[0]+'.outTranslate', thisFollicleTransform[0]+'.translate', f=True)
                cmds.connectAttr(thisFollicle[0]+'.outRotate', thisFollicleTransform[0]+'.rotate', f=True)
                #Attach feather object to follicle
                #cmds.connectAttr(thisFollicleTransform[0]+'.translate', feather+'.translate', f=True)
                cmds.connectAttr(thisFollicleTransform[0]+'.translate', CTRLgroup+'.translate', f=True)
                cmds.connectAttr(thisFollicleTransform[0]+'.rotate', feather+'.rotate', f=True)
                #Hide follicle
                cmds.setAttr(thisFollicleTransform[0]+'.visibility', 0)


                #some parenting
                cmds.parent(CTRLgroup, fGrp)
                cmds.parent(thisFollicleTransform, folGrp)

        cmds.select(cl = True)


def populateCreator():
    return OpenMayaMPx.asMPxPtr( populateCommand() )

def syntaxCreator():
    syntax = OpenMaya.MSyntax()
    syntax.addFlag( kWidthFlag, kWidthLongFlag, OpenMaya.MSyntax.kDouble )
    syntax.addFlag( kIsSelectedItemFlag, kIsSelectedItemLongFlag, OpenMaya.MSyntax.kBoolean )

    return syntax




# Initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerCommand( kPluginCmdName, populateCreator, syntaxCreator )
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


