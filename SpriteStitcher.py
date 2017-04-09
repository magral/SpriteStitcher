# -*- coding: utf-8 -*-

import sys
import os
from PIL import Image
from PyQt5 import QtWidgets

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self): 
        #Labels
        self.labelDirectory = QtWidgets.QLabel("No directory selected") 
        labelCols = QtWidgets.QLabel("Columns")
        labelRows = QtWidgets.QLabel("Rows")
        labelSaveName = QtWidgets.QLabel("Final Image Name")
        labelSaveType = QtWidgets.QLabel("File Save Format")
        
        #Line edits
        self.saveName = QtWidgets.QLineEdit(self)
        self.cols = QtWidgets.QLineEdit(self)
        self.rows = QtWidgets.QLineEdit(self)
        
        #Buttons
        self.searchDirectory = QtWidgets.QPushButton("Search Directory")
        self.stitch = QtWidgets.QPushButton("Stitch Images")
        
        #Combo box
        self.saveType = QtWidgets.QComboBox(self)
        self.saveType.addItem("PNG")
        self.saveType.addItem("JPEG")
        self.saveType.addItem("GIF")
        
        #Other variables
        self.targetDir = "";
        
        #Set layout
        box = QtWidgets.QVBoxLayout()
        box.addStretch()
        box.addWidget(self.labelDirectory)
        box.addWidget(labelCols)
        box.addWidget(self.cols)
        box.addWidget(labelRows)
        box.addWidget(self.rows)
        box.addWidget(labelSaveName)
        box.addWidget(self.saveName)
        box.addWidget(labelSaveType)
        box.addWidget(self.saveType)
        box.addWidget(self.stitch)
        box.addStretch()
        
        v = QtWidgets.QVBoxLayout()
        v.addWidget(self.searchDirectory)
        v.addLayout(box)
        
        self.setLayout(v)
        self.setWindowTitle("Sprite Stitcher")
        
        #Connect buttons
        self.stitch.clicked.connect(self.stitchImages)
        self.searchDirectory.clicked.connect(self.openDirectoryDialogue)
        
        self.show()
         
    def openDirectoryDialogue(self):
        self.targetDir = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        if(self.targetDir):
            self.labelDirectory.setText(self.targetDir)
          
    def stitchImages(self):
        #Vars
        imageList = []
        root = self.targetDir
        intCols = int(self.cols.text())
        intRows = int(self.rows.text())
        xoff = 0
        yoff = 0
        imageStart = 0
        
        #Populate image list from directory
        for subdir, dirs, files in os.walk(root):
            for file in files:
                imageList.append(os.path.join(subdir, file))
                
                
        images = map(Image.open, imageList)
        
        #Create image size
        widths, heights = zip(*(i.size for i in images))
        total_width = max(widths) * intCols
        max_height = max(heights) * intRows
        
        finalImg = Image.new('RGB', (total_width, max_height))
        images = map(Image.open, imageList)
      
        listImages = list(images)
        
        #Paste images onto new image
        for i in range(1, (intRows + 1)):
            #In case of uneven image counts
            if len(listImages) - imageStart < intCols: 
                intCols = len(listImages) - imageStart
            print(intCols)
            for j in range(0, intCols):
                finalImg.paste(listImages[j + imageStart], (xoff, yoff))
                xoff += listImages[j].size[0]
            imageStart += intCols
            xoff = 0
            yoff += max(heights)
            
        saveTypeText = self.saveType.currentText()
        #Save file
        finalImg.save(root + '\\' + self.saveName.text() + '.' + saveTypeText.lower(), saveTypeText)
        
#Run program
app = QtWidgets.QApplication(sys.argv)
win = Window()
sys.exit(app.exec_())