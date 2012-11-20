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

from track import *


# --------------------------------------------------------------------------------------------------

class Api1Track():
    '''
    Provides track upload methods.
    '''

    # ----------------------------------------------------------------------------------------------

    def __init__(self, db):
        self._track = Track(db)

    # ----------------------------------------------------------------------------------------------

    @cherrypy.expose
    @cherrypy.tools.cors()
    @cherrypy.tools.protect()
    @cherrypy.tools.json_out()
    def newid(self):
        result = {}
        result['trackId'] = self._track.getNewId(cherrypy.session.get('username', None))
        return result

    # ----------------------------------------------------------------------------------------------

    @cherrypy.expose
    @cherrypy.tools.cors()
    def upload_OPTIONS(self):
        '''
        This method is required because some browsers (e.g. Firefox) first
        do a request with 'OPTIONS' as request method. We don't have to
        return anything, the 'cors' tool sets required headers for us.

        CAUTION: Do not set the 'protect' tool for this method. The request
        does not include a session cookie.
        '''
        return ''

    # ----------------------------------------------------------------------------------------------

    @cherrypy.expose
    @cherrypy.tools.options()
    @cherrypy.tools.protect()
    @cherrypy.tools.asyncfileupload()
    @cherrypy.tools.cors()
    @cherrypy.tools.json_out()
    def upload(self, *args, **kwargs):
        # Tool asyncfileupload checks, if the header is there.
        trackId = cherrypy.request.headers.get('X-Track-Id', None)
        trackId = int(trackId)

        track = kwargs.get('track', None)
        if track == None:
            raise Error(804, 'Missing field name \'track\'.', 'TRACK')

        size = self._track.uploadDone(trackId, cherrypy.session.get('username', None), \
            track.file, track.filename)

        result = {}
        result['length']  = size

        return result

    # ----------------------------------------------------------------------------------------------

    @cherrypy.expose
    @cherrypy.tools.cors()
    @cherrypy.tools.protect()
    @cherrypy.tools.json_out()
    def status(self):
        trackId = cherrypy.request.headers.get('X-Track-Id', None)
        return cherrypy.tools.asyncfileupload.getState(trackId)

    # ----------------------------------------------------------------------------------------------

    @cherrypy.expose
    @cherrypy.tools.cors()
    @cherrypy.tools.protect()
    @cherrypy.tools.json_out()
    def getall(self):
        return self._track.getByUsername(cherrypy.session.get('username', None))
