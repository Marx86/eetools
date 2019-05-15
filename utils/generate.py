#!/usr/bin/env python
# -*- coding: utf-8 -*-

import struct
import alsaaudio
from math import pi, sin
from random import uniform

channels = 2
sample_size = 1                     # bytes per sample
frame_size = channels * sample_size # bytes per frame
frame_rate = 48000                   # frames per second
byte_rate = frame_rate * frame_size # bytes per second
period_size = frame_rate

pcm = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK)
pcm.setchannels(channels)
pcm.setformat(alsaaudio.PCM_FORMAT_FLOAT_LE)
pcm.setrate(frame_rate)
pcm.setperiodsize(period_size)


gen_sample = lambda s, g: struct.pack('f', s*g) * channels


def sine_wave(freq, gain=1.0, periods=None):
    max_val = 2 * pi
    i = 0.0
    period_num = 1

    while True:
        pcm.write(gen_sample(sin(i), gain))
        i += max_val / (frame_rate / float(freq))

        if i > max_val:
            period_num += 1
            i = 0.0
            if periods and period_num > periods:
                break


def sq_wave(freq, gain=1.0):
    i = 0.0
    frame_count = 0.0

    while True:
        pcm.write(gen_sample(i, gain))

        frame_count += freq
        frame_count = frame_count <= frame_rate and frame_count or 0.0
        i = frame_count > frame_rate / 2.0 and 1.0 or -1.0


def pink_noise(gain=1.0):
    b0, b1, b2, b3, b4, b5, b6 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

    while True:
        white = uniform(-1, 1)
        b0 = 0.99886 * b0 + white * 0.0555179
        b1 = 0.99332 * b1 + white * 0.0750759
        b2 = 0.96900 * b2 + white * 0.1538520
        b3 = 0.86650 * b3 + white * 0.3104856
        b4 = 0.55000 * b4 + white * 0.5329522
        b5 = -0.7616 * b5 - white * 0.0168980
        sample = b0 + b1 + b2 + b3 + b4 + b5 + b6 + white * 0.5362
        sample *= 0.11
        b6 = white * 0.115926

        pcm.write(gen_sample(sample, gain))


def brown_noise(gain=1.0):
    last = 0.0

    while True:
        white = uniform(-1, 1)
        sample = (last + (0.02 * white)) / 1.02
        last = sample
        sample *= 3.5

        pcm.write(gen_sample(sample, gain))


def white_noise(gain=1.0):
    while True:
        pcm.write(gen_sample(uniform(-1, 1), gain))

