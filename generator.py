import numpy
import sys
import math
import binascii
import pyaudio
import numpy as np
from bitarray import bitarray
import zlib
import wave


amplitude = 2000
samplerate = float(1/float(sys.argv[1]))
freq0 = 3000
freq1 = 500


def encoding(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def decode(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)



def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

def generplay(code):
    samples = [0, 0]
    code=code
    p = pyaudio.PyAudio()
    volume = 1    # range [0.0, 1.0]
    samples[0] =  ((np.sin(np.arange(0,2*math.pi*samplerate*freq0,2*math.pi*freq0/1200))*amplitude).astype(np.float32))
    samples[0] = samples[0]/(max(np.abs(samples[0])))
    samples[1] =  (np.sin(np.arange(0,2*math.pi*samplerate*freq1,2*math.pi*freq1/1200))*amplitude).astype(np.float32)
    samples[1] = samples[1]/(max(np.abs(samples[1])))

    # generate samples, note conversion to float32 array
    # for paFloat32 sample values must be in range [-1.0, 1.0]
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=1200, output=True)
    for i in code:
        stream.write(volume*samples[int(i)])
    stream.stop_stream()
    stream.close()
    p.terminate()

    # play. May repeat with different volume values (if done interactively)
    # stream.write(volume*frames[0])
x = encoding("########aaaaaa###############")
print(len(x))
print(freq0)
print(freq1)
print(x)
print(decode(x))

generplay(x)
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
