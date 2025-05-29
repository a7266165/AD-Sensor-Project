# led_controller.py - LED控制模組

import time
import serial
import serial.tools.list_ports
from PyQt6 import QtCore


def find_arduino_port():
    """搜尋Arduino連接埠"""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "Arduino" in port.description or "CH340" in port.description:
            return port.device
    return None


class LEDController:
    """Arduino LED控制器"""

    def __init__(self, port, baudrate=9600, timeout=2):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

    def _send_command(self, command: bytes):
        """發送命令到Arduino"""
        try:
            with serial.Serial(self.port, self.baudrate, timeout=self.timeout) as ser:
                time.sleep(2)  # Allow Arduino to reset
                ser.write(command + b"\n")
        except serial.SerialException as e:
            print(f"無法開啟串列埠 {self.port}: {e}")

    def flash_three_times(self):
        """閃爍白光3次"""
        self._send_command(b"flash_white_light_3_times")

    def cycle_led(self):
        """LED循環3次"""
        self._send_command(b"LED_cycle_3_times")


class LEDWorker(QtCore.QThread):
    """LED控制子執行緒"""

    finished = QtCore.pyqtSignal()

    def __init__(self, led_ctrl: LEDController):
        super().__init__()
        self.led_ctrl = led_ctrl

    def run(self):
        """執行LED控制序列"""
        # 先閃爍 3 次，再 cycle
        self.led_ctrl.flash_three_times()
        time.sleep(3)
        self.led_ctrl.cycle_led()
        self.finished.emit()
