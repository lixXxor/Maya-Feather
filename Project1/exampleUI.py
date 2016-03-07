import maya.cmds as cmds

#run to keep UI updated in maya
#import exampleUI
#reload(exampleUI)
#exampleUI.UI()

def UI():
    #check to see if our windows exists
    if cmds.window("exampleUI", exists = True):
        cmds.deleteUI("exampleUI")


    #create our window
    window = cmds.window("exampleUI", title = "ExampleUI", w = 300, h = 300, mnb = False, mxb = False, sizeable = False)


    #create main layout
    mainLayout = cmds.columnLayout(w = 300, h = 300)

    #banner image (bilden ska ligga under prefs/icons i maya
    #imagePath = cmds.internalVar(upd = true) + "icons/example.jpg"
    #cmds.image(w = 300, h = 100, image = imagePath)

    #create projects options menu
    cmds.separator(h = 15)
    objectOptionsMenu = cmds.optionMenu(w = 300, label = "Choose an object: ")
    
    #create character options menu
    cmds.separator(h = 15)
    characterOptionsMenu = cmds.optionMenu(w = 300, label = "Dick butt: ")

    #create build button
    cmds.separator(h = 15)
    cmds.button(label = "Build", w = 300, h = 50)

    #Show window
    cmds.showWindow(window)


def Testfunctionen():
    print 'hej hej'


def Petergus():
    print 'hej hej'