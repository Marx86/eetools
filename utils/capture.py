import struct
import alsaaudio
from math import ceil

channels = 1
frame_rate = 48000                   # frames per second
period_size = 64
num_samples = frame_rate

pcm = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)
pcm.setchannels(channels)
pcm.setformat(alsaaudio.PCM_FORMAT_S32_LE)
pcm.setrate(frame_rate)
pcm.setperiodsize(period_size)


def capture_samples(samples=num_samples):
    data = []
    chuncs = int(ceil(samples / period_size))
    for i in range(chuncs):
        l = 0
        while not l:
            l, _bytes = pcm.read()
        # Parse s32_le
        data.extend(struct.unpack('<'+'i'*l, _bytes))

    return data[:samples]
