#dropToFloor.py 2017 Issei Mori
#Drops the selected objects on the floor with an optional offset value
"""
1.Place this file into the scripts folder,
2.Paste the code below in your python Script Editor

import dropToFloor
import imp
imp.reload(dropToFloor)
dropToFloor.Window()

3.Click "Save Script to Shell" in the Script Editor menu bar to save this script in your shellf
"""
from maya import cmds

#drop the selected objects to the ground with offset
def dropToFloor(nodes = None, offset = 0):
    #no object is selected, return error
    if not nodes:
        nodes = cmds.ls(sl = True)

    if not nodes:
        cmds.error("No object is selected")

    #for loop for each object
    for node in nodes:
        #get the bouding box
        bbox = cmds.exactWorldBoundingBox(node)

        #store minimum y value
        minValue = bbox[1]

        #get wordl coordinate of the object
        ws = cmds.xform(node, q = True, t = True, ws = True)

        #calculate the difference between the floor with offset
        distance = ws[1] - bbox[1] + float(offset)
        ws[1] = distance
        
        #move the object
        cmds.xform(node, translation = ws, ws = True)

#window class to open window
#call this class to run the script
class Window(object):
    def __init__(self):
        self.name = "DropToFloor"
        #close the current window if the same name window exists
        if cmds.window(self.name, q = True, exists = True):
            cmds.deleteUI(self.name)

        #open window
        window = cmds.window(self.name)

        #build UI
        self.buildUI()

        #show window
        cmds.showWindow()
        cmds.window(window, edit = True, height = 50, width = 100)

    #UI implementation
    def buildUI(self):
        #set up column
        column = cmds.columnLayout()

        #offset value input box
        self.offset = cmds.intSliderGrp(label = "Offset", field = True)
        #Run button
        cmds.button(label = "Drop", command = self.onApplyClick)
    
    def onApplyClick(self, *args):
        dropToFloor(offset = cmds.intSliderGrp(self.offset, query = True, value = True))
        cmds.deleteUI(self.name)