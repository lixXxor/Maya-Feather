#create a simple falloffObject
import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds
import pymel.core.general as pm

kPluginCmdName = "createFalloffObject"

#Create flags for width and default value
kSizeFlag = '-s'
kSizeLongFlag = '-size'
defaultSize = 5.0


# Populate Command
class falloffCommand(OpenMayaMPx.MPxCommand):
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)

    #parseArguments handles the input flags and sets self variables
    def parseArguments(self, args):
        argData = OpenMaya.MArgParser( self.syntax(), args )
        global defaultSize
        self.size = defaultSize
        if argData.isFlagSet( kSizeFlag ):
            flagValue = argData.flagArgumentDouble( kSizeFlag, 0 )
            self.size = flagValue

    # Invoked when the command is run.
    def doIt(self,args):
        self.parseArguments(args)
        circle1 = cmds.circle(r=self.size)
        circle2 = cmds.circle(r=self.size)
        cmds.rotate(0,'90deg',0,circle2[0])
        locator = cmds.spaceLocator(n='Falloff_Obj')[0];
        #Kanske connecta Falloff_size med radien pa cirklarna
        cmds.addAttr(locator, at='double', k=True, dv=self.size,ln='Falloff_Size' )
        locGroup = cmds.group(circle1, circle2, n='circleGroup')
        cmds.setAttr(locator+'.visibility', 0)
        movingLocator = cmds.spaceLocator(n='Move_This_Obj')[0]
        cmds.connectAttr(movingLocator+'.translate', locator+'.translate')
        cmds.connectAttr(movingLocator+'.rotate', locator+'.rotate')
        cmds.connectAttr(movingLocator+'.scale', locator+'.scale')
        cmds.parent(locGroup, movingLocator)

        #test = OpenMaya.
        #main = cmds.select( all = True )
def falloffCreator():
    return OpenMayaMPx.asMPxPtr( falloffCommand() )

def syntaxCreator():
    syntax = OpenMaya.MSyntax()
    syntax.addFlag( kSizeFlag, kSizeLongFlag, OpenMaya.MSyntax.kDouble )

    return syntax

# Initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerCommand( kPluginCmdName, falloffCreator, syntaxCreator )
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
