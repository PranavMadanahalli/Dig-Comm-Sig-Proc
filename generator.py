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
time = float(1/float(sys.argv[1]))
filename = sys.argv[2]
freq0 = 2000
freq1 = 600


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

    p = pyaudio.PyAudio()
    volume = 0.5    # range [0.0, 1.0]
    samples[0] =  ((np.sin(np.arange(0,2*math.pi*time*freq0,2*math.pi*freq0/1200))*amplitude).astype(np.float32))
    samples[0] = samples[0]/(max(np.abs(samples[0])))
    samples[1] =  (np.sin(np.arange(0,2*math.pi*time*freq1,2*math.pi*freq1/1200))*amplitude).astype(np.float32)
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
    # stream.write(volume*frames[0]

with open(filename, 'r') as file:
    data = file.read().replace('\n', '')
    generplay(encoding(data))
    print("Generating completed.")
