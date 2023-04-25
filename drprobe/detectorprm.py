# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 12:12:27 2023

@author: User
"""
import numpy as np
import re
import os
from functools import reduce

class MsaPrm(object):
    def __init__(self, msa_dict=None, aberrations_dict=None):
        if msa_dict is None:
            msa_dict = {}
            
        if aberrations_dict is None:
            self.aberrations_dict = {}
        else:
            self.aberrations_dict = aberrations_dict
            
        self.num_detectors = msa_dict.get('num_detectors', 3)   #number of detector
        self.detector_1st = msa_dict.get('detector_1st',("90.0, 250.0, 0.0, 0.0, 0.0, 0.0",'HAADF','prm/FiscioneHAADF-profile.dat'))
        self.detector_2nd = msa_dict.get('detector_2nd',("30.0, 90.0, 0.0, 0.0, 0.0, 0.0",'ADF',''))
        self.detector_3rd = msa_dict.get('detector_3rd',("10.0, 23.0, 0.0, 0.0, 0.0, 0.0",'ABF',''))
        
    @property
    def number_of_aberrations(self):
        return len(self.aberrations_dict.keys())
    
    def factors(self, n):
        return np.sort(list(reduce(list.__add__,
                                   ([i, n // i] for i in range(1, int(n ** 0.5) + 1) if
                                    n % i == 0))))
    
    def save_msa_prm(self, prm_filename, output=True):
        directory = os.path.split(prm_filename)[0]
        if directory:
            if not os.path.isdir(directory):
                os.makedirs(directory, exist_ok=True)
        
        aberrations = {0: 'image_shift',
                       1: 'defocus',
                       2: '2-fold-astigmatism',
                       3: 'coma',
                       4: '3-fold-astigmatism',
                       5: 'CS',
                       6: 'star_aberration',
                       7: '4-fold-astigmatism',
                       8: 'coma(5th)',
                       9: 'lobe-aberration',
                       10: '5-fold-astigmatism',
                       11: 'C5'}
        
        with open(prm_filename, 'w') as prm:
            string_0 ="'[Detector Parameters]'"
            string_1 = "block ID string for detector definitions"
            prm.write("{} ! {}\n".format(string_0, string_1))
            string_2 ="2016021801"
            string_3 = "detector file format version (keep this)"
            prm.write("{} ! {}\n".format(string_2, string_3))
            string_4 = "number of detector definitions following, only this number of lines will be read in the following, additional lines are ignored."
            prm.write("{} ! {}\n".format(self.num_detectors, string_4))
            string_5 = "1st detector definition: inner radius [mrad], outer radius [mrad], start azimuth [deg], stop azimuth [deg], decenter-x [mrad], decenter-y [mrad], detector name string, detector sensitivity profile file "
            prm.write("{}, '{}', '{}'! {}\n".format(self.detector_1st[0], self.detector_1st[1], self.detector_1st[2], string_5))
            string_6 = "2nd detector definition"
            prm.write("{}, '{}', '{}'! {}\n".format(self.detector_2nd[0], self.detector_2nd[1], self.detector_2nd[2], string_6))
            string_7 = "3rd detector definition"
            prm.write("{}, '{}', '{}'! {}\n".format(self.detector_3rd[0], self.detector_3rd[1], self.detector_3rd[2], string_7))
            prm.write("(End of detector parameter file example)")
            
        # Sort prm file
        with open(prm_filename, 'r+') as prm:
            content = prm.readlines()

            length = []
            for line in content:
                length.append(len(line.split('!',1)[0]))

            spacer = np.max(length)
            prm.seek(0)
            prm.truncate()
            for line in content:
                if '!' in line:
                    line = line.split('!',1)[0].ljust(spacer) + ' !' + line.split('!',1)[1]
                prm.write(line)

        if output:
            print("Detectors parameters successfully saved to file '{}'!".format(prm_filename))