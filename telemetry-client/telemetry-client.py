from dashboard import Dashboard
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import math
import sys
import glob
import serial
import serial.tools.list_ports
import qdarkstyle
import Games.ets2


#
# Widgets
#

class SerialGroupBox(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.isLock = False
        self.port = None
        self.createUi()

    def createUi(self):
        self.layout = QHBoxLayout(self)
        self.setTitle("Dashboard")

        self.portLabel = QLabel(self)
        self.portLabel.setText("Port:")
        self.layout.addWidget(self.portLabel, 1) 

        self.portComboBox = QComboBox(self)
        self.portComboBox.currentIndexChanged.connect(self.onPortChange)
        self.layout.addWidget(self.portComboBox, 3) 

        self.connectButton = QPushButton(self)
        self.connectButton.setText("Connect")
        self.layout.addWidget(self.connectButton, 1) 
        
        self.setLayout(self.layout)

        self.portRefresh()

    def portRefresh(self):
        self.portComboBox.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.portComboBox.addItem(port.device, port)

    def onPortChange(self, index):
        self.port = self.portComboBox.itemData(index)
        pass

    def lock(self):
        self.portLabel.setDisabled(True)
        self.portComboBox.setDisabled(True)
        self.isLock = True

    def unlock(self):
        self.portLabel.setDisabled(False)
        self.portComboBox.setDisabled(False)
        self.isLock = False

class GameGroupBox(QGroupBox):
    games = [
        ("Euro Truck Symulator 2 (ets2-telemetry-udp)", Games.ets2.GameWidget),
        ("American Truck Simulator (ets2-telemetry-udp)", Games.ets2.GameWidget)
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.isLock = False
        self.createUi()

    def createUi(self):
        self.layout = QVBoxLayout(self)
        self.setTitle("Game")

        self.gameComboBox = QComboBox(self)
        self.gameComboBox.currentIndexChanged.connect(self.onGameChange)
        self.layout.addWidget(self.gameComboBox, 1)

        self.hline = QFrame(self)
        self.hline.setFrameShape(QFrame.HLine)
        self.layout.addWidget(self.hline, 1)

        self.gameWidgetStack = QStackedWidget(self)
        self.layout.addWidget(self.gameWidgetStack, 5)

        self.setLayout(self.layout)
        self.gamesRefresh()

    def gamesRefresh(self):
        for i in range(self.gameWidgetStack.count()):
            self.gameWidgetStack.removeWidget(self.gameWidgetStack.widget(i))

        self.gameComboBox.clear()
        for game in self.games:
            self.gameComboBox.addItem(game[0])
            self.gameWidgetStack.addWidget(game[1](self.parent().dashboard, self))
        
    def onGameChange(self, index):
        oldWidget = self.gameWidgetStack.currentWidget()
        if oldWidget is not None:
            oldWidget.close()
        
        self.gameWidgetStack.setCurrentIndex(index)
        pass

#
# E90Dashboard window
#

class E90Dashboard(QMainWindow):
    WINDOW_WIDTH = 400
    WINDOW_HEIGHT = 300
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dashboard = Dashboard()
        self.createUi()

        self.dashboardUpdateTimer = QTimer(self)
        self.dashboardUpdateTimer.setInterval(5)
        self.dashboardUpdateTimer.timeout.connect(self.updateDashboard)
        
    def createUi(self):
        #
        # Main window
        #
        self.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.setWindowTitle("E90 Dashboard")
        self.setMaximumSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.setMinimumSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)

        #
        # Layouts
        #
        self.mainlayout = QVBoxLayout(self)

        #
        # Dashboard
        #
        self.serialGroupBox = SerialGroupBox(self)
        self.serialGroupBox.connectButton.pressed.connect(self.onConnectButtonPress)
        self.mainlayout.addWidget(self.serialGroupBox)

        #
        # Game
        #
        self.gameGroupBox = GameGroupBox(self)
        self.mainlayout.addWidget(self.gameGroupBox)

        #
        # Apply
        #
        self.widget.setLayout(self.mainlayout)

    def onConnectButtonPress(self):
        if (self.serialGroupBox.port is not None) and (not self.dashboard.isOpen()):
            self.connect()
        else:
            self.disconnect()
        pass

    def connect(self):
        self.dashboard.open(self.serialGroupBox.port.device)
        self.serialGroupBox.connectButton.setText("Disconnect")
        self.dashboardUpdateTimer.start()
        self.serialGroupBox.lock()

    def disconnect(self):
        self.dashboard.close()
        self.serialGroupBox.connectButton.setText("Connect")
        self.dashboardUpdateTimer.stop()
        self.serialGroupBox.unlock()

    def updateDashboard(self):
        if self.dashboard.isOpen():
            try:
                self.dashboard.update()
            except serial.serialutil.SerialTimeoutException as e:
                QMessageBox.critical(self, "Error", "Dashboard: " + str(e))
                self.disconnect()

#
# Main
#

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    e90Dashboard = E90Dashboard()
    e90Dashboard.show()
    sys.exit(app.exec_())

