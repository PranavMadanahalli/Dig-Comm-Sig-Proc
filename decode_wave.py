from __future__ import division
import pyaudio
import wave
import random
import scipy.io.wavfile
import numpy as np
from IPython import display
import matplotlib.pyplot as plt
import sys
from math import sin, cos, pi, sqrt
FORMAT = pyaudio.paFloat32
v = 340.29
sampling_rate = 44100
carrier_freq0 = 6000
carrier_freq1 = 12000
time=5
rate, raw_signal = scipy.io.wavfile.read('file.wav')

def dominatfreq(time, recorder):
    nframes = int(float(time)*rate)
    tab = raw_signal
    print(tab)
    if (len(tab) == 0):
        return -1
    halftab = np.fft.fft(tab)
    print(halftab)
    halftab = halftab[0:int(time*rate/2)]
    return (np.argmax(np.absolute(halftab))/time)

err = 0
counta = 0
while(counta < 100): # err == 0
    noise = 0
    while(noise == 0):
        noise = dominatfreq(time, raw_signal)
        print("noise")
        if (noise == -1):
            err = 1
            break
    #synchronization ***
    # maxx = -1.0;
    # for i in range(0,5):
    #     nframes = int(float(time)*rate)
    #     tab = raw_signal
    #     if (len(tab) == 0):
    #         break
    #     halftab = np.fft.fft(tab)[0:int(time*rate/2)]
    #     temp = int(np.argmax(np.absolute(halftab))/time)
    #     print("no noise")
    #     print(temp)
    #     if (temp > maxx): #index zep
    #         maxx = temp
    #         index = i
    #     if (temp < carrier_freq0):
    #         err = 1
    #         break
    #     tab = raw_signal[0:int(len(raw_signal)/5)]
    # else:
    #     for i in range(0, index):
    #         raw_signal[0:int(len(raw_signal)/5)]
    # if (err == 1):
    #     continue
    # #finding the end of the preamble ***
    # prev = 2
    # while(True):
    #     cur =  dominatfreq(time, raw_signal)
    #     print(cur)
    #     if (cur == -1):
    #         err = 1
    #         break
    #     if (cur == prev == carrier_freq1):
    #         break;
    #     prev = cur
    #reading the encoded message ***
    counta = counta + 1
    todecodein = ""
    count = 0
    while(count < 100):
        print("trying to decode")
        try:
            sound = dominatfreq(time, raw_signal)
            print(sound)
        except:
            break
        if (int(sound) <= 0):
        	err = 1
        	break
        if (sound == carrier_freq0):
        	todecodein += '0'
        elif (sound == carrier_freq1):
        	todecodein += '1'
        try:
        	outpu = decode(todecodein)
        	print(outpu)
        except:
            count = count + 1
            print("not decoding")
            continue
# print(record_rate)
# print(len(raw_signal))
# raw_signal_fft = np.fft.fft(raw_signal)
# halftab = raw_signal_fft[0:int(time*record_rate/2)]
# print(np.argmax(np.absolute(halftab))/time)
#
# N = len(raw_signal)
# L = N / record_rate
# print(f'Audio length: {L:.2f} seconds')
#
# f, ax = plt.subplots()
# ax.plot(np.arange(N) / record_rate, raw_signal_fft)
# ax.set_xlabel('Time [s]')
# ax.set_ylabel('Amplitude [unknown]');
# # Demodulate raw signal
# #demod = demodulate_signal(raw_signal)
# plt.show()
