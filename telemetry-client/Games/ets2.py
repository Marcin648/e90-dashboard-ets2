from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from dashboard import Dashboard
import GamesTelemetry.EtsTelemetryClient

class UpdateThread(QThread):
    errorSignal = pyqtSignal((str,))

    def __init__(self, dashboard: Dashboard, ip, port, parent=None):
        super().__init__(parent)
        self.ip = ip
        self.port = port
        self.isWorking = True
        self.dashboard = dashboard
        self.telemetry = GamesTelemetry.EtsTelemetryClient.Client()
    
    def __del__(self):
        self.isWorking = False
        self.wait()

    def run(self):
        self.telemetry.connect(self.ip, self.port)

        while(self.isWorking):
            try:
                self.telemetry.update()
            except Exception as e:
                self.errorSignal.emit("Game telemetry: " + str(e))
                self.isWorking = False
                break

            self.dashboard._Dashboard__lock.acquire()
            self.dashboard.ignition = self.telemetry.truck.engine_enabled
            self.dashboard.parking_lights = self.telemetry.truck.light_parking
            self.dashboard.dipped_lights = self.telemetry.truck.light_low_beam
            self.dashboard.main_lights = self.telemetry.truck.light_high_beam
            self.dashboard.fog_lights = self.telemetry.truck.light_aux_front or self.telemetry.truck.light_aux_roof
            if self.telemetry.truck.light_lblinker and self.telemetry.truck.light_rblinker:
                self.dashboard.blinkers = Dashboard.BLINKERS_HAZZARD
            else:
                if self.telemetry.truck.light_lblinker:
                    self.dashboard.blinkers = Dashboard.BLINKERS_LEFT
                elif self.telemetry.truck.light_rblinker:
                    self.dashboard.blinkers = Dashboard.BLINKERS_RIGHT
                else:
                    self.dashboard.blinkers = Dashboard.BLINKERS_OFF

            self.dashboard.handbrake = self.telemetry.truck.parking_brake
            self.dashboard.RPM = self.telemetry.truck.engine_rpm
            self.dashboard.speed = self.telemetry.truck.speed * 3.6

            if self.telemetry.config_truck.fuel_capacity > 0.0:
                self.dashboard.fuel = (self.telemetry.truck.fuel / self.telemetry.config_truck.fuel_capacity) * 1000

            self.dashboard.hour = 0
            self.dashboard.minute = 0
            self.dashboard.second = 0
            self.dashboard.day = 1
            self.dashboard.month = 1
            self.dashboard.year = 2019
            self.dashboard._Dashboard__lock.release()

        self.telemetry.close()
        self.quit()

class GameWidget(QWidget):
    def __init__(self, dashboard: Dashboard, parent=None):
        super().__init__(parent)
        self.dashboard = dashboard
        self.isConnect = False
        self.ip = "127.0.0.1"
        self.port = 23444
        self.createUi()
        self.updateThread = UpdateThread(self.dashboard, self.ip, self.port, self)

    def createUi(self):
        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        self.ipLabel = QLabel(self)
        self.ipLabel.setText("IP:")
        self.layout.addWidget(self.ipLabel, 1)

        self.ipEditBox = QLineEdit(self)
        self.ipEditBox.setText(self.ip)
        self.layout.addWidget(self.ipEditBox, 3)

        self.portLabel = QLabel(self)
        self.portLabel.setText("Port:")
        self.layout.addWidget(self.portLabel, 1)

        self.portEditBox = QLineEdit(self)
        self.portEditBox.setText(str(int(self.port)))
        self.portEditBox.setValidator(QIntValidator())
        self.layout.addWidget(self.portEditBox, 2)

        self.connectButton = QPushButton(self)
        self.connectButton.setText("Connect")
        self.connectButton.pressed.connect(self.onConnectButtonPress)
        self.layout.addWidget(self.connectButton, 1)

        self.setLayout(self.layout)

    def errorMessage(self, message):
        QMessageBox.critical(None, "Error", message)

    def onConnectButtonPress(self):
        self.ip = self.ipEditBox.text()
        self.port = int(self.portEditBox.text())

        if self.isConnect:
            self.disconnect()
        else:
            self.connect()

    def connect(self):
        self.ipLabel.setDisabled(True)
        self.ipEditBox.setDisabled(True)
        self.portLabel.setDisabled(True)
        self.portEditBox.setDisabled(True)
        self.connectButton.setText("Disconnect")
        self.isConnect = True
        self.updateThread = UpdateThread(self.dashboard, self.ip, self.port, self)
        self.updateThread.finished.connect(self.disconnect)
        self.updateThread.errorSignal.connect(self.errorMessage)
        self.updateThread.start()

    def disconnect(self):
        self.ipLabel.setDisabled(False)
        self.ipEditBox.setDisabled(False)
        self.portLabel.setDisabled(False)
        self.portEditBox.setDisabled(False)
        self.connectButton.setText("Connect")
        self.isConnect = False
        self.updateThread.isWorking = False
        self.updateThread.wait()
        
    def close(self):
        self.disconnect()
