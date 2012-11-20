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
#
# EXCEPTIONS:
# - class Captcha (see details below)
# --------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------
# Imports external
# --------------------------------------------------------------------------------------------------

import Image
import ImageFont
import ImageDraw
import ImageFilter
import random
import os


# --------------------------------------------------------------------------------------------------
# Imports internal
# --------------------------------------------------------------------------------------------------

from utils import *


# --------------------------------------------------------------------------------------------------

class Captcha():
    '''
    The code of this class was copied from the following URL:

      <http://code.activestate.com/recipes/440588-human-verification-test-captcha/>

    Due to the fact that there is no license header in the code and there is a machine tag
    'meta:license=psf' on the site I assume it is licensed under the 'Python-Software-Foundation-
    License'.

    This is not the original code. It is modified.
    '''

    # ----------------------------------------------------------------------------------------------

    @staticmethod
    def generate(fileName, text=None):
        '''Generate a captcha image'''
        # text
        if text == None:
            text = Utils.generateRandomStringContainingLettersAndDigits(6)
        # image size
        imageWidth  = 150
        imageHeight = 50
        # randomly select the foreground color
        fgcolor = random.randint(0, 0xffff00)
        # make the background color the opposite of fgcolor
        bgcolor = fgcolor ^ 0xffffff
        # create a new image slightly larger that the text
        im = Image.new('RGB', (imageWidth, imageHeight), bgcolor)
        d = ImageDraw.Draw(im)
        x, y = im.size
        r = random.randint
        # draw 100 random colored boxes on the background
        for num in range(100):
            d.rectangle((r(0,x),r(0,y),r(0,x),r(0,y)),fill=r(0,0xffffff))
        # add the text to the image
        sourceFilePath = os.path.dirname(os.path.abspath(__file__))
        fontFile = os.path.join(sourceFilePath, 'porkys.ttf')
        font = ImageFont.truetype(fontFile, 32)
        dim = font.getsize(text)
        position = (((imageWidth - dim[0]) / 2),((imageHeight - dim[1]) / 2))
        d.text(position, text, font=font, fill=fgcolor)
        im = im.filter(ImageFilter.EDGE_ENHANCE_MORE)
        # save the image to a file
        im.save(fileName, format='JPEG')
        return text
