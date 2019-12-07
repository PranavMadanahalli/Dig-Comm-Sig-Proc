import wave
import struct
import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt
import binascii
def isSilence(windowPosition):
    sumVal = sum( [ x*x for x in sound[windowPosition:windowPosition+windowSize+1] ] )
    avg = sumVal/(windowSize)
    if avg <= 0.0001:
        return True
    else:
        return False


rate, raw_signal = scipy.io.wavfile.read('file.wav')

rate=len(raw_signal)
plt.plot(raw_signal)
plt.show()
while(np.mean(np.abs(np.random.choice(raw_signal[0 : 44100],size=1000)))< .1*10**9):
    raw_signal=raw_signal[44100:]
rate=len(raw_signal)//48
#print(rate)
T1 = 1/1600
T2 = 1/800
frate = rate
window_1 = int(T1*rate)
print(int(len(raw_signal)//rate))
plt.plot(raw_signal)
plt.show()

#zero=np.mean(((volume*np.sin(np.arange(0,2*math.pi*time*freq0,2*math.pi*freq0/44100))*amplitude).astype(np.float32)))
#one=np.mean((volume*np.sin(np.arange(0,2*math.pi*time*freq1,2*math.pi*freq1/44100))*amplitude).astype(np.float32))

string = ""
for i in range(int(len(raw_signal)//rate)):
    val = np.mean(np.abs(np.random.choice(raw_signal[i*rate : min(i*rate + rate,len(raw_signal))],size=1000)))
    if (val >= .4*(10**9)):
        string+="1"
    else:
        string+="0"
string = "0b"+string
print(string)
def decode(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

original_str = "011000010110001001100011011001000110010101100110"
our_str = string[2:]
print(sum([1 if original_str[i]==our_str[i] else 0 for i in range(len(our_str))])/len(our_str))
# print(len(string))
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
