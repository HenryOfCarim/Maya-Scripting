import maya.cmds as cmds

global rotationField

global isXPlus
global isXMinus
global isYPlus
global isYMinus
global isZPlus
global isZMinus

isXPlus = 0
isXMinus = 0
isYPlus = 0
isYMinus = 0
isZPlus = 0
isZMinus = 0
    
def setTestAnim():
    global rotationField
    global isXPlus
    global isXMinus
    global isYPlus
    global isYMinus
    global isZPlus
    global isZMinus
    
    timeZero = 0
    timeLenght = 5
    jntRotation = cmds.intField(rotationField, query=True, value=True)
    
    if isXPlus == 1:
        setKeyframes(timeZero,timeLenght)
        timeZero += timeLenght*2
        cmds.rotate(jntRotation,0,0,relative=True)
        
    if isXMinus == 1:
        setKeyframes(timeZero,timeLenght)
        timeZero += timeLenght*2
        cmds.rotate(-1*jntRotation,0,0,relative=True)
        
    if isYPlus == 1:
        setKeyframes(timeZero,timeLenght)
        timeZero += timeLenght*2
        cmds.rotate(0,jntRotation,0,relative=True)                
        
    if isYMinus == 1:
        setKeyframes(timeZero,timeLenght)
        timeZero += timeLenght*2
        cmds.rotate(0,-1*jntRotation,0,relative=True)

    if isZPlus == 1:
        setKeyframes(timeZero,timeLenght)
        timeZero += timeLenght*2
        cmds.rotate(0,0,jntRotation,relative=True)
                
    if isZMinus == 1:
        setKeyframes(timeZero,timeLenght)
        timeZero += timeLenght*2
        cmds.rotate(0,0,-1*jntRotation,relative=True)
        
def setKeyframes(zero,time):
    
    selection = cmds.ls(selection=True)
    cmds.currentTime(zero)
    cmds.setKeyframe(selection[0])
    cmds.currentTime(zero+time*2)
    cmds.setKeyframe(selection[0])
    cmds.currentTime(zero+time)
    
    
def deleteKeyframes(time):
    selection = cmds.ls(selection=True)
    cmds.currentTime(0)
    cmds.cutKey( time=(0,60) )
    

def createAnimHelperWindow():
        global rotationField
        global isXPlus
        global isXMinus
        global isYPlus
        global isYMinus
        global isZPlus
        global isZMinus
        
        if (cmds.window("Re5AnimHelp", exists=True)):
            cmds.deleteUI("Re5AnimHelp")


            
        animHelperWin = cmds.window("Re5AnimHelp",title="Rigging Animation Helper", menuBar=True, widthHeight=(280,100))
        cmds.rowLayout(numberOfColumns=4)
        cmds.text("Rotation Angle")
        rotationField = cmds.intField(value=90)
        cmds.button("setBtn", label="Add", command="setTestAnim()")
        cmds.button("clearBtn", label="Clear All", command="deleteKeyframes(5)")
        cmds.setParent("..")
        
        cmds.rowLayout(numberOfColumns=1)
        cmds.text(label = "Rotation axis", align='center', backgroundColor = (0.2,0.2,0.2))
        cmds.setParent("..")
        
        cmds.rowLayout(numberOfColumns=6)
        cmds.checkBox("xPlusChBx",label="x+",onCommand="isXPlus = 1", offCommand="isXPlus = 0")
        cmds.checkBox("xMinusChBx",label="x-",onCommand="isXMinus = 1", offCommand="isXMinus = 0")
        cmds.checkBox("yPlusChBx",label="y+",onCommand="isYPlus = 1", offCommand="isYPlus = 0")
        cmds.checkBox("yMinusChBx",label="y-",onCommand="isYMinus = 1", offCommand="isYMinus = 0")
        cmds.checkBox("zPlusChBx",label="z+",onCommand="isZPlus = 1", offCommand="isZPlus = 0")
        cmds.checkBox("zMinusChBx",label="z-",onCommand="isZMinus = 1", offCommand="isZMinus = 0")
        cmds.setParent("..")
             
        cmds.showWindow(animHelperWin)
        
createAnimHelperWindow()