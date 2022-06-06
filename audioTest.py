import audiocore
import board

import time


kick_file = open("bd_tek.wav", "rb")  #open for reading in binary mode ... rb
snare_file = open("drum_cowbell.wav", "rb")
snare = audiocore.WaveFile(snare_file)
kick = audiocore.WaveFile(kick_file)
'''possible order word select, bclock, data
classaudiobusio.I2SOut(bit_clock, word_select, data, *, left_justified)'''
'''
audio = audiobusio.I2SOut(board.GP8, board.GP9, board.GP7)
count = 10
while count > 0:
 
    audio.play(kick)
    time.sleep(0.2)
    audio.play(kick)
    time.sleep(0.3)
    audio.play(snare)
    time.sleep(0.7)
    count -= 1
    while audio.playing:
        pass
        '''