#!/usr/bin/env python
#-*-coding:utf8-*-
from __future__ import print_function
import math


def _read_num_param(param_name, msg):
    param = None

    while not param:
        try:
            param = float(input(msg))
        except ValueError:
            print(u'ERROR: {} must be a number.'.format(param_name))

    return param


def run_manual(by_parameter, R1, R2, Re):
    if by_parameter == 'I':
        Ir2 = _read_num_param(by_parameter, u'Please enter "R2" amperage:')
        Uout = Ir2 * (R1 + R2)
        #_pass = input(u'Please connect speaker instead "R2" and press "Enter":')
        Ifs = _read_num_param(by_parameter, u'Please enter "Fs" amperage:')
        Rfs = (Uout / Ifs) - R1
    else:
        Ur2 = _read_num_param(by_parameter, u'Please enter "R2" voltage:')

    Ro = Rfs / Re
    Rx = math.sqrt(Ro) / Rfs

    Ix = Uout / (Rx + R1)
    Ux = Ix * Rx

    print(Ix, Ux)
