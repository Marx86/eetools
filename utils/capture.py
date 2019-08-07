import struct
import alsaaudio
from math import ceil

channels = 2
frame_rate = 48000                   # frames per second
period_size = 600
num_samples = frame_rate

pcm = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)
pcm.setchannels(channels)
pcm.setformat(alsaaudio.PCM_FORMAT_FLOAT_LE)
pcm.setrate(frame_rate)
pcm.setperiodsize(period_size)


def capture_samples(samples=num_samples):
    data = ''
    data_l = ''
    data_r = ''
    chuncs = int(ceil(samples / period_size / 10.0))

    for i in range(chuncs):
        l = 0
        _bytes = ''
        while not l:
            l, _bytes = pcm.read()

        data += _bytes
    data_l = ''.join(data[i:i+4] for i in range(0, len(data), 8))
    data_r = ''.join(data[i:i+4] for i in range(4, len(data), 8))

    # Parse s32_le
    return struct.unpack('<'+'f'*(len(data_l) / 4), data_l), struct.unpack('<'+'f'*(len(data_l) / 4), data_r)
