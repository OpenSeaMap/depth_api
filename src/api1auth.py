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
import string
import tempfile


# --------------------------------------------------------------------------------------------------
# Imports internal
# --------------------------------------------------------------------------------------------------

from auth import *
from captcha import *


# --------------------------------------------------------------------------------------------------

class Api1Auth():
    '''
    Provides authentication methods.
    '''

    # ----------------------------------------------------------------------------------------------

    def __init__(self, db):
        self._auth = Auth(db)

    # ----------------------------------------------------------------------------------------------

    @cherrypy.expose
    @cherrypy.tools.cors()
    def captcha(self):
        # Create temporary file. Close fileHandle immediately, beacuse
        # captcha generation overrides file.
        fileHandle, fileName = tempfile.mkstemp()
        os.close(fileHandle)

        captcha = Captcha.generate(fileName)
        cherrypy.session.acquire_lock()
        cherrypy.session['captcha'] = captcha
        cherrypy.session.release_lock()

        fh = open(fileName)
        result = fh.read()
        fh.close()
        os.unlink(fileName)

        cherrypy.response.headers['Content-Type']  = 'image/jpeg'
        cherrypy.response.headers['Cache-Control'] = 'no-cache, must-revalidate'

        return result

    # ----------------------------------------------------------------------------------------------

    @cherrypy.expose
    @cherrypy.tools.cors()
    @cherrypy.tools.json_out()
    def create(self, username, password, captcha):
        sessionCaptcha = cherrypy.session.get('captcha', None)
        if sessionCaptcha == None or captcha != sessionCaptcha:
            # Reset Captcha, user has to get a new one.
            cherrypy.session.acquire_lock()
            cherrypy.session.pop('captcha', None)
            cherrypy.session.release_lock()
            raise Error(801, 'Invalid captcha.', 'AUTH')

        self._validatePassword(password)
        self._auth.create(username, password)
        cherrypy.session.acquire_lock()
        cherrypy.session.pop('captcha', None)
        cherrypy.session.release_lock()

        return {}

    # ----------------------------------------------------------------------------------------------

    @cherrypy.expose
    @cherrypy.tools.cors()
    @cherrypy.tools.protect()
    @cherrypy.tools.json_out()
    def changepassword(self, old, new):
        self._validatePassword(old)
        self._validatePassword(new)
        self._auth.changePassword(cherrypy.session.get('username', None), old, new)

        return {}

    # ----------------------------------------------------------------------------------------------

    def _validatePassword(self, password):
        if len(password) != 40:
            raise Error(802, 'Invalid password hash (sha1).', 'AUTH')
        removeHexDigits = str(password).translate(None, string.hexdigits)
        if len(removeHexDigits) > 0:
            raise Error(802, 'Invalid password hash (sha1).', 'AUTH')

    # ----------------------------------------------------------------------------------------------

    @cherrypy.expose
    @cherrypy.tools.cors()
    @cherrypy.tools.json_out()
    def login(self, username, password):
        result = {}

        authenticated = self._auth.authenticate(username, password)
        cherrypy.session.acquire_lock()
        cherrypy.session['authenticated'] = authenticated
        cherrypy.session['username']      = username
        cherrypy.session.release_lock()

        result['session_id'] = cherrypy.session.id

        return result

    # ----------------------------------------------------------------------------------------------

    @cherrypy.expose
    @cherrypy.tools.cors()
    @cherrypy.tools.json_out()
    def logout(self):
        cherrypy.session.acquire_lock()
        cherrypy.session.clear()
        cherrypy.session.release_lock()

        return {}
