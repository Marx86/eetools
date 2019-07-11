#!/usr/bin/env python
#-*-coding:utf8-*-
import math


CIRCUIT_U = '''
        R1
      _____
 +---|_____|---o-------------+   <----+
 |             |             |        |
 |             |            _|_       | /|
 |             |            | |      +-+ |
(~) Vout      (V) Voltmeter | | R2   | | | Speaker
 |             |            |_|      +-+ |
 |             |             |        | \|
 |             |             |        |
 +-------------o-------------+   <----+
'''

CIRCUIT_I = '''
    Amperemeter     R1
                  _____
 +------(I)------|_____|-----+   <----+
 |                           |        |
 |                          _|_       | /|
 |                          | |      +-+ |
(~) Vout                    | | R2   | | | Speaker
 |                          |_|      +-+ |
 |                           |        | \|
 |                           |        |
 +---------------------------+   <----+
'''


def _read_num_param(param_name, msg):
    param = None

    while not param:
        try:
            param = float(raw_input(msg))
        except ValueError:
            print(u'ERROR: "{}" must be a number.'.format(param_name))

    return param


def run_manual(by_parameter, R1=None, R2=None, Re=None, Vb=None):
    if not Re:
        Re = _read_num_param(by_parameter, u'Please enter "Re" value in Ohms:')

    if not R1:
        R1 = _read_num_param(by_parameter, u'Please enter "R1" value in Ohms:')

    if not R2:
        R2 = _read_num_param(by_parameter, u'Please enter "R2" value in Ohms:')

    if by_parameter == 'I':
        print(CIRCUIT_I)
        Ir2 = _read_num_param(by_parameter, u'Please enter "R2" amperage:')
        Uout = Ir2 * (R1 + R2)
        raw_input(u'Please connect speaker instead "R2" and press "Enter":')
        Ifs = _read_num_param(by_parameter, u'Please enter speaker "Fs" amperage:')
        Rfs = (Uout / Ifs) - R1
    else:
        print(CIRCUIT_U)
        Ur2 = _read_num_param(by_parameter, u'Please enter "R2" voltage:')

    Ro = Rfs / Re
    Rx = math.sqrt(Ro) / Re

    Ix = Uout / (Rx + R1)
    Ux = Ix * Rx

    if by_parameter == 'I':
        F1 = _read_num_param('F1', u'Please enter the lower frequency at which the current is {0:.3f}:'.format(Ix))
        F2 = _read_num_param('F1', u'Please enter the higher frequency at which the current is {0:.3f}:'.format(Ix))
    else:
        F1 = _read_num_param('F1', u'Please enter the lower frequency at which the voltage is {0:.3f}:'.format(Ux))
        F2 = _read_num_param('F1', u'Please enter the higher frequency at which the voltage is {0:.3f}:'.format(Ux))

    Fs = math.sqrt(F1 * F2)

    Qms = (Fs * math.sqrt(Ro)) / (F2 - F1)
    Qes = Qms / (Ro - 1)
    Qts = (Qes * Qms) / (Qes + Qms)

    Vas = 0
    if Vb:
        Fc = _read_num_param(by_parameter, u'Please enter resonanse frequency in "Vb" box:')
        Vas = Vb * (((Fc / Fs) ** 2) - 1)

    result = (
        'Fs  = {fs:.1f} Hz\n'
        'Qts = {qts:.2f}\n'
        'Qes = {qes:.2f}\n'
        'Qms = {qms:.2f}\n'
        'Vas = {vas:.2f} l'
    ).format(fs=Fs, qts=Qts, qes=Qes, qms=Qms, vas=Vas)
    print(result)
