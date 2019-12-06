import wave
import struct
import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot
import binascii

def isSilence(windowPosition):
    sumVal = sum( [ x*x for x in sound[windowPosition:windowPosition+windowSize+1] ] )
    avg = sumVal/(windowSize)
    if avg <= 0.0001:
        return True
    else:
        return False


rate, raw_signal = scipy.io.wavfile.read('file.wav')
rate=1200
print(rate)
T1 = 1/1600
T2 = 1/800
frate = rate
window_1 = int(T1*rate)
print(len(raw_signal))
matplotlib.pyplot.plot(raw_signal)
matplotlib.pyplot.show()

#zero=np.mean(((volume*np.sin(np.arange(0,2*math.pi*time*freq0,2*math.pi*freq0/44100))*amplitude).astype(np.float32)))
#one=np.mean((volume*np.sin(np.arange(0,2*math.pi*time*freq1,2*math.pi*freq1/44100))*amplitude).astype(np.float32))

string = ""
for i in range(len(raw_signal)//rate):
    val = np.mean(raw_signal[i*rate : min(i*rate + rate,len(raw_signal))])
    if (val > 10^9):
        string+="1"
    else:
        string+="0"

def decode(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

# string=string.zfill(8 * ((len(string) + 7) // 8))
print(string)
# print(decode(string))

# w = np.fft.fft(raw_signal)
#
# freqs = np.fft.fftfreq(len(w))
# print(freqs.min(), freqs.max())
# # (-0.5, 0.499975)
# # Find the peak in the coefficients
# idx = np.argmax(np.abs(w))
# freq = freqs[idx]
# freq_in_hertz = abs(freq * rate)
# print(freq_in_hertz)
