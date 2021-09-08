import threading
import time
from tkinter import *
from tkinter import messagebox

import keyboard
import pyautogui
import win32api
import win32con
import win32gui
from pyautogui import *

# Variables
active = True

def on_closing():
    global active
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        active = False
        root.destroy()
        raise SystemExit(0)

class ClickPosition:
        x = 0
        y = 0
        time = 0
class Color:
    r = None
    g = None
    b = None
    color = None
# Click functions, will click where x and y are set
def leftClick ():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.001) # Pause script for 0.001 seconds for mouse down to register
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def rightClick ():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
    time.sleep(0.001) # Pause script for 0.001 seconds for mouse down to register
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)

# Spam button
def clickMouse(clickType, clickSpeed):
    # Right or left click depending on setting
    if (clickType == 0): leftClick()
    elif (clickType == 1): rightClick()
    # Wait for the time specified
    time.sleep(clickSpeed)

# Click mouse at preset positions
def clickPositions(clickType, clickPositions):
    # Loop through all positions
    for i in range(len(clickPositions)):
        # Set mouse to position
        win32api.SetCursorPos((clickPositions[i].x, clickPositions[i].y))
        leftClick()
        # # Right or left click depending on setting
        # if (clickType == 0): leftClick()
        # elif (clickType == 1): rightClick()
        # Wait for the time specified
        time.sleep(clickPositions[i].time)

def clickColors(clickType, colors, position, speed):
    pos = []
     # Convert tuples to just lists
    for i in range(2):
        pos.append([])
        pos[i].append(position[i][0])
        pos[i].append(position[i][1])

    # Swap x and y positions to correct sections
    # Swap x
    if (pos[0][0] < pos[1][0]): 
        temp = pos[0][0] # record lower x
        pos[0][0] = pos[1][0] # Set higher x
        pos[1][0] = temp # Set lower x
    # Swap y
    if (pos[0][1] < pos[1][1]): 
        temp = pos[0][1] #record lower y
        pos[0][1] = pos[1][1] # Set higher y
        pos[1][1] = temp # Set lower y

    flag = 0
    pic = pyautogui.screenshot(region=(pos[1][0], pos[1][1], pos[0][0]-pos[1][0], pos[0][1]-pos[1][1]))

    width, height = pic.size

    if (speed == 0): speed = 1
    for x in range(0, width, speed):
        for y in range(0, height, speed):
            current_color = pic.getpixel((x, y))
            for i in range(len(colors)):
                if (current_color == colors[i].color):
                    win32api.SetCursorPos((x+pos[1][0], y+pos[1][1]))
                    leftClick()
                    flag = 1
                    break
            if (flag == 1): break
        
        if (flag == 1): 
            break

def rgb2hex(r,g,b):
    return "#{:02x}{:02x}{:02x}".format(r,g,b)

class App:
    global active
    def __init__(self, root, title, geometry):
        threading.Thread.__init__(self)

        # Variables
        self.settingPosition = False
        self.settingColor = False
        self.currentSettingPosition = 0
        self.running = False
        self.clickTime = 0
        self.clickType = 0
        self.currentOption = 0
        self.positions = []
        self.maxPositionsLength = 7
        self.colors = []
        self.maxColorsLength = 6

        self.colorButtons = []
        self.colorLabels = []
        self.colorPositions = [[], []],[[], []]
        self.speed = 1
        self.settingColorPosition = False
        self.currentSettingColorButton = None
        self.colorPosButtons = [None]*2
        
        self.positionButtons = []
        self.positionLabels = []
        self.positionTime = [None]*self.maxPositionsLength

        # Set up 
        self.root = root
        self.root.title(title)
        self.root.geometry(geometry)
        self.root.resizable(0,0)

        main = threading.Thread(target=self.update, args=())
        main.setDaemon(True)
        self.monitorKeyboard = threading.Thread(target=self.monitorKeyboard, args=())
        self.monitorKeyboard.setDaemon(True)

        main.start()
        self.monitorKeyboard.start()

        self.screens()
        
        self.root.after(2999, self.monitorKeyboard)

    def update(self):
        print("Program Start")
        while (active):
            print('running')
            if (self.clickTime == None):
                self.clickTime = 0
            if (self.running):
                if (self.currentOption == 0):
                    pass
                elif (self.currentOption == 1):
                    clickMouse(self.clickType, float(self.clickTime.get()))
                elif (self.currentOption == 2):
                    clickPositions(self.clickType, self.positions)
                elif (self.currentOption == 3):
                    clickColors(self.clickType, self.colors, self.colorPositions, float(self.speed.get()))
            if (not self.monitorKeyboard.is_alive): self.monitorKeyboard.start()
            # pass


    def monitorKeyboard(self):
        while (active):
            print('also running')
            if (keyboard.is_pressed('alt+1') and not self.wasPressed):
                self.running = not self.running
            
            self.wasPressed = keyboard.is_pressed('alt+1')

            if (not self.running or self.currentOption == 0):
                self.running = False
                self.startButton['text'] = "Start"
            else:
                self.startButton['text'] = "Stop"

            # Check if currently waiting to get position
            if (self.settingPosition and keyboard.is_pressed('alt+0')):
                pos = win32gui.GetCursorPos()
                self.positions[self.currentSettingPosition].x = pos[0]
                self.positions[self.currentSettingPosition].y = pos[1]
                self.positionLabels[self.currentSettingPosition]['text'] = pos

                self.positionButtons[self.currentSettingPosition]['text'] = "Set pos"
                self.settingPosition = False
            if (self.settingColor and keyboard.is_pressed('alt+0')):
                pos = win32gui.GetCursorPos()
                pix = pyautogui.pixel(pos[0], pos[1])
                self.colors[self.currentSettingColor].r = pix[0]
                self.colors[self.currentSettingColor].g = pix[1]
                self.colors[self.currentSettingColor].b = pix[2]
                self.colors[self.currentSettingColor].color = pix
                self.colorLabels[self.currentSettingColor]['bg'] = rgb2hex(pix[0],pix[1],pix[2])

                self.colorButtons[self.currentSettingColor]['text'] = "Set color"
                self.settingColor = False
            if (self.settingColorPosition and keyboard.is_pressed('alt+0')):
                index = self.colorPosButtons.index(self.currentSettingColorButton)
                pos = win32gui.GetCursorPos()

                self.colorPositions[index][0] = pos[0]
                self.colorPositions[index][1] = pos[1]
                self.colorPosButtons[index]['text'] = pos

                self.settingColorPosition = False
            # self.root.after(100, self.monitorKeyboard)
            # pass
        
    def StartButton(self):
        self.running = not self.running

    def changeOption(self, int, frame):
        self.currentOption = int
        frame.tkraise()
        pass
    
    def switchClickType(self, button):
        if (button['text'] == "Left Click"):
            button['text'] = 'Right Click'
            self.clickType = 1
        elif (button['text'] == "Right Click"):
            button['text'] = 'Left Click'
            self.clickType = 0

    # Adding positions
    def setPosition(self, button):
        self.settingPosition = not self.settingPosition or self.currentSettingPosition != button
        self.currentSettingPosition = button

        for i in self.positionButtons:
            if (i != self.positionButtons[button] and i['text'] == "Stop"):
                i['text'] = "Set pos"

        if (self.positionButtons[button]['text'] == "Set pos"):
            self.positionButtons[button]['text'] = "Stop"
        elif (self.positionButtons[button]['text'] == "Stop"):
            self.positionButtons[button]['text'] = "Set pos"
        pass

    def addPosition(self, frame):
        if (len(self.positions) < self.maxPositionsLength):
            pos = ClickPosition()
            self.positions.append(pos)
            
            if (len(self.positions) <= 4):
                posx = 0
                posy = -25+len(self.positions)*50
            else:
                posx = 250
                posy = -25+((len(self.positions)-4)*50)

            Label(frame, bg='#9e9e9e').place(x=posx,y=posy, width= 210,height=55)

            Label(frame, bg='#9e9e9e', text="pos").place(x=posx+75,y=posy+5, width=75,height=15)
            Label(frame, bg='#9e9e9e', text="time").place(x=posx+130,y=posy+5, width=75,height=15)

            button = Button(frame, text="Set pos",font='Consolas 10 bold')
            self.positionButtons.append(button)
            self.positionButtons[self.positionButtons.index(button)].config(command=lambda:self.setPosition(self.positionButtons.index(button)))
            self.positionButtons[self.positionButtons.index(button)].place(x=posx+5,y=posy+5, width= 75,height=45)
            
            label = Label(frame, bg='#9e9e9e', text="x,y",font='Consolas 10 bold')
            self.positionLabels.append(label)
            self.positionLabels[self.positionLabels.index(label)].place(x=posx+88,y=posy+25, width= 50,height=25)

            # Validation
            vcmd = (frame.register(self.onValidate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

            self.positionTime[self.positionButtons.index(button)] = StringVar()
            time = Entry(frame, bg='#9e9e9e', text="0x0",font='Consolas 10 bold', validate='key', validatecommand=vcmd, textvariable=self.positionTime[self.positionButtons.index(button)])
            time.insert(0, '0')
            time.place(x=posx+142,y=posy+25, width= 50,height=25)

            pos.time = int(time.get())
    
    # Adding positions
    def setColor(self, button):
        self.settingColor = not self.settingColor or self.currentSettingColor != button
        self.currentSettingColor = button

        for i in self.colorButtons:
            if (i != self.colorButtons[button] and i['text'] == "Stop"):
                i['text'] = "Set color"

        if (self.colorButtons[button]['text'] == "Set color"):
            self.colorButtons[button]['text'] = "Stop"
        elif (self.colorButtons[button]['text'] == "Stop"):
            self.colorButtons[button]['text'] = "Set color"
        pass

    def addColor(self, frame):
        if (len(self.colors) < self.maxColorsLength):
            color = Color()
            self.colors.append(color)
            
            if (len(self.colors) <= 3):
                posx = 0
                posy = 30+len(self.colors)*50
            else:
                posx = 145
                posy = 80+((len(self.colors)-4)*50)

            Label(frame, bg='#9e9e9e').place(x=posx,y=posy, width= 145,height=55)

            Label(frame, bg='#9e9e9e', text="Color").place(x=posx+88,y=posy+5, width=50,height=15)
            button = Button(frame, text="Set color",font='Consolas 10 bold')
            self.colorButtons.append(button)
            self.colorButtons[self.colorButtons.index(button)].config(command=lambda:self.setColor(self.colorButtons.index(button)))
            self.colorButtons[self.colorButtons.index(button)].place(x=posx+5,y=posy+5, width= 75,height=45)
            
            label = Label(frame, bg='black',font='Consolas 10 bold')
            self.colorLabels.append(label)
            self.colorLabels[self.colorLabels.index(label)].place(x=posx+88,y=posy+25, width= 50,height=25)

    def setColorPosition(self, button):
        self.settingColorPosition = not self.settingColorPosition or self.currentSettingColorButton != button
        self.currentSettingColorButton = button

        for i in self.colorPosButtons:
            if (i != button and i['text'] == "Stop"):
                i['text'] = "Set pos"

        if (button['text'] != "Stop"):
            button['text'] = "Stop"
        elif (button['text'] == "Stop"):
            index = self.colorPosButtons.index(button)
            if (self.colorPositions[index][0] != None):
                button['text'] = self.colorPositions[index]
            else: button['text'] = "Set pos"


    def onValidate(self, d, i, P, s, S, v, V, W):
        # Disallow anything but lowercase letters
        if S.isdigit() or S == '.':
            return True
        else:
            self.root.bell()
            return False

    def screens(self):

        # Main Screen
        Label(self.root, bg='#b3b3b3').place(x=0,y=0, width= 600,height=400)
        # Top and bottom bar
        Label(self.root, bg='#fcef5b',text="PyClicker",font='Consolas 25 bold').place(x=0,y=0, width= 600,height=75)
        Label(self.root, bg='#fcef5b',font='Consolas 25 bold').place(x=0,y=350, width= 600,height=50)

        # Buttons and text
        Button(self.root, text="Click",font='Consolas 10 bold', command=lambda:self.changeOption(1, clickFrame)).place(x=10,y=85, width= 125,height=75)
        Button(self.root, text="Click Positions",font='Consolas 10 bold', command=lambda:self.changeOption(2, clickPositionsFrame) ).place(x=10,y=175, width= 125,height=75)
        Button(self.root, text="Click Colors",font='Consolas 10 bold', command=lambda:self.changeOption(3, clickColorsFrame)).place(x=10,y=265, width= 125,height=75)
        self.startButton = Button(self.root, text="Start",font='Consolas 10 bold', command=self.StartButton)
        self.startButton.place(x=490,y=355, width= 100,height=40)
        

        Label(self.root, text="Hotkeys",font='Consolas 10 bold', bg='#fcef5b').place(x=10,y=355, width= 100,height=40)
        Label(self.root, text="Start\nalt+1",font='Consolas 10 bold', bg='#fcef5b').place(x=110,y=355, width= 100,height=40)
        Label(self.root, text="Record pos/colour\nalt+0",font='Consolas 10 bold', bg='#fcef5b').place(x=220,y=355, width= 125,height=40)

        # Info frame
        infoFrame = Frame(self.root,bg="#b3b3b3")

        Label(infoFrame,text="Welcome to PyClicker", bg="#b3b3b3").place(x=0,y=0, width= 445,height=75)
        Label(infoFrame,text="PyClicker is an autoclicker made completely with python. ", bg="#b3b3b3").place(x=0,y=50, width= 445,height=75)
        
        
        infoFrame.place(x=145, y=85, width= 445,height=255)

        # Click spam frame
        clickFrame = Frame(self.root,bg="#b3b3b3")

        Label(clickFrame,text="This setting will spam a mouse button", bg="#b3b3b3").place(x=0,y=0, width= 445,height=75)
        clickTypeButton = Button(clickFrame,text="Left Click")
        clickTypeButton.config(command=lambda:self.switchClickType(clickTypeButton))
        clickTypeButton.place(x=0,y=75, width= 445,height=75)

        # Validation
        vcmd = (clickFrame.register(self.onValidate),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        var = StringVar()
        clickTimeEntry = Entry(clickFrame, bg="#b3b3b3", text="0x0",font='Consolas 10 bold', validate='key', validatecommand=vcmd, textvariable=var)
        clickTimeEntry.insert(0, '0')
        self.clickTime = clickTimeEntry
        clickTimeEntry.place(x=0,y=125, width= 445,height=75)
        
        clickFrame.place(x=145, y=85, width= 445,height=255)

        # Click positions frame
        clickPositionsFrame = Frame(self.root,bg="#bdbdbd")

        Label(clickPositionsFrame,text="This setting will click on the positions that you specify here", bg="#b3b3b3").place(x=0,y=0, width= 445,height=25)
        
        addNewPosition = Button(clickPositionsFrame,text="Add pos")
        addNewPosition.config(command=lambda:self.addPosition(clickPositionsFrame))
        addNewPosition.place(x=345,y=215, width= 100,height=40)

        clickPositionsFrame.place(x=145, y=85, width= 445,height=255)

        # Click colors frame
        clickColorsFrame = Frame(self.root,bg="#bdbdbd")

        Label(clickColorsFrame,text="This setting will click on the colors that you specify here, within a box", bg="#b3b3b3").place(x=0,y=0, width= 445,height=25)
        
        setSpeed = Entry(clickColorsFrame, bg="#b3b3b3",font='Consolas 10 bold', validate='key', validatecommand=vcmd, textvariable=var)
        setSpeed.insert(0, '1')
        self.speed = setSpeed
        setSpeed.place(x=345,y=175, width= 100,height=40)

        clickTimeEntry.place(x=0,y=125, width= 445,height=75)
        addNewColor = Button(clickColorsFrame,text="Add color")
        addNewColor.config(command=lambda:self.addColor(clickColorsFrame))
        addNewColor.place(x=345,y=215, width= 100,height=40)

        Label(clickColorsFrame, text="Pick two corners to form a box", bg="#b3b3b3").place(x=0,y=25, width= 200,height=50)
        posButton = Button(clickColorsFrame, text="Set pos")
        posButton.config(command=lambda:self.setColorPosition(posButton))
        posButton.place(x=200,y=25, width= 125,height=50)
        posButton1 = Button(clickColorsFrame, text="Set pos")
        posButton1.config(command=lambda:self.setColorPosition(posButton1))
        posButton1.place(x=325,y=25, width= 125,height=50)

        self.colorPosButtons = [posButton, posButton1]
        clickColorsFrame.place(x=145, y=85, width= 445,height=255)

        self.changeOption(0, infoFrame)

        self.root.mainloop()

root = Tk()
root.protocol("WM_DELETE_WINDOW", on_closing)


        
app = App(root, "PyClicker", '600x400')
    

