from tkinter import *
from tkinter import ttk
from SerialRadarPlotter import get_serial_list, SerialRadarPlotter
from threading import Thread

serial_ports = []
SRP = None

def get_ports(): # get list of serial ports
    global serial_ports, ports
    names = []
    portInfo = get_serial_list()
    for portI in portInfo:
        serial_ports.append(portI)
        names.append(portI.name)
    ports.config(values=names)

def connect(event): #connect to radar and start ploting
    global serial_ports, ports, SRP, redZEntry, sensorMaxEntry
    name = ports.get()
    print(name)
    sp = None
    for portI in serial_ports:
        if portI.name == name:
            sp = portI
    try:
        SRP = SerialRadarPlotter(sp, float(sensorMaxEntry.get()), "1", float(redZEntry.get()))
        thread = Thread(target=(SRP.run())) # create new thread and start ploting in it,
        thread.run()
    except Exception as e:
        print(e)

def GraphExit(): #exit
    global SRP
    if (SRP != None):
        SRP.stop()
    exit(0)


root = Tk()
root.title("SerialRadarPlotter")
root.geometry("300x150")

redZLabel = Label(text="RedZone (in cm):")
redZLabel.pack()

redZEntry = Entry() #redZone entry in cm
redZEntry.pack()

sensorMaxLabel = Label(text="SensorMax (in cm):")
sensorMaxLabel.pack()

sensorMaxEntry = Entry() #sensor max entry in cm
sensorMaxEntry.pack()

search_port_bt = Button(text='Get Ports', command=get_ports) # search ports
search_port_bt.pack()

ports = ttk.Combobox(values=serial_ports) # user select port, then this programm connect to it and plot
ports.bind("<<ComboboxSelected>>", connect)
ports.pack()

close_bt = Button(text='Exit', command=GraphExit) #exit button
close_bt.pack()
root.mainloop()