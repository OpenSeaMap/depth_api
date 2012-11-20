#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------------------------------
# OpenSeaMap API - Web API for OpenSeaMap services.
#
# Written in 2012 by Dominik Fässler dfa@bezono.org
#
# To the extent possible under law, the author(s) have dedicated all copyright
# and related and neighboring rights to this software to the public domain
# worldwide. This software is distributed without any warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
# --------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------
# Imports external
# --------------------------------------------------------------------------------------------------

import random


# --------------------------------------------------------------------------------------------------

class Utils():
    '''
    Provides utility functions for this project.
    '''

    # ----------------------------------------------------------------------------------------------

    @staticmethod
    def generateRandomStringContainingLettersAndDigits(length):
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        maxCharsIndex = len(chars) - 1
        result = ''
        for i in range(0, length):
            result = result + chars[random.randint(0, maxCharsIndex)]
        return result
