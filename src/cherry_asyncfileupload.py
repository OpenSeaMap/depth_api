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

class AsyncFileUploadPart(cherrypy._cpreqbody.Part):

    # ----------------------------------------------------------------------------------------------

    def default_proc(self):
        trackId = cherrypy.request.headers.get('X-Track-Id', None)
        size    = cherrypy.request.headers.get('Content-Length', 0)
        cherrypy.tools.asyncfileupload.registerFp(trackId, self.fp, size)
        super(AsyncFileUploadPart, self).default_proc()
        cherrypy.tools.asyncfileupload.unregisterFp(trackId)


# --------------------------------------------------------------------------------------------------

class AsyncFileUpload(cherrypy.Tool):

    # ----------------------------------------------------------------------------------------------

    def __init__(self):
        self._point       = 'on_start_resource'
        self._name        = None
        self._priority    = 60
        self.__doc__      = self.callable.__doc__
        self._actualFiles = {}
        self._setargs()

    # ----------------------------------------------------------------------------------------------

    def callable(self):
        request = cherrypy.request
        if request.headers.get('X-Track-Id', None) == None:
            raise Error(803, 'Header X-Track-Id not set.', 'TRACK')
        request.body.part_class = AsyncFileUploadPart

    # ----------------------------------------------------------------------------------------------

    def registerFp(self, trackId, fp, size):
        key = self._generateKey(trackId)
        self._actualFiles[key]         = {}
        self._actualFiles[key]['fp']   = fp
        self._actualFiles[key]['size'] = size

    # ----------------------------------------------------------------------------------------------

    def unregisterFp(self, trackId):
        key = self._generateKey(trackId)
        del self._actualFiles[key]

    # ----------------------------------------------------------------------------------------------

    def getState(self, trackId):
        result = {
            'sizeExpected' : None,
            'sizeUploaded' : None
        }
        key = self._generateKey(trackId)
        if key in self._actualFiles:
            result['sizeExpected'] = self._actualFiles[key]['size']
            result['sizeUploaded'] = self._actualFiles[key]['fp'].bytes_read
        return result

    # ----------------------------------------------------------------------------------------------

    def _generateKey(self, trackId):
        return cherrypy.session.id + '_' + trackId


# --------------------------------------------------------------------------------------------------

cherrypy.tools.asyncfileupload = AsyncFileUpload()
