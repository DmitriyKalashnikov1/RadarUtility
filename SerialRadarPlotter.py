import serial.tools.list_ports as list_ports
import serial
from serial import SerialException
from serial.tools.list_ports_common import ListPortInfo
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors
import numpy as np
import sys

def get_serial_list() -> list: # get serial port list
    return list_ports.comports()

class SerialRadarPlotter:
    # packet format for this radar plotter: [angle,dist/n]
    # dist > renZone and <= sensormax ---> sensor see something in a range, yellow line in a graph
    # dist > renZone and > sensormax ---> sensor doesn't see something in a range, green line in a graph
    # dist < renZone ---> danger dist, red line in a graph
    running = True
    def __init__(self, port_info:ListPortInfo, sensorMax: float, name:str, redzone:float): #open serial port and graph window
        self.port = serial.Serial(port_info.name,  baudrate=9600)
        self.sensormax = sensorMax
        self.redZone = redzone
        self.fig = plt.figure(figsize=(9, 9))
        self.fig.suptitle(f"Radar: {name}")
        self.ax = self.fig.add_subplot(111, polar=True)
        #self.ax.set_ymargin(0.1)
        plt.axis()
        try:
            self.port.open()
        except SerialException as e:
            print(e)
    def __animate__(self, i):
        # parse data from radar
        if (self.running):
            inputData = str(self.port.readline(), "ascii") #read and trasform bytes to str
            inputData = inputData.split(",") # split angle and dist
            inputData = [int(inputData[0]), int(inputData[1])] # toInt
            # plot data
            w = 2*np.pi / 180 # set width to 1 grad

            if ((np.radians(inputData[0])==0) or (np.radians(inputData[0])==np.pi)):
                self.ax.clear() # clear graph
            # dist > renZone and <= sensormax ---> sensor see something in a range
            # dist > renZone and > sensormax ---> sensor doesn't see something in a range
            # dist < renZone ---> danger dist
            if ((inputData[1] > self.redZone) and (inputData[1] <= self.sensormax)):
                self.ax.bar(x=np.radians(270), height=self.sensormax, width=w, color=mcolors.BASE_COLORS["w"])
                self.ax.bar(x=np.radians(inputData[0]), height=inputData[1], width=w, color=mcolors.BASE_COLORS["y"]) # plot new data
            elif ((inputData[1] > self.redZone) and (inputData[1] > self.sensormax)):
                self.ax.bar(x=np.radians(270), height=self.sensormax, width=w, color=mcolors.BASE_COLORS["w"])
                self.ax.bar(x=np.radians(inputData[0]), height=inputData[1], width=w,color=mcolors.BASE_COLORS["g"])  # plot new data
            else:
                self.ax.bar(x=np.radians(270), height=self.sensormax, width=w, color=mcolors.BASE_COLORS["w"])
                self.ax.bar(x=np.radians(inputData[0]), height=inputData[1], width=w, color=mcolors.BASE_COLORS["r"])  # plot new data


    def run(self):
        #plot data from radar
        anim = animation.FuncAnimation(self.fig, self.__animate__) #draw graphic
        plt.show()

    def stop(self):
        # stop animation, close port and window
        self.running = False
        self.port.close()
        plt.close(self.fig)


#This program can work it self. This is CLI
if __name__ == "__main__":
    ports = get_serial_list() # get list of ports
    print("Index|Port name")
    for index, portI in enumerate(ports):
        print(f'{index}|{portI.name}')
    selectPort = int(input("Select port index: "))
    if ((selectPort < 0) or (selectPort > len(ports) )):
        print("Invalid index")
        exit(0)
    redZone = input("Input RedZone (in cm): ")
    sensorMax = input("Input SensorMax (in cm): ")
    stack = SerialRadarPlotter(ports[selectPort], float(sensorMax), "1", float(redZone))
    try:
        stack.run()
    finally:
        stack.stop()