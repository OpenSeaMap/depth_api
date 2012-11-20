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
import logging
import sys


# --------------------------------------------------------------------------------------------------
# Imports internal
# --------------------------------------------------------------------------------------------------

from cherry_asyncfileupload import *
from cherry_cors import *
from cherry_options import *
from cherry_protect import *
from api1 import *
from error import *


# --------------------------------------------------------------------------------------------------

class Root:

    _cp_config = {
        'tools.staticdir.on'   : True,
        'tools.staticdir.root' : os.path.join(os.path.dirname(os.path.realpath(__file__)), 'public'),
        'tools.staticdir.dir'  : ''
    }


    @cherrypy.expose
    def index(self):
        return "Welcome on OpenSeaMap services."


    @cherrypy.tools.cors()
    def handleError(self):
        exctype, e = sys.exc_info()[:2]
        r = cherrypy.response
        r.status = 409
        r.headers['Access-Control-Allow-Credentials'] = 'true'
        r.headers['Access-Control-Allow-Methods']     = 'POST, GET, OPTIONS'
        r.headers['Access-Control-Allow-Origin']      = cherrypy.config.get('cors.origin')
        r.headers['Content-Type']                     = 'application/json;charset=utf-8'
        r.body = json.dumps({
            'code' : 999,
            'msg'  : 'An error occured.'
        })
        cherrypy.log.error(cherrypy._cperror.format_exc(), 'SERVICE', logging.ERROR)


# --------------------------------------------------------------------------------------------------

cherrypy.config.update('site.conf')

cherrypy.log.access_log.setLevel(cherrypy.config.get('log.level'))
cherrypy.log.error_log.setLevel(cherrypy.config.get('log.level'))

root = Root()
root.api1 = Api1()

cherrypy.config.update({
    'engine.autoreload_on'   : False,
    'request.error_response' : root.handleError
})

cherrypy.tree.mount(root, '/', 'site.conf')
