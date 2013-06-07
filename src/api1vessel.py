#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------------------------------
# OpenSeaMap API - Web API for OpenSeaMap services.
#
# Written in 2012 by Dominik Fässler dfa@bezono.org
# Written in 2013 by Dominik Fässler dfa@bezono.org
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

from vessel import *


# --------------------------------------------------------------------------------------------------

class Api1Vessel():
    '''
    Provides vessel management methods.
    '''

    # ----------------------------------------------------------------------------------------------

    def __init__(self, db):
        self._vessel = Vessel(db)

    # ----------------------------------------------------------------------------------------------

    @cherrypy.expose
    @cherrypy.tools.cors()
    @cherrypy.tools.protect()
    @cherrypy.tools.json_out()
    def create(self, name):
        vesselId = self._vessel.create(cherrypy.session.get('username', None), name)
        result = {
            'vesselId' : vesselId
        }
        return result

    # ----------------------------------------------------------------------------------------------

    @cherrypy.expose
    @cherrypy.tools.cors()
    @cherrypy.tools.protect()
    @cherrypy.tools.json_out()
    def set(self, *args, **kwargs):
        vesselId = kwargs.get('vesselId', None)
        if vesselId == None:
            raise Error(805, 'Missing field name \'vesselId\'.', 'VESSEL')
        del kwargs['vesselId']
        self._vessel.setParams(cherrypy.session.get('username', None), vesselId, kwargs)
        result = {
            'success' : True
        }
        return result

    # ----------------------------------------------------------------------------------------------

    @cherrypy.expose
    @cherrypy.tools.cors()
    @cherrypy.tools.protect()
    @cherrypy.tools.json_out()
    def getall(self):
        result = {
            'data' : self._vessel.getByUsername(cherrypy.session.get('username', None))
        }
        return result
