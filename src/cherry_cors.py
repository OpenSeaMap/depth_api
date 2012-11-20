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

class Cors(cherrypy.Tool):
    '''
    The 'Access-Control-Allow-*' headers permits the browser to do
    cross site requests. For further information see:
    'http://www.html5rocks.com/en/tutorials/cors'
    '''

    # ----------------------------------------------------------------------------------------------

    def __init__(self):
        self._point    = 'before_finalize'
        self._name     = None
        self._priority = 50
        self.__doc__   = self.callable.__doc__
        self._setargs()

    # ----------------------------------------------------------------------------------------------

    def callable(self):
        r = cherrypy.response
        r.headers['Access-Control-Allow-Credentials'] = 'true'
        r.headers['Access-Control-Allow-Headers']     = 'X-Track-Id'
        r.headers['Access-Control-Allow-Methods']     = 'POST, GET, OPTIONS'
        r.headers['Access-Control-Allow-Origin']      = cherrypy.config.get('cors.origin')


# --------------------------------------------------------------------------------------------------

cherrypy.tools.cors = Cors()
