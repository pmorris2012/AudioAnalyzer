import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt

chunk = 735
format = pyaudio.paInt16
channels = 2
rate = 44100

p = pyaudio.PyAudio()

stream = p.open(format=format,channels=channels,rate=rate,input=True,frames_per_buffer=chunk)

left = []
right = []

stream.read(chunk)

print 'Starting to record'

frame = stream.read(chunk * 60)

print 'Done recording'

for i in xrange(0, len(frame), 4):
	left.append(struct.unpack('<h', frame[i:i+2]))
	right.append(struct.unpack('<h', frame[i+2:i+4]))

left = [x[0] for x in left]
right = [x[0] for x in right]

f = np.fft.fft(left)

print len(f)

plt.figure(1)
plt.subplot(211)
plt.plot(f)
#plt.axis([0, chunk * 50, -pow(2, 15), pow(2, 15)])
plt.subplot(212)
plt.plot(right)
plt.axis([0, chunk * 50, -pow(2, 15), pow(2, 15)])
plt.show()

stream.stop_stream()
stream.close()
p.terminate()