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

import cherrypy


# --------------------------------------------------------------------------------------------------
# Imports internal
# --------------------------------------------------------------------------------------------------

from api1auth import *
from api1track import *
from db import *


# --------------------------------------------------------------------------------------------------

class Api1():
    '''
    Provides the root for API version 1.
    '''

    # ----------------------------------------------------------------------------------------------

    def __init__(self):
        self._db   = Db()
        self.auth  = Api1Auth(self._db)
        self.track = Api1Track(self._db)

    # ----------------------------------------------------------------------------------------------

    @cherrypy.expose
    def index(self):
        return 'OpenSeaMap API v1.1'
