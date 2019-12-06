import numpy
import sys
import math

import pyaudio
import numpy as np
from bitarray import bitarray
import zlib
import wave


amplitude = 2000
time = float(1/float(sys.argv[1]))
freq0 = float(sys.argv[2])
freq1 = float(sys.argv[3])

tocode = {
    '0000':'11110',
    '0001':'01001',
    '0010':'10100',
    '0011':'10101',
    '0100':'01010',
    '0101':'01011',
    '0110':'01110',
    '0111':'01111',
    '1000':'10010',
    '1001':'10011',
    '1010':'10110',
    '1011':'10111',
    '1100':'11010',
    '1101':'11011',
    '1110':'11100',
    '1111':'11101'
}

def code4b5b(code):
	output = ""
	while (len(code)):
		output += tocode[code[:4]]
		code = code[4:]
	return output

def codenrz(code):
	output = ""
	prev = 1
	while (len(code)):
		cur = code[:1]
		code = code[1:]
		if (cur == "1"):
			prev = (prev+1)%2
		output += str(prev)
	return output


def encoding(to, fromwho, msg):
	output = bin(int(fromwho))[2:].zfill(48)
	output += bin(int(to))[2:].zfill(48)
	output += bin(len(msg))[2:].zfill(16)
	for i in range(0, len(msg)):
		output += bin(ord(msg[i]))[2:].zfill(8)
	output += bin(zlib.crc32(bitarray(output).tobytes())&0xffffffff)[2:].zfill(32)
	output = code4b5b(output)
	output = codenrz(output)
    #term one below is the 'preamble'
	output =  "1010101010101010101010101010101010101010101010101010101010101011" + output
	return output


def generplay(code):
    frames = [0, 0]

    p = pyaudio.PyAudio()
    volume = 0.1    # range [0.0, 1.0]
    #fs = 44100       # sampling rate, Hz, must be integer
#    duration = 1.0   # in seconds, may be float
#    f = 940.0        # sine frequency, Hz, may be float
    frames[0] =  (np.sin(np.arange(0,2*math.pi*time*freq0,2*math.pi*freq0/44100))*amplitude).astype(np.float32)
    frames[1] =  (np.sin(np.arange(0,2*math.pi*time*freq1,2*math.pi*freq1/44100))*amplitude).astype(np.float32)
    # generate samples, note conversion to float32 array
    # for paFloat32 sample values must be in range [-1.0, 1.0]
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True)
    for i in code:
        stream.write(volume*frames[int(i)])
    stream.stop_stream()
    stream.close()
    p.terminate()

    # play. May repeat with different volume values (if done interactively)
    # stream.write(volume*frames[0])
generplay(encoding(1, 900, "Hi this should make a lot of noises.Beep boop bop."))
"""while True:
	try:
		input = input()
	except EOFError:
		break

	if(input == ""):
		break
	else:
		inputspl = input.split(" ", 2)
		output = encoding(inputspl[0], inputspl[1], inputspl[2])
		generplay(output)
	print("Generating completed.")
	break"""
