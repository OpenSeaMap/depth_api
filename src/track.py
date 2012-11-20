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
import logging
import os


# --------------------------------------------------------------------------------------------------
# Imports internal
# --------------------------------------------------------------------------------------------------

from error import *


# --------------------------------------------------------------------------------------------------

class Track():
    '''
    This class allows to handle user tracks. Each track becomes an unique
    track id which is referenced to an user. The track file will be
    stored in the file system, while information about the user and state
    will be stored in the database (table user_tracks).

    Each track has an upload state:

      0 : New track, nothing uploaded yet.
      1 : Upload done, track id can not be used for further uploads.

    To have at maximum 100 files in a directory, subdirectories will be
    created automatically. Files from '1.dat' to '99.dat' will reside in
    the subdirectory '000', Files from '100.dat' to '199.dat' will reside
    in '100', ...
    '''


    # ----------------------------------------------------------------------------------------------

    def __init__(self, db):
        self._db  = db
        self._cur = db.getCursor()

        try:
            self._dir = cherrypy.config.get('track.dir', None)
        except ConfigParser.NoOptionError as e:
            raise Exception('Track directory not defined.')

        if self._dir == None:
            raise Exception('Track directory not defined.')

    # ----------------------------------------------------------------------------------------------

    def __del__(self):
        self._cur.close()

    # ----------------------------------------------------------------------------------------------

    def getNewId(self, username):
        self._cur.execute(
            '''
            SELECT nextval('user_tracks_track_id_seq')
            '''
        )
        record = self._cur.fetchone()
        self._db.commit()
        if record == None:
            raise Error(201, 'Unable to fetch new track id.', 'TRACK')
        trackId = record[0]
        self._cur.execute(
            '''
            INSERT INTO user_tracks (track_id, user_name)
            VALUES (%s, %s)
            ''',
            (trackId, username)
        )
        self._db.commit()
        return trackId

    # ----------------------------------------------------------------------------------------------

    def uploadDone(self, trackId, username, fileHandle, fileName):
        assert isinstance(trackId, int)
        assert isinstance(fileHandle, file)
        self._cur.execute(
            '''
            SELECT upload_state
            FROM user_tracks
            WHERE track_id = %s
            AND user_name = %s
            ''',
            (trackId, username)
        )
        record = self._cur.fetchone()
        self._db.commit()
        if record == None:
            raise Error(202, 'Invalid track id.', 'TRACK')
        if record[0] > 0:
            raise Error(203, 'Upload already done.', 'TRACK')

        size = self._storeFile(trackId, fileHandle)

        self._cur.execute(
            '''
            UPDATE user_tracks
            SET file_ref = %s, upload_state = 1
            WHERE track_id = %s
            ''',
            (fileName, trackId)
        )
        self._db.commit()

        return size

    # ----------------------------------------------------------------------------------------------

    def _storeFile(self, trackId, fileHandle):
        size = 0
        fh = open(self._generateFileName(trackId), 'w')
        while True:
            data = fileHandle.read(8192)
            if not data:
                break
            fh.write(data)
            size += len(data)
        fh.close()
        return size

    # ----------------------------------------------------------------------------------------------

    def _generateFileName(self, trackId):
        trackDir  = str(int(round(trackId / 100)) * 100)
        trackFile = str(trackId) + '.dat'
        path = os.path.abspath(self._dir)
        path = os.path.join(path, trackDir.rjust(3, '0'))
        if os.path.exists(path) == False:
            os.makedirs(path)
        filename = os.path.join(path, trackFile)
        return filename;

    # ----------------------------------------------------------------------------------------------

    def getByUsername(self, username):
        self._cur.execute(
            '''
            SELECT track_id, file_ref, upload_state
            FROM user_tracks
            WHERE user_name = %s
            ORDER BY track_id ASC
            ''',
            (username,)
        )
        records = self._cur.fetchall()
        self._db.commit()
        return records
