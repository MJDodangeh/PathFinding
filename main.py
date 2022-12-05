import random

from PyQt5 import uic, QtWidgets, QtGui, QtCore
import sys
import time
from PyQt5.QtCore import QSize, QRect
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from queue import PriorityQueue


class TableButton(QPushButton):
    def __init__(self, text, style, color, parent=None):
        super(TableButton, self).__init__(text, parent)
        self.setStyleSheet(self.styleSheet()+style)
        self.setText(text)
        self.setMaximumSize(QSize(35,35))
        self.setMinimumSize(QSize(35,35))
        self.color = ""
        self.status = ""
        self.pre = ""


class Search(QtWidgets.QMainWindow):
    SourceNode = ''
    DestinationNode = ''
    Srow = ''
    Scolumn = ''
    Drow = ''
    Dcolumn = ''
    rows = 20
    columns = 30
    Styles = {"White":"background-color: white;","Red":"background-color: red;",
              "Lime":"background-color: lime;",
              "Black":"background-color:black;border-color:gray;border-width:0.5px;border-style:inset"}
    Buttons = [[0 for i in range(30)] for j in range(20)]
    def __init__(self):
        super().__init__()
        self.show()
        Widget = QWidget()
        vertical = QVBoxLayout()
        inWidget = QWidget()
        self.layout = QGridLayout(inWidget)
        self.layout.setVerticalSpacing(0)
        self.layout.setHorizontalSpacing(0)
        vertical.addWidget(inWidget)
        Widget.setLayout(vertical)
        self.setCentralWidget(Widget)

        self.UpRow=QHBoxLayout()
        self.ButtomRow=QHBoxLayout()

        self.GP_btn = QPushButton("Generate Pattern")
        self.GP_btn.setFont(QFont('Eras Medium ITC', 8))
        self.HP_btn = QPushButton("Handy Pattern")
        self.HP_btn.setFont(QFont('Eras Medium ITC', 8))
        self.Search_btn = QPushButton("Search")
        self.Search_btn.setFont(QFont('Eras Medium ITC', 8))
        self.Clear_btn = QPushButton("Clear")
        self.Clear_btn.setFont(QFont('Eras Medium ITC', 8))
        self.Clear_btn.setMaximumSize(QSize(140, 30))
        self.Undo_btn = QPushButton("Undo")
        self.Undo_btn.setFont(QFont('Eras Medium ITC', 8))
        self.Undo_btn.setMaximumSize(QSize(80,30))
        self.Undo_btn.setEnabled(False)
        self.Algrtm_lbl = QLabel("Algorithm:")
        self.Algrtm_lbl.setFont(QFont('Eras Medium ITC', 8))
        self.Algrtm_lbl.setMaximumSize(QSize(80,30))
        self.Algrtm_lbl.setMargin(9)
        self.Color_lbl = QLabel("Color:")
        self.Color_lbl.setFont(QFont('Eras Medium ITC', 8))
        self.Color_lbl.setMaximumSize(QSize(80,30))
        self.Color_lbl.setMargin(10)
        self.Time_lbl = QLabel("Time of Execution:")
        self.Time_lbl.setFont(QFont('Eras Medium ITC', 8))
        self.Time_lbl.setMaximumSize(QSize(150, 30))
        self.Time_lbl.setMargin(20)
        self.atTime_lbl = QLabel("-")
        self.atTime_lbl.setFont(QFont('Eras Medium ITC', 8))
        self.atTime_lbl.setMaximumSize(QSize(120, 30))
        self.atTime_lbl.setMargin(20)

        self.Nodes_lbl = QLabel("Opened Nodes:")
        self.Nodes_lbl.setFont(QFont('Eras Medium ITC', 8))
        self.Nodes_lbl.setMaximumSize(QSize(150, 30))
        self.Nodes_lbl.setMargin(20)
        self.atNodes_lbl = QLabel("-")
        self.atNodes_lbl.setFont(QFont('Eras Medium ITC', 8))
        self.atNodes_lbl.setMaximumSize(QSize(120, 30))
        self.atNodes_lbl.setMargin(20)

        self.Algrtm_cmb = QComboBox(Widget)
        self.Algrtm_cmb.setObjectName(("Algrtm_cmb"))
        self.Algrtm_cmb.setFont(QFont('Eras Medium ITC', 8))
        self.Algrtm_cmb.addItem("DFS")
        self.Algrtm_cmb.addItem("BFS")
        self.Algrtm_cmb.addItem("A*")

        self.Color_cmb = QComboBox(Widget)
        self.Color_cmb.setObjectName(("Color_cmb"))
        self.Color_cmb.setFont(QFont('Eras Medium ITC', 8))
        self.Color_cmb.addItem("Black")
        self.Color_cmb.addItem("White")
        self.Color_cmb.addItem("Red")
        self.Color_cmb.addItem("Lime")

        self.UpRow.addWidget(self.GP_btn)
        self.ButtomRow.addWidget(self.HP_btn)
        self.UpRow.addWidget(self.Search_btn)
        self.ButtomRow.addWidget(self.Clear_btn)
        self.ButtomRow.addWidget(self.Undo_btn)
        self.UpRow.addWidget(self.Algrtm_lbl)
        self.ButtomRow.addWidget(self.Color_lbl)
        self.UpRow.addWidget(self.Algrtm_cmb)
        self.ButtomRow.addWidget(self.Color_cmb)
        self.UpRow.addWidget(self.Time_lbl)
        self.UpRow.addWidget(self.atTime_lbl)
        self.ButtomRow.addWidget(self.Nodes_lbl)
        self.ButtomRow.addWidget(self.atNodes_lbl)

        vertical.addLayout(self.UpRow)
        vertical.addLayout(self.ButtomRow)
        for row in range(self.rows):
            for column in range(self.columns):
                if (row != 0 and row != 19) and (column != 0 and column != 29):
                    button = TableButton('', style=self.Styles["White"], color="white")
                    self.Buttons[row][column]=button
                    button.clicked.connect(self.CP_ButtonClicked)
                    button.setEnabled(False)
                    self.layout.addWidget(button, row+1 , column)
                else:
                    button = TableButton('', style=self.Styles["Black"], color="black")
                    self.Buttons[row][column] = button
                    self.layout.addWidget(button, row + 1, column)

        self.GP_btn.clicked.connect(self.GP_func)
        self.HP_btn.clicked.connect(self.HP_func)
        self.Clear_btn.clicked.connect(self.Clear_func)
        self.Search_btn.clicked.connect(self.Search_func)
        self.Algrtm_cmb.currentTextChanged.connect(self.Edit_Alg)
        self.Undo_btn.clicked.connect(self.Undo_func)

    def CP_ButtonClicked(self):
        #global SourceNode
        #global DestinationNode
        NowColor = self.sender().palette().window().color().name()
        if self.Color_cmb.currentText() == "White" or self.Color_cmb.currentText() == "Black":
            self.sender().setStyleSheet(self.Styles[self.Color_cmb.currentText()])
            if NowColor == "#ff0000":
                self.DestinationNode = ''
            if NowColor == "#00ff00":
                self.SourceNode = ''
        if self.Color_cmb.currentText() == "Red":
            if self.DestinationNode == '':
                if NowColor == "#00ff00":
                    self.SourceNode = ''
                self.sender().setStyleSheet(self.Styles["Red"])
                self.DestinationNode = self.sender()
            else:
                QMessageBox.about(self, "Error", "Destination specified!")
        if self.Color_cmb.currentText() == "Lime":
            if self.SourceNode == '':
                if NowColor == "#ff0000":
                    self.DestinationNode = ''
                self.sender().setStyleSheet(self.Styles["Lime"])
                self.SourceNode = self.sender()
            else:
                QMessageBox.about(self, "Error", "Source specified!")

    def Clear_func(self):
        for row in range(1,self.rows-1):
            for column in range(1,self.columns-1):
                    self.Buttons[row][column].setStyleSheet(self.Styles["White"])
                    self.Buttons[row][column].setText("")
                    self.SourceNode = ''
                    self.DestinationNode = ''
                    self.Buttons[row][column].setEnabled(False)
                    self.Buttons[row][column].status = ""
                    self.Buttons[row][column].pre = ""
        self.Search_btn.setEnabled(True)

    def Undo_func(self):
        for row in range(1,self.rows-1):
            for column in range(1,self.columns-1):
                self.Buttons[row][column].status = ""
                self.Buttons[row][column].pre = ""
                if self.Colorb(self.Buttons[row][column]) == "#d8bfd8" or self.Colorb(self.Buttons[row][column]) == "#00ffff":
                    self.Buttons[row][column].setStyleSheet(self.Styles["White"])
                    self.Buttons[row][column].setText("")
        self.Search_btn.setEnabled(True)

    def GP_func(self):
        self.Clear_func()
        i = random.randint(50,150)
        for x in range(i):
            a = random.randint(1,18)
            b = random.randint(1,28)
            self.Buttons[a][b].setStyleSheet(self.Styles["Black"])
            self.HP_func()
        sr = random.randint(1,18)
        dr = random.randint(1,18)
        sc = random.randint(1,28)
        dc = random.randint(1,28)
        self.Buttons[dr][dc].setStyleSheet(self.Styles["Red"])
        self.DestinationNode = self.Buttons[dr][dc]
        self.Buttons[sr][sc].setStyleSheet(self.Styles["Lime"])
        self.SourceNode = self.Buttons[sr][sc]

    def HP_func(self):
        for row in range(1, self.rows - 1):
            for column in range(1, self.columns - 1):
                self.Buttons[row][column].setEnabled(True)

    def SearchNode(self,Node):
        for row in range(1, self.rows - 1):
            for column in range(1, self.columns - 1):
                if self.Buttons[row][column] == Node:
                    return row,column

    def Search_func(self):
        if self.Algrtm_cmb.currentText() == "DFS":
            start = time.time()
            if self.SourceNode != '' and self.DestinationNode != '':
                self.Srow,self.Scolumn=self.SearchNode(self.SourceNode)
                self.Drow,self.Dcolumn=self.SearchNode(self.DestinationNode)
                CurNode = self.SourceNode
                CurRow = self.Srow
                CurCol = self.Scolumn
                Fringe=[]
                OpenNode = 0
                while CurNode != self.DestinationNode:
                        if self.Colorb(self.Buttons[CurRow-1][CurCol]) == "#ffffff" or self.Colorb(self.Buttons[CurRow-1][CurCol]) == "#ff0000":
                            self.Buttons[CurRow - 1][CurCol].setStyleSheet("background-color: thistle;")
                            CurNode = self.Buttons[CurRow-1][CurCol]
                            CurRow = CurRow-1
                            Fringe.append((CurNode,CurRow,CurCol))
                            OpenNode=OpenNode+1
                            continue
                        if self.Colorb(self.Buttons[CurRow][CurCol+1]) == "#ffffff" or self.Colorb(self.Buttons[CurRow][CurCol+1]) == "#ff0000":
                            self.Buttons[CurRow][CurCol+1].setStyleSheet("background-color: thistle;")
                            CurNode = self.Buttons[CurRow][CurCol+1]
                            CurCol = CurCol+1
                            Fringe.append((CurNode, CurRow, CurCol))
                            OpenNode = OpenNode + 1
                            continue
                        if self.Colorb(self.Buttons[CurRow+1][CurCol]) == "#ffffff" or self.Colorb(self.Buttons[CurRow+1][CurCol]) == "#ff0000":
                            self.Buttons[CurRow + 1][CurCol].setStyleSheet("background-color: thistle;")
                            CurNode = self.Buttons[CurRow + 1][CurCol]
                            CurRow = CurRow + 1
                            Fringe.append((CurNode, CurRow, CurCol))
                            OpenNode = OpenNode + 1
                            continue
                        if self.Colorb(self.Buttons[CurRow][CurCol-1]) == "#ffffff" or self.Colorb(self.Buttons[CurRow][CurCol-1]) == "#ff0000":
                            self.Buttons[CurRow][CurCol-1].setStyleSheet("background-color: thistle;")
                            CurNode = self.Buttons[CurRow][CurCol-1]
                            CurCol = CurCol - 1
                            Fringe.append((CurNode, CurRow, CurCol))
                            OpenNode = OpenNode + 1
                            continue
                        else:
                            Fringe.pop()
                            if len(Fringe) == 0:
                                QMessageBox.about(self, "Error", "NotFound!")
                                return
                            CurNode = Fringe[-1][0]
                            CurRow = Fringe[-1][1]
                            CurCol = Fringe[-1][2]
                            continue
                self.DestinationNode.setStyleSheet("background-color: red;")
                n=1
                Fringe.pop()
                for i in Fringe:
                    i[0].setStyleSheet("background-color: aqua;")
                    i[0].setText(str(n))
                    n=n+1
            else:
                QMessageBox.about(self, "Error", "Please Select Source and Destination!")
                return
            end = time.time()
            self.atTime_lbl.setText(str(round(1000*(end-start)))+" ms")
            self.atNodes_lbl.setText(str(OpenNode+1))
        if self.Algrtm_cmb.currentText() == "BFS":
            start = time.time()
            if self.SourceNode != '' and self.DestinationNode != '':
                self.Srow,self.Scolumn=self.SearchNode(self.SourceNode)
                self.Drow,self.Dcolumn=self.SearchNode(self.DestinationNode)
                CurNode = self.SourceNode
                CurRow = self.Srow
                CurCol = self.Scolumn
                Fringe=[]
                Fringe.append((CurNode,CurRow,CurCol))
                m=0
                OpenNode = 0
                while CurNode != self.DestinationNode:
                    if len(Fringe) == 0:
                        QMessageBox.about(self, "Error", "NotFound!")
                        return
                    x = Fringe.pop(0)
                    CurNode = x[0]
                    CurRow = x[1]
                    CurCol = x[2]
                    tChild = self.AChild(CurNode,CurRow,CurCol)
                    if not tChild:
                        if self.Colorb(CurNode) != "#ff0000" and self.Colorb(CurNode) != "#00ff00":
                            CurNode.setStyleSheet("background-color: thistle;")
                            OpenNode = OpenNode + 1
                        continue
                    else:
                        for c in tChild:
                            if c not in Fringe:
                                Fringe.append(c)
                            if self.Colorb(CurNode) != "#ff0000" and self.Colorb(CurNode) != "#00ff00" and self.Colorb(CurNode) != "#d8bfd8":
                                CurNode.setStyleSheet("background-color: thistle;")
                                OpenNode = OpenNode + 1
                        continue
                res=[]
                while CurNode != self.SourceNode:
                    res.append(CurNode)
                    CurNode = self.Buttons[CurRow][CurCol].pre[0]
                    CurRow,CurCol = self.Buttons[CurRow][CurCol].pre[1],self.Buttons[CurRow][CurCol].pre[2]
                res.reverse()
                res.pop()
                m=1
                for i in res:
                    i.setStyleSheet("background-color: aqua;")
                    i.setText(str(m))
                    m=m+1
            else:
                QMessageBox.about(self, "Error", "Please Select Source and Destination!")
                return
            end = time.time()
            self.atTime_lbl.setText(str(round(1000*(end-start)))+" ms")
            self.atNodes_lbl.setText(str(OpenNode+2))
        if self.Algrtm_cmb.currentText() == "A*":
            start = time.time()
            if self.SourceNode != '' and self.DestinationNode != '':
                self.Srow,self.Scolumn=self.SearchNode(self.SourceNode)
                self.Drow,self.Dcolumn=self.SearchNode(self.DestinationNode)
                CurNode = self.SourceNode
                CurRow = self.Srow
                CurCol = self.Scolumn
                PQFringe = PriorityQueue()
                g=0
                s=1
                OpenNode=0
                while CurNode != self.DestinationNode:
                    if g!=0:
                        g=get[1]+1
                    else:
                        g=1
                    aChild = self.AChild(CurNode,CurRow,CurCol)
                    for i in aChild:
                        h = self.Calh(i[1],i[2])
                        f=g+h
                        cr=(i[1],i[2])
                        if i[0].status != "added":
                            PQFringe.put((f,g,h,cr))
                            i[0].status="added"
                    if PQFringe.empty() and len(aChild) != 1:
                        QMessageBox.about(self, "Error", "NotFound!")
                        return
                    if not PQFringe.empty():
                        get = PQFringe.get()
                    CurRow = get[3][0]
                    CurCol = get[3][1]
                    CurNode = self.Buttons[CurRow][CurCol]
                    if self.Colorb(CurNode) != "#ff0000" and self.Colorb(CurNode) != "#00ff00":
                        CurNode.setStyleSheet("background-color: thistle;")
                        OpenNode=OpenNode+1
                self.atNodes_lbl.setText(str(OpenNode+2))
                row = self.Drow
                col = self.Dcolumn

                rout=[]
                while self.Buttons[row][col] != self.SourceNode:
                    rout.append(self.Buttons[row][col].pre[0])
                    row,col = self.Buttons[row][col].pre[1],self.Buttons[row][col].pre[2]
                rout.pop()
                rout.reverse()
                for j in rout:
                    j.setStyleSheet("background-color: aqua;")
                    j.setText(str(s))
                    s=s+1

            else:
                QMessageBox.about(self, "Error", "Please Select Source and Destination!")
                return
            end = time.time()
            self.atTime_lbl.setText(str(round(1000*(end-start)))+" ms")
        self.Search_btn.setEnabled(False)
        self.Undo_btn.setEnabled(True)

    def Calh(self,row,col):
        a = abs(row - self.Drow)
        b = abs(col - self.Dcolumn)
        if a<0:
            a=0
        if b < 0:
            b=0
        r = a ** 2 + b ** 2
        return r

    def AChild(self,Node,row,col):
        res=[]
        if self.Colorb(self.Buttons[row-1][col]) == "#ffffff" or self.Colorb(self.Buttons[row-1][col]) == "#ff0000":
            res.append((self.Buttons[row-1][col],row-1,col))
            self.Buttons[row-1][col].pre = (Node,row,col)
        if self.Colorb(self.Buttons[row][col+1]) == "#ffffff" or self.Colorb(self.Buttons[row][col+1]) == "#ff0000":
            res.append((self.Buttons[row][col+1],row,col+1))
            self.Buttons[row][col+1].pre = (Node, row, col)
        if self.Colorb(self.Buttons[row+1][col]) == "#ffffff" or self.Colorb(self.Buttons[row+1][col]) == "#ff0000":
            res.append((self.Buttons[row+1][col],row+1,col))
            self.Buttons[row+1][col].pre = (Node, row, col)
        if self.Colorb(self.Buttons[row][col-1]) == "#ffffff" or self.Colorb(self.Buttons[row][col-1]) == "#ff0000":
            res.append((self.Buttons[row][col-1],row,col-1))
            self.Buttons[row][col-1].pre = (Node, row, col)
        return res

    def Edit_Alg(self):
        for row in range(1,self.rows-1):
            for column in range(1,self.columns-1):
                self.Buttons[row][column].status = ""
                self.Buttons[row][column].pre = ""
                if self.Colorb(self.Buttons[row][column]) == "#d8bfd8" or self.Colorb(self.Buttons[row][column]) == "#00ffff":
                    self.Buttons[row][column].setStyleSheet(self.Styles["White"])
                    self.Buttons[row][column].setText("")
        self.Search_btn.setEnabled(True)

    def Colorb(self,btn):
        return btn.palette().window().color().name()

app = QtWidgets.QApplication(sys.argv)
Searchtest = Search()
app.exec_()
