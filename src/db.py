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
import psycopg2
import psycopg2.extras


# --------------------------------------------------------------------------------------------------

class Db:
    '''
    Database helper class
    '''

    # ----------------------------------------------------------------------------------------------

    conn = None

    # ----------------------------------------------------------------------------------------------

    def __init__(self):
        self._connect()

    # ----------------------------------------------------------------------------------------------

    def __del__(self):
        self._disconnect()

    # ----------------------------------------------------------------------------------------------

    def _connect(self):
        dbHost     = cherrypy.config.get('db.host', 'localhost')
        dbPort     = cherrypy.config.get('db.port', '5432')
        dbName     = cherrypy.config.get('db.name', '')
        dbUser     = cherrypy.config.get('db.user', '')
        dbPassword = cherrypy.config.get('db.password', '')
        connStr    = 'host=%s port=%s dbname=%s user=%s password=%s' % \
                     (dbHost, dbPort, dbName, dbUser, dbPassword)
        self.conn = psycopg2.connect(connStr)
        psycopg2.extras.register_hstore(self.conn)

    # ----------------------------------------------------------------------------------------------

    def _disconnect(self):
        if self.conn:
            self.conn.close()

    # ----------------------------------------------------------------------------------------------

    def getCursor(self):
        cursor = self.conn.cursor()
        cursor.execute("SET TIME ZONE 'UTC';")
        return cursor

    # ----------------------------------------------------------------------------------------------

    def commit(self):
        self.conn.commit()
