import serial
import serial.tools.list_ports
import time

def find_arduino_ports():
    ports = serial.tools.list_ports.comports()

    arduino_ports = [port.device for port in ports if 'Arduino' in port.description or 'CH340' in port.description]

    return arduino_ports

def flash_white_light_3_times(port):
    try:
        with serial.Serial(port, 9600, timeout=2) as ser:
            time.sleep(2)  # 給 Arduino 一點時間來重置和準備接收數據，不能刪！！！
            ser.write(b'flash_white_light_3_times\n')
    except serial.SerialException as e:
        print(f"無法開啟串列埠 {port}: {e}")

def LED_cycle_3_times(port):
    try:
        with serial.Serial(port, 9600, timeout=2) as ser:
            time.sleep(2)  # 給 Arduino 一點時間來重置和準備接收數據，不能刪！！！
            ser.write(b'LED_cycle_3_times\n')
    except serial.SerialException as e:
        print(f"無法開啟串列埠 {port}: {e}")


if __name__ == "__main__":
    ports = find_arduino_ports()
    if not ports:
        print("找不到任何包含 'Arduino' 的串列埠。")
    else:
        print("找到以下可能是 Arduino 的串列埠：")
        for port in ports:
            print(port)
        if ports:
            flash_white_light_3_times(ports[0])
            # time.sleep(5)
            # LED_cycle_3_times(ports[0])
