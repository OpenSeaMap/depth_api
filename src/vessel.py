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
import logging
import psycopg2


# --------------------------------------------------------------------------------------------------
# Imports internal
# --------------------------------------------------------------------------------------------------

from error import *


# --------------------------------------------------------------------------------------------------

class Vessel():
    '''
    This class allows to handle user vessels. A vessel has its settings
    stored as param->value pairs.
    '''


    # ----------------------------------------------------------------------------------------------

    _allowedParams = {
        'name'        : [ 'string', 1,  50 ],
        'description' : [ 'string', 1, 500 ]
    }

    # ----------------------------------------------------------------------------------------------

    def __init__(self, db):
        self._db  = db
        self._cur = db.getCursor()

    # ----------------------------------------------------------------------------------------------

    def __del__(self):
        self._cur.close()

    # ----------------------------------------------------------------------------------------------

    def create(self, username, name):
        assert len(username) > 0
        assert len(name) > 0
        self._cur.execute(
            '''
            SELECT count(*)
            FROM user_vessels
            WHERE user_name = %s
            AND (settings->'name') = %s
            ''',
            (username, name)
        )
        record = self._cur.fetchone()
        if record[0] > 0:
            self._db.commit()
            raise Error(204, 'Vessel name already exists.', 'VESSEL')
        self._cur.execute(
            '''
            INSERT INTO user_vessels (user_name, settings)
            VALUES (%s, hstore('name' => %s))
            RETURNING vessel_id
            ''',
            (username, name)
        )
        record = self._cur.fetchone()
        vesselId = record[0]
        self._db.commit()
        return vesselId

    # ----------------------------------------------------------------------------------------------

    def setParams(self, username, vesselId, params):
        for param, value in params.iteritems():
            self._setParam(username, vesselId, param, value)
        self._db.commit()

    # ----------------------------------------------------------------------------------------------

    def _setParam(self, username, vesselId, param, value):
        self._valueValid(param, value)
        try:
            self._cur.execute(
                '''
                UPDATE user_vessels
                SET settings = settings || (%s => %s)
                WHERE vessel_id = %s
                AND user_name = %s
                RETURNING vessel_id
                ''',
                (param, str(value), vesselId, username)
            )
            if self._cur.fetchone() == None:
                raise Error(207, 'Invalid vessel ID.', 'VESSEL')
        except psycopg2.IntegrityError as e:
            raise Error(204, 'Vessel name already exists.', 'VESSEL')

    # ----------------------------------------------------------------------------------------------

    def _paramValid(self, param):
        if self._allowedParams.has_key(param) == False:
            raise Error(205, 'Invalid param \'{param}\'.', 'VESSEL', logging.WARNING, {
                'param' : param
            })

    # ----------------------------------------------------------------------------------------------

    def _valueValid(self, param, value):
        self._paramValid(param)

        (valType, valMin, valMax) = self._allowedParams.get(param)

        if valType == 'string':
            if len(value) < valMin or len(value) > valMax:
                raise Error(206, 'Invalid param format \'{param}\'.', 'VESSEL', logging.WARNING, {
                    'param' : param
                })
            return
        else:
            raise Exception('Invalid validation type.')

    # ----------------------------------------------------------------------------------------------

    def getByUsername(self, username):
        self._cur.execute(
            '''
            SELECT vessel_id, settings
            FROM user_vessels
            WHERE user_name = %s
            ORDER BY (settings -> 'name') ASC
            ''',
            (username,)
        )
        result = []
        for vesselId, settings in self._cur:
            settings['vesselId'] = vesselId
            result.append(settings)
        self._db.commit()
        return result

    # ----------------------------------------------------------------------------------------------

    def removeAll(self):
        self._cur.execute(
            '''
            DELETE FROM user_vessels
            '''
        )
        self._db.commit()
