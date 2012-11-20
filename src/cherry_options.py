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

class Options(cherrypy.Tool):
    '''
    This tool redirects requests with 'OPTIONS' as request method. It
    is a internal redirection, therefore the client does not notice
    about this redirection.

    E.g.: '/api/upload' -> '/api/upload_OPTIONS'
    '''

    # ----------------------------------------------------------------------------------------------

    def __init__(self):
        self._point    = 'on_start_resource'
        self._name     = None
        self._priority = 50
        self.__doc__   = self.callable.__doc__
        self._setargs()

    # ----------------------------------------------------------------------------------------------

    def callable(self):
        if cherrypy.request.method.upper() == 'OPTIONS':
            raise cherrypy.InternalRedirect(cherrypy.request.path_info + '_OPTIONS')


# --------------------------------------------------------------------------------------------------

cherrypy.tools.options = Options()
