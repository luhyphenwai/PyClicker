import threading
from pyautogui import *
import time, keyboard, threading
import win32api, win32con, win32gui

# Clicks per second
cps = 10
click_type = 1


# Click function, will click where x and y are set
def click ():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01) # Pause script for 0.01 seconds for mouse down to register
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def set_speed():
    global current_option
    # Prompt
    print("Choose your clicks per second for the program")

    # Reset value
    global cps
    cps = 0

    # Make sure value is integer
    while (cps == 0):
        if (current_option == 0):
                break
        try:
            cps = int(input("Input an integer"))
        except ValueError:
            print("That is not a valid integer")
    print("Your clicks per second are now "+str(cps))
    current_option = 0 
    print("Select a new option")
    
# Spam button
def click_mouse():
    global cps
    click()
    check_end()

# Click position variables
def click_positions():
    global cps
    global current_option
    state_left = win32api.GetKeyState(0x01)  # Left button up = 0 or 1. Button down = -127 or -128
    let_go = True
    positions = []

    # Prompt
    print("Click on the positions you would like to select, press alt+3 to end")

    # Wait to let go 
    while keyboard.is_pressed('alt+3'):
        pass
        
    # Get options
    while (keyboard.is_pressed('alt+3') == False):
        if (current_option == 0):
                break
        a = win32api.GetKeyState(0x01)
        if (a == -127 or a == -128) and let_go:  # Pessing button and also let go already
            positions.append(win32gui.GetCursorPos())
            let_go = False
            print(len(positions))
        elif (a == 0 or a == 1) and let_go == False:
            let_go = True

    print("Your positions have been chosen")
    while (current_option != 0):
        for i in range(len(positions)):
            if (current_option == 0):
                break
            win32api.SetCursorPos(positions[i])
            click()
            time.sleep((1/cps))

def click_colors():
    global cps
    global current_option
    color_option = 0
    positions = []

    print("Would you like to click colors within an area, or within certain positions (alt+1 for first option, alt+2 for second):")

    option_picked = False
    while (option_picked == False):
        if (keyboard.is_pressed('alt+1')):
            color_option = 1
            option_picked = True
        elif(keyboard.is_pressed('alt+2')):
            color_option = 2
            option_picked = True
    
    if (color_option == 1):
        print("Select the top left and bottom right positions that you would like to search for colors in")
        let_go = True
        tuples=[]
        pos = []
        while (len(tuples) < 2):
            if (current_option == 0):
                break
            a = win32api.GetKeyState(0x01)
            if (a == -127 or a == -128) and let_go:  # Pessing button and also let go already
                tuples.append(win32gui.GetCursorPos())
                let_go = False
                print(len(tuples))
            elif (a == 0 or a == 1) and let_go == False:
                let_go = True
        # test print of positions

        print(tuples)
        # Convert tuples to just lists
        for i in range(2):
            pos.append([])
            pos[i].append(tuples[i][0])
            pos[i].append(tuples[i][1])
        
        # Swap x and y positions to correct sections
        # Swap x
        if (pos[0][0] < pos[1][0]): 
            temp = pos[0][0] # record lower x
            pos[0][0] = pos[1][0] # Set higher x
            pos[1][0] = temp # Set lower x
        # Swap y
        print(pos[0][1] < pos[1][1])
        if (pos[0][1] < pos[1][1]): 
            temp = pos[0][1] #record lower y
            pos[0][1] = pos[1][1] # Set higher y
            pos[1][1] = temp # Set lower y
        print(pos)

    elif (color_option == 2):
        print("Click on the positions you would like to check, press (alt+4) to finish")
        let_go = True
        while (keyboard.is_pressed('alt+4') == False):
            if (current_option == 0):
                    break
            a = win32api.GetKeyState(0x01)
            if (a == -127 or a == -128) and let_go:  # Pessing button and also let go already
                positions.append(win32gui.GetCursorPos())
                let_go = False
                print(len(positions))
            elif (a == 0 or a == 1) and let_go == False:
                let_go = True



options = {
    1:set_speed,
    2:click_mouse,
    3:click_positions,
    4:click_colors
}


current_option = 0

def check_end():
    global current_option
    
    # Check for alt+0
    if (keyboard.is_pressed('alt+0')):
        current_option = 0
        print("Select a new option")
   


# Main program
def main():
    global current_option
    print("Welcome to PyClicker")
    print("Options:")
    print("(alt+1) Set speed")
    print("(alt+2) Click mouse button")
    print("(alt+3) Click mouse at preset positions")
    print("(alt+4) Click certain colors within a position")
    print("(alt+9) End program")
    print("(alt+0) Stop current selection")
    program_end = False
    while (program_end == False):
        
        if current_option != 0:
            options[current_option]()
        
        time.sleep((1/cps))
   
def monitor_keyboard():
    global current_option
        
    while (1):
        if (current_option == 0):
                for i in range(10):
                    if (keyboard.is_pressed('alt+'+str(i)) and not keyboard.is_pressed('alt+0')):                                                                                                          
                        current_option = i
                        print("You picked option "+str(i))
        # Check for alt+0
        if (keyboard.is_pressed('alt+0') and current_option != 0):
            current_option = 0
            print("Select a new option")

#Start threads
t1 = threading.Thread(target=main, args=())
t2 = threading.Thread(target=monitor_keyboard, args=())
t1.start()
t2.start()

