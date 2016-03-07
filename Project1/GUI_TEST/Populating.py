
    # Invoked when the command is run.
def make_it_feather(self,args):
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

    cmds.connectAttr(sphere1+'.rotate', fGrp+'.rotate')
    for fin_U in self.my_range(minU, maxU, 0.5):
        for fin_V in self.my_range(minV, maxV, 0.5):
            uvSphere = cmds.pointOnSurface(sphere1, u=fin_U, v=fin_V, position=True )
            uvSphereNormalized = cmds.pointOnSurface(sphere1, u=fin_U, v=fin_V, nn = True )
            uvSphereTangentU = cmds.pointOnSurface(sphere1, u=fin_U, v=fin_V, ntu = True )
            uvSphereTangentV = cmds.pointOnSurface(sphere1, u=fin_U, v=fin_V, ntv = True )
            cmds.select(cl = True)
            cmds.select(featherProto)
            feather = cmds.duplicate(featherProto, n='myPlane')[0]
            if self.isSelected is False:
                cmds.rotate(0, 0, -90)
                cmds.move(0, self.width/2.0, 0, ws=True)
            cmds.move(0, 0, 0, feather+".scalePivot",feather+".rotatePivot", absolute=True)
            cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
            cmds.move(uvSphere[0], uvSphere[1], uvSphere[2])
            angleEuler = cmds.angleBetween(euler = True, v1 = (0,1,0), v2 = uvSphereNormalized)
            cmds.pointConstraint(sphere1, feather, mo=True)
            cmds.geometryConstraint(sphere1, feather, w=2)
            # cmds.geometryConstraint(feather, sphere1)
            cmds.parent(feather, fGrp)
            cmds.select(cl = True)
            cmds.select(feather)
            hejehe = cmds.rotate(angleEuler[0], angleEuler[1], angleEuler[2])
            print hejehe

      
    print 'batman'
    cmds.select(cl = True)

