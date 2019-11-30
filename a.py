import sys
import csv
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from pyqtgraph import PlotWidget, plot
from scipy.interpolate import interp1d
import pyqtgraph as pg
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MainTab(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.title = 'Task 1'
        self.left = 0
        self.top = 0
        self.width = 400
        self.height = 500

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.createMenus()

        self.layout = QVBoxLayout(self)
        self.model = QStandardItemModel(self)

        self.tableView = QTableView(self)
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.scatterPointsBtn = QPushButton(self)
        self.scatterPointsBtn.setText("Plot scatter points")
        self.scatterPointsBtn.clicked.connect(self.onScatterPointsBtnClicked)

        self.scatterLinesBtn = QPushButton(self)
        self.scatterLinesBtn.setText("Plot scatter points with smooth lines")
        self.scatterLinesBtn.clicked.connect(self.onScatterLinesBtnClicked)

        self.linesBtn = QPushButton(self)
        self.linesBtn.setText("Plot scatter points with smooth lines")
        self.linesBtn.clicked.connect(self.onLinesBtnClicked)

        self.tabs = QTabWidget()
        self.tableTab = QWidget()

        self.tabs.resize(400, 500)

        self.tableTab.layout = QVBoxLayout()
        self.tableTab.layout.addWidget(self.tableView)
        self.tableTab.layout.addWidget(self.scatterPointsBtn)
        self.tableTab.layout.addWidget(self.scatterLinesBtn)
        self.tableTab.layout.addWidget(self.linesBtn)
        self.tableTab.setLayout(self.tableTab.layout)
        self.tabs.addTab(self.tableTab, "Table")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.setCentralWidget(self.tabs)
        self.show()

    def createMenus(self):
        loadDataAction = QAction("&Load data", self,
                                 shortcut="Ctrl+L",
                                 triggered=self.onLoadDataActionClicked)
        addDataAction = QAction("&Add data", self,
                                shortcut="Ctrl+A",
                                triggered=self.onAddDataActionClicked)
        saveAsAction = QAction("&Save as", self,
                               shortcut="Ctrl+S",
                               triggered=self.onSaveAsActionClicked)

        editDataAction = QAction("&Edit data", self,
                                 shortcut="Ctrl+E",
                                 triggered=self.onEditDataActionClicked)

        fileMenu = QMenu("&File", self)
        fileMenu.addAction(loadDataAction)
        fileMenu.addAction(addDataAction)
        fileMenu.addSeparator()
        fileMenu.addAction(saveAsAction)

        editMenu = QMenu("&Edit", self)
        editMenu.addAction(editDataAction)

        self.menuBar().addMenu(fileMenu)
        self.menuBar().addMenu(editMenu)

    def onLoadDataActionClicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            with open(fileName, "r") as fileInput:
                for row in csv.reader(fileInput):
                    items = [
                        QStandardItem(field)
                        for field in row
                    ]
                    self.model.appendRow(items)

    def onAddDataActionClicked(self):
        print("Hello")

    def onSaveAsActionClicked(self):
        print("Saved")
        fileFormat = 'png'
        initialPath = QDir.currentPath() + 'untitled.' + fileFormat
        fileName, _ = QFileDialog.getSaveFileName(self, "Save As",
                                                  initialPath, "%s Files (*.%s);; All Files (*)" %
                                                  (fileFormat.upper(), fileFormat))
        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(self.newTab.winId())
        screenshot.save(fileName, fileFormat)

    def onEditDataActionClicked(self):
        self.tableView.setEditTriggers(QAbstractItemView.SelectedClicked)

    def onScatterPointsBtnClicked(self):
        number = 1
        values = []
        for index in self.tableView.selectedIndexes():
            values.append(index.data())

        self.newTab = MyNewTab(self, values, number)
        self.tabs.addTab(self.newTab, "Scatter Points Tab")

    def onScatterLinesBtnClicked(self):
        number = 3
        values = []
        for index in self.tableView.selectedIndexes():
            values.append(index.data())

        self.newTab = MyNewTab(self, values, number)
        self.tabs.addTab(self.newTab, "Scatter Lines Tab")

    def onLinesBtnClicked(self):
        number = 3
        values = []
        for index in self.tableView.selectedIndexes():
            values.append(index.data())

        self.newTab = MyNewTab(self, values, number)
        self.tabs.addTab(self.newTab, "Lines Tab")


class MyNewTab(QWidget):
    def __init__(self, parent, values, number):
        super(MyNewTab, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.myNewTab = QWidget()
        self.myNewTab.layout = QVBoxLayout(self)

        if number == 1:
            self.tab1(values)
        elif number == 2:
            self.tab2(values)
        elif number == 3:
            self.tab3(values)

    def tab1(self, values):
        print("Tab 1")
        x = []
        y = []
        for i in range(len(values)):
            if i % 2 == 0:
                x.append(int(values[i]))
            else:
                y.append(int(values[i]))
        x = np.array(x)
        y = np.array(y)
        view = pg.GraphicsLayoutWidget()
        view.setBackground('w')
        w1 = view.addPlot(title="Scatter points plot", labels={'left': "Y-axis", 'bottom': "X-axis"})
        s1 = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 0, 255, 120))
        s1.addPoints(x, y)

        w1.addItem(s1)

        self.layout.addWidget(view)
        self.layout.addWidget(self.myNewTab)
        self.setLayout(self.myNewTab.layout)

    def tab2(self, values):
        print("tab2")

    def tab3(self, values):
        print("Tab 3")
        x = []
        y = []
        for i in range(len(values)):
            if i % 2 == 0:
                x.append(int(values[i]))
            else:
                y.append(int(values[i]))
        x = np.array(x)
        y = np.array(y)

        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground('w')
        pen = pg.mkPen(color=(255, 0, 0))
        self.graphWidget.plot(x, y, pen=pen)

        self.graphWidget.setTitle("Lines Plot")
        self.graphWidget.setLabel('left', 'Y-axis', size=20)
        self.graphWidget.setLabel('bottom', 'X-axis', size=20)

        self.layout.addWidget(self.graphWidget)

        self.layout.addWidget(self.myNewTab)
        self.setLayout(self.myNewTab.layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainTab()
    sys.exit(app.exec_())

