from PyQt5 import QtWidgets, uic, QtCore, QtGui,QtSerialPort
import sys
import numpy as np
import pyqtgraph as pg
import pathlib
from scipy import signal
from datawindow import sepWidget, PlotArea
from pyqtspinner.spinner import WaitingSpinner
import serial.tools.list_ports

class listWidget(QtWidgets.QWidget):
    def __init__(self,name,subname):
        super(listWidget, self).__init__()
        widgetitemfile = pathlib.Path(__file__).parent.absolute() / 'widgetitem.ui'
        uic.loadUi(widgetitemfile, self)
        self.name_1.setText(name)
        self.name_2.setText(subname)
class Ui(QtWidgets.QWidget):
    def animsearch(self):
        self.searchlbl.setVisible(True)
        self.findBoard.start()
        QtCore.QTimer.singleShot(2000,self.search)
    def search(self):
        self.listWidget.clear()
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            item  = QtGui.QListWidgetItem()
            dougui = listWidget(p[0],p[1])
            item.setSizeHint(QtCore.QSize(self.listWidget.width(),40)) 
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item,dougui)
        self.findBoard.stop()
        self.searchlbl.setVisible(False)   
    def maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
    def minimize(self):
        self.showMinimized()
    def StayonTop(self,checked):
        if checked:
            self.setWindowFlags(self.windowFlags()| QtCore.Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.show()
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonPress and obj==self.pushButton_16:
            self.oldPos = event.globalPos()
        elif event.type() == QtCore.QEvent.Wheel:
            if self.dataPlot_1.innerWidget.underMouse() or self.dataPlot_2.innerWidget.underMouse() or self.dataPlot_3.innerWidget.underMouse() or self.dataPlot_4.innerWidget.underMouse() or self.response_plot_1.innerWidget.underMouse() or self.response_plot_2.innerWidget.underMouse() or self.response_plot_3.innerWidget.underMouse() or self.response_plot_4.innerWidget.underMouse():
                return True
        elif event.type() == QtCore.QEvent.MouseMove and obj==self.pushButton_16:
            delta = QtCore.QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
        return QtWidgets.QWidget.eventFilter(self, obj, event)
    def Cleared(self):
        self.dislocation = []
        self.time = []
    def ReceiveData(self):
        while self.arduino.canReadLine():
            if self.dataignore<200:
                self.dataignore +=1
            else:
                try:
                    text = self.arduino.readLine().data().decode()
                    text = text.rstrip('\r\n')
                except:
                    continue
                else:
                    x = text.split(',')
                    try:
                        self.time = np.append(self.time,int(x[0])/1000)
                        self.dislocation = np.append(self.dislocation,float(x[1]))
                        self.dataPlot_1.updatedata(self.dislocation,self.time)
                        self.dataPlot_2.updatedata(self.dislocation,self.time)
                        self.dataPlot_3.updatedata(self.dislocation,self.time)
                        self.dataPlot_4.updatedata(self.dislocation,self.time)
                    except:
                        continue
    def Connect(self):
        self.arduino.open(QtSerialPort.QSerialPort.ReadOnly)
        self.arduino.clear()
        self.stopbtn.setEnabled(True)
        self.startbtn.setEnabled(False)
    def Close_ard(self):
        self.arduino.close()
        self.stopbtn.setEnabled(False)
        self.startbtn.setEnabled(True)
    def change_btn_ui(self,index):
        if index == 0:
            self.board_btn.setChecked(True)
        elif index == 1:
            self.data_btn.setChecked(True)
        elif index == 2:
            self.vib_btn.setChecked(True)
        elif index == 3:
            self.pi_btn.setChecked(True)
    def change_to_analysis_ui(self, item):
        self.startbtn.setEnabled(True)
        self.stopbtn.setEnabled(True)
        self.checkBox.setEnabled(True)
        self.stackedWidget.setCurrentIndex(1)
        self.arduino = QtSerialPort.QSerialPort(
                self.listWidget.itemWidget(item).name_1.text(),
                baudRate=QtSerialPort.QSerialPort.Baud9600
                )
        self.arduino.readyRead.connect(self.ReceiveData)
    def __init__(self):
        super(Ui, self).__init__()
        MainUiFile = pathlib.Path(__file__).parent.absolute() / 'MainWindow.ui'
        uic.loadUi(MainUiFile, self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.findBoard = WaitingSpinner(self.Spinner,centerOnParent=True,roundness=100.0, opacity=100.0,fade=70.0, radius=4.0, lines=50,line_length=5.0, line_width=1.0,speed=1.5, color=(235, 167, 99))
        self.refreshbtn.clicked.connect(self.animsearch)
        self.searchlbl.setVisible(False)

        self.listWidget.itemDoubleClicked.connect(self.change_to_analysis_ui)
        self.stackedWidget.currentChanged.connect(self.change_btn_ui)
        self.dataignore = 0
    #:::Connecting Slots 
        self.exitbtn.clicked.connect(lambda x: app.exit())
        self.maximizebtn.clicked.connect(self.maximize)
        self.minibtn.clicked.connect(self.minimize)
        self.stontopbtn.clicked.connect(self.StayonTop)
        self.stopbtn.clicked.connect(self.Close_ard)
        self.board_btn.clicked.connect(lambda x: self.stackedWidget.setCurrentIndex(0))
        self.data_btn.clicked.connect(lambda x: self.stackedWidget.setCurrentIndex(1))
        self.vib_btn.clicked.connect(lambda x: self.stackedWidget.setCurrentIndex(2))
        self.pi_btn.clicked.connect(lambda x: self.stackedWidget.setCurrentIndex(3))
        self.sld_smooth.valueChanged.connect(lambda x: self.lbl_smooth.setText(str(x)))
        
        self.dataPlot_1 = PlotArea('Data Plot - Sensor 1')
        self.dataPlot_1.ApplySignal(self.Cleared)
        self.verticalLayout_14.addWidget(self.dataPlot_1.innerWidget)
        self.dataPlot_2 = PlotArea('Data Plot - Sensor 2')
        self.dataPlot_2.ApplySignal(self.Cleared)
        self.verticalLayout_14.addWidget(self.dataPlot_2.innerWidget)
        self.dataPlot_3 = PlotArea('Data Plot - Sensor 3')
        self.dataPlot_3.ApplySignal(self.Cleared)
        self.verticalLayout_14.addWidget(self.dataPlot_3.innerWidget)
        self.dataPlot_4 = PlotArea('Data Plot - Sensor 4')
        self.dataPlot_4.ApplySignal(self.Cleared)
        self.verticalLayout_14.addWidget(self.dataPlot_4.innerWidget)

        self.response_plot_1 = PlotArea('System Response - Sensor 1')
        self.verticalLayout_23.addWidget(self.response_plot_1.innerWidget)
        self.response_plot_2 = PlotArea('System Response - Sensor 2')
        self.verticalLayout_23.addWidget(self.response_plot_2.innerWidget)
        self.response_plot_3 = PlotArea('System Response - Sensor 3')
        self.verticalLayout_23.addWidget(self.response_plot_3.innerWidget)
        self.response_plot_4 = PlotArea('System Response - Sensor 4')
        self.verticalLayout_23.addWidget(self.response_plot_4.innerWidget)

        self.pitchbtn.clicked.connect(self.ChangeCarModel)
        self.rollbtn.clicked.connect(self.ChangeCarModel)
        self.fullbtn.clicked.connect(self.ChangeCarModel)

        self.startbtn.clicked.connect(self.Connect)
        #::: -> Sliders values
        self.kfl_sld.valueChanged.connect(lambda x: self.kfl_lbl.setText(str(x)+' N/m'))
        self.kfr_sld.valueChanged.connect(lambda x: self.kfr_lbl.setText(str(x)+' N/m'))
        self.krr_sld.valueChanged.connect(lambda x: self.krr_lbl.setText(str(x)+' N/m'))
        self.krl_sld.valueChanged.connect(lambda x: self.krl_lbl.setText(str(x)+' N/m'))

        self.dfl_sld.valueChanged.connect(lambda x: self.dfl_lbl.setText(str(x)+' N.s/m'))
        self.dfr_sld.valueChanged.connect(lambda x: self.dfr_lbl.setText(str(x)+' N.s/m'))
        self.drr_sld.valueChanged.connect(lambda x: self.drr_lbl.setText(str(x)+' N.s/m'))
        self.drl_sld.valueChanged.connect(lambda x: self.drl_lbl.setText(str(x)+' N.s/m'))

        self.time = []
        self.dislocation = []
    #::: Filtering and Events
        self.pushButton_16.installEventFilter(self)

        self.scrollArea.viewport().installEventFilter(self)
        self.scrollArea_2.viewport().installEventFilter(self)
        self.oldPos = self.pos()

        self.show()

    def ChangeCarModel(self):
        Toggle = [True, True, True, True, True, True, True, True]
        Slider = [self.kfl_sld, self.kfr_sld, self.krl_sld, self.krr_sld, self.dfl_sld, self.dfr_sld, self.drl_sld, self.drr_sld]
        if self.sender() == self.pitchbtn:
            Toggle[1] = False
            Toggle[3] = False
            Toggle[5] = False
            Toggle[7] = False
        if self.sender() == self.rollbtn:
            Toggle[2] = False
            Toggle[3] = False
            Toggle[6] = False
            Toggle[7] = False
        i = 0
        for x in Slider:
            x.setEnabled(Toggle[i])
            i = i + 1

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_() 
