import board
import busio
from digitalio import DigitalInOut, Direction, Pull
import lcd
import i2c_pcf8574_interface
#--------------------Initialize for the matrix of led/buttons
led = [ DigitalInOut(board.GP13), DigitalInOut(board.GP12),
            DigitalInOut(board.GP11), DigitalInOut(board.GP10)]
LED_DIM = 4 #4 by 4 light and buttons
#this approach was terrible - don't do this it points 4 reference to the same single array
#led_pattern = [[True]*LED_DIM]*LED_DIM  #True means light is off because same volts as input
                                        #led_pattern[col][row]

led_pattern = [[True for i in range(LED_DIM)] for j in range(LED_DIM)]


col = [DigitalInOut(board.GP16), DigitalInOut(board.GP17)
       , DigitalInOut(board.GP15), DigitalInOut(board.GP14)]

btn = [DigitalInOut(board.GP18), DigitalInOut(board.GP19),
       DigitalInOut(board.GP20), DigitalInOut(board.GP21)]
state = ["on", "off"]
lineNum = 0

i2c = busio.I2C(scl=board.GP1, sda=board.GP0,
            frequency=1000000,timeout=255)
LCDaddress = 39

i2c = i2c_pcf8574_interface.I2CPCF8574Interface(i2c, LCDaddress)
display = lcd.LCD(i2c, num_rows=2, num_cols=16)
elapsed_time = 0
start_time = 0

#initialize GPIO     
for c in col:   #these are set true sequentially while 4 rows are tested
    c.direction = Direction.OUTPUT
    c.value = False
    
for i in led:   #when these led-rows are set false the LED will illuminate dependent on column
    i.direction = Direction.OUTPUT
    i.value = True

for b in btn:   #these are pull downs that will go high when a button is pressed while column on
    b.direction = Direction.INPUT
    b.pull = Pull.DOWN

#LCD functions
display.set_backlight(True)
display.set_display_enabled(True)
def printLCD(text):
    """ this is for alternatively printing messages or scrolling"""
    global  lineNum, display  #alternate between 2 positions unless we have columns
    lineNum = not lineNum
    display.set_cursor_pos(lineNum,0)
    display.print(text)
    display.print(" ") #to erase longer prev prints
    


def printTime(elapsed_time):
    display.set_cursor_pos(0,0)
    display.print("Time:")
    display.print(str(elapsed_time))
    
def print_buttons(button_num, LCDrow, status):
    display.set_cursor_pos(LCDrow, button_num)
    if status:
        display.print("o")
    else:
        display.print("_")
        