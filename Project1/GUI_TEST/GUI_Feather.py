#populate feathers on object
#guszaas saett att ladda
#unloadPlugin("Populating.py")
#loadPlugin("Users/gzaphf/Sites/Maya-Featherizer/Project1/gusza_petpe/Populating.py")
#MakeFeather()

# import os
import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds
import maya.mel as maymel
import pymel.core.general as pm
from pymel.core import *
import random
# sys.path.append("..")
# from hejsven import testfunctionen
import hejsven as hejs

#import featherizer_utility as fu
kPluginCmdName = "makeFeather"

#Create flags for width and default value
kWidthFlag = '-w'
kWidthLongFlag = '-width'
defaultWidth = 5.0
defaultSize = 5.0

#Create bool flag for duplicating selected object
kIsSelectedItemFlag = '-sel'
kIsSelectedItemLongFlag = '-isselected'
defaultisSelected = False

kIsSelectedItemLongFlag = '-isselectedFeather'
defaultisSelected = False



# Populate Command
class populateCommand(OpenMayaMPx.MPxCommand):
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)


    def createFalloffObject(self):
        circle1 = cmds.circle(r=self.size)
        circle2 = cmds.circle(r=self.size)
        cmds.rotate(0,'90deg',0,circle2[0])
        self.falloffName = cmds.spaceLocator(n='Falloff_Obj')[0];
        #Kanske connecta Falloff_size med radien pa cirklarna
        cmds.addAttr(self.falloffName, at='double', k=True, dv=self.size,ln='Falloff_Size' )
        locGroup = cmds.group(circle1, circle2, n='circleGroup')
        cmds.setAttr(self.falloffName+'.visibility', 0)
        movingLocator = cmds.spaceLocator(n='Move_This_Obj')[0]
        cmds.addAttr(movingLocator, at='double', k=True, dv=self.size,ln='Falloff_Size' )
        cmds.connectAttr(movingLocator+'.Falloff_Size',self.falloffName+'.Falloff_Size')
        cmds.connectAttr(movingLocator+'.translate', self.falloffName+'.translate')
        cmds.connectAttr(movingLocator+'.rotate', self.falloffName+'.rotate')
        cmds.connectAttr(movingLocator+'.scale', self.falloffName+'.scale')
        cmds.parent(locGroup, movingLocator)

        # attachFalloffObject
        cmds.cycleCheck(e=0)
        controllerShapeName = self.falloffName+'Shape'
        counter = 0
        theSet = ''
        feathers = cmds.listRelatives(self.feathergroupName)
        for ScaleGroup in feathers:
            select(ScaleGroup)
            CTRLgroup = pickWalk(d='down')[0]
            initialScaleX = cmds.getAttr(CTRLgroup+'.scaleX')
            initialScaleY = cmds.getAttr(CTRLgroup+'.scaleY')
            initialScaleZ = cmds.getAttr(CTRLgroup+'.scaleZ')


            pickWalk(d='down')
            featherShape = cmds.ls(selection=True)[0]
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
            cmds.connectAttr(rotRangeNode+'.outValueX', CTRLgroup+'.rotateX')
            cmds.connectAttr(rotRangeNode+'.outValueY', CTRLgroup+'.rotateY')
            cmds.connectAttr(rotRangeNode+'.outValueZ', CTRLgroup+'.rotateZ')

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

            cmds.connectAttr(endPlusMinNode+'.output3Dx', CTRLgroup+'.scaleX')
            cmds.connectAttr(endPlusMinNode+'.output3Dy', CTRLgroup+'.scaleY')
            cmds.connectAttr(endPlusMinNode+'.output3Dz', CTRLgroup+'.scaleZ')


            #Add every node to a container
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
                cmds.select(CTRLgroup, r=True)
                cmds.sets(cmds.ls(sl=True), add=theSet)
            else:
                cmds.select(CTRLgroup, r=True)
                theSet = cmds.sets(n=self.falloffName+'_FeatherfalloffSet')
            counter = counter+1



    def pickfeather(self, args):
        self.objFeather = cmds.ls(sl = True)[0]
        print self.objFeather
        self.isSelectedFeather=True
        self.featherProto = self.objFeather


    def pickobject(self, args):
        self.objBody = cmds.ls(sl = True)[0]
        print self.objBody
        self.isSelectedObject=True
        self.objectProto = self.objBody

    def pickController(self, args):
        self.objController = cmds.ls(sl = True)[0]
        print self.objController
        self.isSelectedObject=True
        self.controlMesh = self.objController


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
        self.objBody = ''
        self.objFeather = ''
        self.objController = ''
        self.featherRandomize = 0
        self.isSelectedFeather = False
        self.isSelectedObject = False
        self.size = defaultSize

    def my_range(self, start, end, step):
        while start <= end:
            yield start
            start += step

    # def testfunctionen(self, *args):
    #     print 'batammmamam fuckk yeahhh'

    def makeFeatherNow(self, r, h):

        #
        # self.featherU = self.myNumBalls
        hei = h
        rad = r

        # featherUU = getValueU()
        self.featherU = cmds.intSliderGrp( self.fetU, q=True, value=True )

        self.featherV = cmds.intSliderGrp( self.fetV, q=True, value=True )

        self.featherRandomize = cmds.intSliderGrp( self.fetRandom, q=True, value=True)


        # if self.isSelectedFeather is False:
        #     self.featherProto = cmds.polyPlane(w=self.width, h=hei)[0]

        if self.isSelectedObject is False:
            self.objectProto = cmds.sphere(r = 3)[0]


        shp = cmds.listRelatives(self.objectProto, s=True)[0]
        maxU = cmds.getAttr(shp+'.maxValueU')
        maxV = cmds.getAttr(shp+'.maxValueV')
        minU = cmds.getAttr(shp+'.minValueU')
        minV = cmds.getAttr(shp+'.minValueV')

        self.feathergroupName = cmds.group(n='FeatherGroup', em=True)
        folGrp = cmds.group(n='FollicleGroup', em=True)
        #Loop through the UVs
        counter = 1
        for fin_U in self.my_range(minU, 1.0, 1.0/self.featherU):
            for fin_V in self.my_range(minU, 1.0, 1.0/self.featherV):
                if self.featherRandomize == 0:
                    randomHeight = 1
                else:
                    randomHeight = random.randrange(100-self.featherRandomize, 100+self.featherRandomize)
                    randomHeight = randomHeight / 100.0

                if self.isSelectedFeather is False:
                    self.featherProto = cmds.polyPlane(w=self.width*randomHeight, h=hei)[0]

                CTRLgroup = cmds.group(n='CNTRL_GRP', em=True)
                SCALEgroup = cmds.group(n='SCALE_GRP', em=True)
                cmds.select(cl = True)
                cmds.select(self.featherProto)
                feather = cmds.duplicate(self.featherProto, n='myFeather')[0]
                cmds.select(cl = True)
                cmds.select(feather)
                if self.isSelectedFeather is False:
                    cmds.move(self.width*randomHeight/2.0, 0, 0, ws=True)
                cmds.move(0, 0, 0, feather+".scalePivot",feather+".rotatePivot", absolute=True)

                if self.isSelectedFeather is True:
                    cmds.rotate(90, 0, 0)
                else:
                    cmds.rotate(0, -90, 90 )
                cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
                locator = cmds.spaceLocator(n=feather+'_DistanceLoc')
                cmds.parent(locator, feather)
                cmds.setAttr(locator[0]+'.visibility', 0)
                cmds.parent(feather, CTRLgroup)
                #Create follicle and name it
                cmds.createNode('follicle')
                cmds.pickWalk(d='up')
                cmds.rename(cmds.ls(sl=True), self.objectProto+'_'+feather+'_Follicle')
                cmds.pickWalk(d='down')
                thisFollicle = cmds.ls(sl=True)

                cmds.select(thisFollicle, r=True)
                cmds.pickWalk(d='up')
                thisFollicleTransform = cmds.ls(sl=True)
                #Set follicle UV position


                if counter%2 == 0:
                	print 'NaN'
                	cmds.setAttr(thisFollicle[0]+'.parameterU', fin_U+1.0/self.featherU)

                else:
                    cmds.setAttr(thisFollicle[0]+'.parameterU', fin_U)

                cmds.setAttr(thisFollicle[0]+'.parameterV', fin_V)
                #Attach follicle to the object
                cmds.connectAttr(self.objectProto+'.local', thisFollicle[0]+'.inputSurface', f=True)
                cmds.connectAttr(self.objectProto+'.worldMatrix[0]', thisFollicle[0]+'.inputWorldMatrix', f=True)
                #Attach follicle to itself
                cmds.connectAttr(thisFollicle[0]+'.outTranslate', thisFollicleTransform[0]+'.translate', f=True)
                cmds.connectAttr(thisFollicle[0]+'.outRotate', thisFollicleTransform[0]+'.rotate', f=True)
                #Attach feather object to follicle
                cmds.connectAttr(thisFollicleTransform[0]+'.translate', CTRLgroup+'.translate', f=True)
                cmds.connectAttr(thisFollicleTransform[0]+'.rotate', feather+'.rotate', f=True)
                #Hide follicle
                cmds.setAttr(thisFollicleTransform[0]+'.visibility', 0)


                #some parenting
                cmds.parent(CTRLgroup, SCALEgroup)
                cmds.parent(SCALEgroup, self.feathergroupName)
                cmds.parent(thisFollicleTransform, folGrp)
                counter = counter+1
                if self.isSelectedFeather is False:
                    cmds.delete(self.featherProto)
                if fin_U == 0:
                	break
                if fin_U > 1.0-(1.0/self.featherU):
                	break

        print 'Batman'
        cmds.select(cl = True)


    def makeDynamic(self):
        cmds.select(self.controlMesh, self.objectProto)
        maymel.eval("doWrapArgList \"1\" { \"1\",\"0\",\"1\", \"2\", \"0\", \"1\", \"0\", \"0\" };")
        cmds.setAttr(self.controlMesh+'.castsShadows', 1)
        cmds.setAttr(self.controlMesh+'.receiveShadows', 1)
        cmds.setAttr(self.controlMesh+'.motionBlur', 1)
        cmds.setAttr(self.controlMesh+'.primaryVisibility', 1)
        cmds.setAttr(self.controlMesh+'.smoothShading', 1)
        cmds.setAttr(self.controlMesh+'.visibleInReflections', 1)
        cmds.setAttr(self.controlMesh+'.visibleInRefractions', 1)

        cmds.soft(self.controlMesh, g=0.8, h=True)
        cmds.rename('copyOf'+self.controlMesh, self.controlMesh+'_SOFT')
        select(self.controlMesh+'_SOFT', r=True)
        self.softBody = pickWalk(d='up')
        print self.softBody
        print 'asdasd'
        self.softBodyParticle = cmds.rename('copyOf'+self.controlMesh+'Particle', self.controlMesh+'_SOFT_PARTICLE')

        #A cool transparent shader

        if cmds.objExists('Dynamic_Shader') is False:
            Dynamic_Shader = shadingNode('lambert', n='Dynamic_Shader', asShader=True)
            Dynamic_Shader.transparency.set(0.9, 0.9, 0.9)
            Dynamic_Shader.color.set(0.0, 1.0, 0.0)
            select(self.softBody[0])
            hyperShade(ls(sl=True)[0], assign='Dynamic_Shader')
        else:
            select(self.softBody[0])
            hyperShade(ls(sl=True)[0], assign='Dynamic_Shader')


        #Fixing the softbody to locate closest point etc...
        self.softBodyShape = pickWalk(self.softBody[0], d='down')
        select(self.softBody[0])
        minU = ls(sl=True)[0].minValueU.get()
        maxU = ls(sl=True)[0].maxValueU.get()
        minV = ls(sl=True)[0].minValueV.get()
        maxV = ls(sl=True)[0].maxValueV.get()

        setRangeNode = createNode('setRange', n=self.softBody[0]+'_UVcalc')
        setRangeNode.minX.set(0)
        setRangeNode.minY.set(0)
        setRangeNode.maxX.set(1)
        setRangeNode.maxY.set(1)

        setRangeNode.oldMinX.set(minU)
        setRangeNode.oldMinY.set(minV)
        setRangeNode.oldMaxX.set(maxU)
        setRangeNode.oldMaxY.set(maxV)

        closestPointNode = createNode('closestPointOnSurface', n='closestPoint')
        select(self.softBody[0])
        ls(sl=True)[0].worldSpace[0].connect(closestPointNode.inputSurface)
        scaleGroups = cmds.listRelatives(self.feathergroupName)
        folLocGrp = group(n='folliclesAndLocs', em=True)
        for scaleGroup in scaleGroups:
            select(pickWalk(scaleGroup, d='down'))
            feather = pickWalk(d='down')
            makeIdentity(apply=True, t=0, r=0, s=1, n=0)

            aimLoc = spaceLocator(n=feather[0]+'_aimLoc')
            parent(aimLoc, feather[0])
            xform(a=True, t=[0.0, 0.0, 0.0])
            xform(a=True, t=[0.0, 0.0, self.width])
            #Parent to world
            parent(w=True)
            makeIdentity(apply=True, t=1, r=1, s=1, n=0)
            aimLoc.visibility.set(0)
            #This can be wrong...
            aimConstr = aimConstraint(aimLoc,feather[0], mo=True, weight=1, aimVector=[0.0, 0.0, 1.0], upVector=[0.0, 1.0, 0.0], worldUpType='none')
            featherWs = xform(aimLoc, q=True, ws=True, rp=True)
            closestPointNode.inPositionX.set(featherWs[0])
            closestPointNode.inPositionY.set(featherWs[1])
            closestPointNode.inPositionZ.set(featherWs[2])

            posU = closestPointNode.parameterU.get()
            posV = closestPointNode.parameterV.get()

            setRangeNode.valueX.set(posU)
            setRangeNode.valueY.set(posV)

            calcPosU=setRangeNode.outValueX.get()
            calcPosV=setRangeNode.outValueY.get()

            createNode('follicle')
            pickWalk(d='up')
            follicleTrans = rename(ls(sl=True) ,self.softBody[0]+'_Follicle')
            pickWalk(d='down')
            follicle = ls(sl=True)
            select(self.softBody[0])
            ls(sl=True)[0].local.connect(follicle[0].inputSurface)
            ls(sl=True)[0].worldMatrix[0].connect(follicle[0].inputWorldMatrix)
            follicle[0].outTranslate.connect(follicleTrans.translate)
            follicle[0].outRotate.connect(follicleTrans.rotate)

            follicle[0].parameterU.set(calcPosU)
            follicle[0].parameterV.set(calcPosV)
            follicle[0].visibility.set(0)
            parent(follicle[0], folLocGrp)
            parent(aimLoc, folLocGrp)
            pointConstr = pointConstraint(follicleTrans, aimLoc, mo=True)







    # Invoked when the command is run.
    def doIt(self,args):
        self.parseArguments(args)
        #check to see if our windows exists
        if cmds.window("Featherizerzzrzrzz", exists = True):
            cmds.deleteUI("Featherizerzzrzrzz")



        #create our window
        window = cmds.window("Featherizerzzrzrzz", title = "Featherizerzzrzrzz", w = 500, h = 300, mnb = False, mxb = False, sizeable = False)



        #create main layout
        mainLayout = cmds.columnLayout(w = 500, h = 500)

        #create projects options menu
        cmds.separator(h = 15)
        # objectOptionsMenu = cmds.optionMenu(w = 300, label = "Choose object to featherize: ")

        self.button = cmds.button(label = "Use selected object as feather", w = 300, h = 50, command=self.pickfeather)
        cmds.separator(h = 5)
        self.button = cmds.button(label = "Use selected object as body", w = 300, h = 50, command=self.pickobject)
        cmds.separator(h = 5)
        self.fetU = cmds.intSliderGrp( label="Numbers of Feather U", field=True, value = 10, minValue = 1, maxValue = 100, step = 1)
        self.fetV = cmds.intSliderGrp( label="Numbers of Feather V", field=True, value = 10, minValue = 1, maxValue = 100, step = 1)
        self.fetRandom = cmds.intSliderGrp( label="Randomize the Feather length", value = 0, minValue = 0, maxValue = 100, step = 1)
        #create character options menu
        cmds.separator(h = 15)
        #create build button
        cmds.separator(h = 15)
        cmds.button(label = "Make Bird or whatever", w = 300, h = 50, command=lambda *args: self.makeFeatherNow(5.0, 1.0))
        cmds.button(label = "Create falloffobject", w = 300, h = 50, command=lambda *args: self.createFalloffObject())

        self.button = cmds.button(label = "Use selected object as controller", w = 300, h = 50, command=self.pickController)
        cmds.button(label = "Add Dynamics", w = 300, h = 50, command=lambda *args: self.makeDynamic())
        #Show window
        cmds.showWindow(window)


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
