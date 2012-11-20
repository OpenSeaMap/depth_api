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
import json

from cherrypy._cpcompat import ntob
from cherrypy._cperror import _be_ie_unfriendly


# --------------------------------------------------------------------------------------------------

class Error(cherrypy.HTTPError):
    '''
    A general error class which supports code and message. The message
    can contain params in curly brackets.
    '''


    # ----------------------------------------------------------------------------------------------

    def __init__(self, code, msg, context='', severity=20, paramDict={}):
        '''
        Log each error and create a HTTPError object.
        '''
        msg = self.__replaceParams(msg, paramDict)
        cherrypy.log.error(('Error %s: %s' % (code, msg)), context, severity)
        msg = json.dumps({
            'code' : code,
            'msg'  : msg
        })
        cherrypy.HTTPError.__init__(self, 409, msg)


    # ----------------------------------------------------------------------------------------------

    def __replaceParams(self, msg, paramDict):
        '''
        Replaces params surrounded with curly brackets with params from
        a dictionary.
        '''
        for k, v in paramDict.iteritems():
            msg = msg.replace('{' + k + '}', v)
        return msg


    # ----------------------------------------------------------------------------------------------

    def set_response(self):
        '''
        Override parents set_response method, because a JSON object must
        be returned.
        '''
        cherrypy.HTTPError.set_response(self)
        cherrypy.serving.response.headers['Content-Type'] = 'application/json;charset=utf-8'
        cherrypy.serving.response.body = ntob(self._message)
        _be_ie_unfriendly(self.code)
