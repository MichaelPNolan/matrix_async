# import matrix_setup
from digitalio import DigitalInOut, Direction  # , Pull

from matrix_setup import display, print_buttons, col, btn, led, LED_DIM,  \
    led_pattern, printTime, elapsed_time, start_time
import time
import board
import asyncio  # in micropython you might use import _thread
from audioTest import kick, snare
import audiobusio
''' classaudiobusio.I2SOut(bit_clock, word_select, data, *, left_justified)'''
audio = audiobusio.I2SOut(board.GP8, board.GP9, board.GP7)
bscan_ready = 0
bpm = 60
tempo_sixteenth =  15/bpm  #where a quarter at 60 is 1 sec so 60/60 = 1 but 15/60 = 0.25
beat_map = [False for i in range(16)]

def led_rows_on(led_col):
    for i in range(LED_DIM):
        led[i].value = led_pattern[led_col][i]
    
def led_rows_off(led_col):
    for i in range(LED_DIM):
        led[i].value = True

# bug - all one column
debounce = 0        
def check_button(button_col, button_row):
    global bscan_ready, debounce
    if debounce > 0:
        debounce -= 1
    elif btn[button_row].value is True:
        button_num = 4*button_col+button_row
        # print("BTN+:"+str(button_num))
        # bscan_ready = 0
        # led[button_row].value = not led[button_row].value
        if led_pattern[button_col][button_row]:
            led_pattern[button_col][button_row] = False
            print_buttons(button_num, 1, True)  # because False turns LED on
            beat_map[button_num] = True
        else:
            led_pattern[button_col][button_row] = True
            print_buttons(button_num, 1, False)
            beat_map[button_num] = False
        # print(led_pattern[button_col])
        debounce = 16
    # else:
        #  print("BTN-:"+str(button_col))
    

''' this is about the lighting of LEDs switching the gpios of col one at a time
    and during that time each row is set according to 
    led_pattern[led_col][i] in a for loop'''  
async def processMatrix():
    global reset, bscan_ready, elapsed_time, start_time
    while True:
        col_idx = 0
        
        start_time = time.monotonic()
        for c in col:
            c.value = True  # set the column pin high
            await asyncio.sleep(0.002)
            
            led_rows_on(col_idx)
            if bscan_ready == 1:
                await asyncio.sleep(0.001)
                for row_idx in range(LED_DIM):
                    check_button(col_idx, row_idx)  # row_idx
                await asyncio.sleep(0.001)
            else:
                await asyncio.sleep(0.002)
            led_rows_off(col_idx)
            
            c.value = False  # set the column pin low
            
            # printTime()
            col_idx = col_idx + 1
        elapsed_time = time.monotonic() - start_time

        bscan_ready = 0
        
        
''' relies on process Matrix to finish and reset bscan to 0 '''        
async def bscan_timer():
    global bscan_ready
    indicator_LED = DigitalInOut(board.GP22)
    indicator_LED.direction = Direction.OUTPUT
    while True:
        if bscan_ready == 0:
            bscan_ready = 1
            indicator_LED.value ^= 1
        await asyncio.sleep(0.1)

''' i really want to get this to run faster 
maybe a complied .mpy of the library'''
async def print_loop():
    global elapsed_time
    while True:
        printTime(elapsed_time)
        await asyncio.sleep(5)
        
async def beat_loop():
    global tempo_sixteenth
    current_beat = 0
    while True:
        current_beat +=1
        if current_beat > 15:
            current_beat = 0
        if beat_map[current_beat]:
            audio.play(kick)
        await asyncio.sleep(tempo_sixteenth)
       
        
        # prep for main loop
display.clear()
display.print("ReadySteady")


# init row_LCD
for bn in range(16):
    print_buttons(bn, 1, False)
# while True is the main event loop
# -------------------------------------------------
async def main():
    global elapsed_time, schedule_time, bscan_ready, schedule_time
    
    matrix_task = asyncio.create_task(processMatrix())
    bscan_timer_task = asyncio.create_task(bscan_timer())
    # print_loop_task = asyncio.create_task(print_loop())
    beat_loop_task = asyncio.create_task(beat_loop())
    await asyncio.gather(matrix_task, bscan_timer_task, beat_loop_task)
    print("done")


# --------------------------------------------------

asyncio.run(main())
