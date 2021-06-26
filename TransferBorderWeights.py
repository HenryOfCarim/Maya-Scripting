import posixpath
import ntpath

import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel
#enable  ordered selection
cmds.selectPref( trackSelectionOrder=1 )

def getVertexWeights():
        
    global weightsList 
    weightsList =[]
    meshSkinCluster = ""
    vertexWeightList =[]   
    
    # get all selected vetices in order
    verts = cmds.ls(flatten = True, orderedSelection = True)
    cmds.polyEvaluate( v=True)
    # check is any vertex 
    if len(verts) == 0:
        return cmds.error( "Please select vetices with skin weighs" )
    else:
        obj = cmds.ls(verts[0], objectsOnly = True)
        history = cmds.listHistory(obj) 
    #get mesh skin cluster
        for historyNode in history:
            if cmds.nodeType(historyNode)=="skinCluster":
                meshSkinCluster = historyNode
    #get joint list   
        for each in verts:
            #get weight values
            skinVals = cmds.skinPercent(meshSkinCluster, each, query=True, value=True)
            #get joints list which affect vetex
            jointVals = cmds.skinPercent(meshSkinCluster, each, query=True, transform=None)
            #clear list before creating child
            vertexWeightList = []
            for i in range(len(jointVals)):
                #clear list every loop
                childList =[] 
                #build list [jointName, weightValue]
                if skinVals[i] > 0:
                    childList.append(jointVals[i])
                    childList.append(skinVals[i])
                    print childList
                    #add values of each influenced joint to the list which will represent one vertex data
                    vertexWeightList.append(childList)
            #add each vertexWeightList to the weightsList
            weightsList.append(vertexWeightList)
        cmds.button("applyWeightsBtn",edit=True, enable=True)
        cmds.select(clear=True)
        verts=[]   

def setBorderWeights():
    verts = cmds.ls(flatten = True, orderedSelection = True)
    
    #check if anything selected
    if len(verts) == 0:
        return cmds.error( "Please select vetices with skin weighs" )
    else:
        obj = cmds.ls(verts[0], objectsOnly=True)
        print obj
        
        history = cmds.listHistory(obj) 
        #get mesh skin cluster
        for historyNode in history:
            if cmds.nodeType(historyNode)=="skinCluster":
                meshSkinCluster = historyNode   
        #get namespace
        objNamespace = pm.selected()[0].namespace()
        #if there is no namespace apply weight frome the stored list without changes
        if objNamespace=='':
            for i in range(len(verts)):  
                cmds.skinPercent( meshSkinCluster, verts[i], transformValue=weightsList[i])
                print 'no namespace'
        else:
            #
            for i in range(len(verts)):
                for j in range (len(weightsList[i])):
                    tempName = weightsList[i][j][0]
                    weightsList[i][j][0] = objNamespace+tempName
                    print weightsList[i][j][0]
            #apply weights from the stored list to selected vertice
            for i in range(len(verts)):  
                cmds.skinPercent( meshSkinCluster, verts[i], transformValue=weightsList[i])
        cmds.button("applyWeightsBtn",edit=True, enable=False)
        cmds.select(clear=True)
        verts=[]    

def exportNamespace():
        objNamespace = pm.selected()[0].namespace()
        if objNamespace == '':
            print "There is no namespace selected"
        else:
            cmds.select(objNamespace+'*', replace=True)
            objName=objNamespace.replace(":", "")
            #cmds.file(rename=objName+".ma")
            filePath = cmds.fileDialog2(fileMode=0, fileFilter="Maya files (*.ma)")
            toMayaPath = filePath[0].replace(ntpath.sep, posixpath.sep)
            print str(toMayaPath)
            
            cmds.file(rename=str(toMayaPath))
            cmds.file(force=True, exportSelected=True, type="mayaAscii", relativeNamespace=":"+objNamespace)


def showUI():
    if (cmds.window("TransferBorderWeights", exists=True)):
        cmds.deleteUI("TransferBorderWeights")
        
    myWin = cmds.window("TransferBorderWeights",title="Transfer border Weights", resizeToFitChildren=True,maximizeButton=False, widthHeight=(300,40))
    cmds.columnLayout()
    
    cmds.rowLayout(numberOfColumns=2)
    cmds.button("storeWeightsBtn",label="Store Weights", enable=True, command="getVertexWeights()", width=150)
    cmds.button("applyWeightsBtn",label="Apply Weights", enable=False, command="setBorderWeights()", width=150)
    cmds.setParent("..")
    cmds.rowLayout(numberOfColumns=1)
    cmds.button("exportFromNamespace", label ='Export Selected Namespace', enable=True, command="exportNamespace()", width=300)
    cmds.setParent('..')
    
    cmds.showWindow(myWin)
showUI()
