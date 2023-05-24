import serial
import serial.tools.list_ports
import UI
from queue import Queue
from threading import Thread, Lock
from time import sleep

dataReceiveBuffer = Queue(maxsize=100)
ReceiveBuffer_lock = Lock()
port_list = list(serial.tools.list_ports.comports())
if len(port_list) == 0:
    print('无可用串口，不能开始')
for port in port_list:
    print(port[0])
    serialPort = port[0]
uart = serial.Serial(serialPort, 115200, timeout=0.5)

class UartReceiveThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while UI.quitApplication == 0:
            data = uart.read_all()
            n = len(data)
            if n > 0:
                strbuf = "------ReceiveThread------ " + str(data)
                UI.my_print(strbuf)
				
                ReceiveBuffer_lock.acquire()
                for i in range(n):
                    if dataReceiveBuffer.qsize() < dataReceiveBuffer.maxsize:
                        dataReceiveBuffer.put(data[i])
                    else :
                        print("dataReceiveBuffer overflow")
                ReceiveBuffer_lock.release()
            sleep(0.001)

        uart.close()
        print("UartReceiveThread quit")
      