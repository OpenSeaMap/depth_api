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

from error import *


# --------------------------------------------------------------------------------------------------

class Protect(cherrypy.Tool):
    '''
    Use this class to protect exposed methods beeing accessed by unauthorized
    users.

    Protect an exposed method:

      @cherrypy.expose
      @cherrypy.tools.protect()
      def protected(self):
          pass
    '''

    # ----------------------------------------------------------------------------------------------

    def __init__(self):
        self._point    = 'before_request_body'
        self._name     = None
        self._priority = 60
        self.__doc__   = self.callable.__doc__
        self._setargs()

    # ----------------------------------------------------------------------------------------------

    def callable(self):
        authenticated = cherrypy.session.get('authenticated', False)
        if not authenticated:
            raise Error(511, 'Please login to access this method.', 'SERVICE')


# --------------------------------------------------------------------------------------------------

cherrypy.tools.protect = Protect()
