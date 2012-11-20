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
import datetime
import hashlib
import random


# --------------------------------------------------------------------------------------------------
# Imports internal
# --------------------------------------------------------------------------------------------------

from error import *


# --------------------------------------------------------------------------------------------------

class Auth():

    # ----------------------------------------------------------------------------------------------

    def __init__(self, db):
        self._db  = db
        self._cur = db.getCursor()

        self._maxUnsuccessfulAttempts = 3
        self._blockForMinutes         = 3

    # ----------------------------------------------------------------------------------------------

    def __del__(self):
        self._cur.close()

    # ----------------------------------------------------------------------------------------------

    def authenticate(self, username, password):
        '''
        Authenticates user account. The account will be blocked for '_blockForMinutes' if the
        maximum attempts '_maxUnsuccessfulAttempts' is reached.
        '''
        username = self._hashUsername(username)
        self._cur.execute(
            '''
            SELECT password, salt, attempts, last_attempt
            FROM user_profiles
            WHERE user_name = %s
            ''',
            (username,)
        )
        record = self._cur.fetchone()
        self._db.commit()
        if record == None:
            raise Error(101, 'Username or password wrong.', 'AUTH')
        if record[2] >= self._maxUnsuccessfulAttempts:
            nextPossibleAttempt = record[3] + datetime.timedelta(0, 0, 0, 0, self._blockForMinutes)
            if nextPossibleAttempt > datetime.datetime.utcnow():
                raise Error(102, 'Account temporarily blocked.', 'AUTH')
        saltedPassword = self._saltPassword(password, record[1])
        if saltedPassword != record[0]:
            attempts = record[2] + 1
            if attempts <= self._maxUnsuccessfulAttempts:
                now = str(datetime.datetime.utcnow())[:19]
                self._updateAttempts(username, attempts, now)
            raise Error(101, 'Username or password wrong.', 'AUTH')
        else:
            now = str(datetime.datetime.utcnow())[:19]
            self._updateAttempts(username, 0, now)
            return True

    # ----------------------------------------------------------------------------------------------

    def create(self, username, password):
        username = self._hashUsername(username)
        self._cur.execute(
            '''
            SELECT count(*)
            FROM user_profiles
            WHERE user_name = %s
            ''',
            (username,)
        )
        record = self._cur.fetchone()
        self._db.commit()
        if record[0] > 0:
            raise Error(103, 'Username already exists.', 'AUTH')
        self._cur.execute(
            '''
            INSERT INTO user_profiles
            (user_name, password, salt)
            VALUES (%s, '*', '')
            ''',
            (username,)
        )
        self._db.commit()
        self._setPassword(username, password)

    # ----------------------------------------------------------------------------------------------

    def changePassword(self, username, oldPassword, newPassword):
        username = self._hashUsername(username)
        self._cur.execute(
            '''
            SELECT password, salt
            FROM user_profiles
            WHERE user_name = %s
            ''',
            (username,)
        )
        record = self._cur.fetchone()
        self._db.commit()
        if record == None:
            raise Error(101, 'Username or password wrong.', 'AUTH')
        saltedPassword = self._saltPassword(oldPassword, record[1])
        if saltedPassword != record[0]:
            raise Error(101, 'Username or password wrong.', 'AUTH')
        else:
            self._setPassword(username, newPassword)


    # ----------------------------------------------------------------------------------------------

    def _hashUsername(self, username):
        h = hashlib.sha1(username)
        return h.hexdigest()


    # ----------------------------------------------------------------------------------------------

    def _setPassword(self, username, password):
        salt = self._getNewSalt()
        saltedPassword = self._saltPassword(password, salt)
        self._cur.execute(
            '''
            UPDATE user_profiles
            SET password = %s, salt = %s
            WHERE user_name = %s
            ''',
            (saltedPassword, salt, username)
        )
        self._db.commit()


    # ----------------------------------------------------------------------------------------------

    def _getNewSalt(self):
        c = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        s = '';
        for i in range(0, 10):
            s = s + random.choice(c)
        return s


    # ----------------------------------------------------------------------------------------------

    def _saltPassword(self, password, salt):
        h = hashlib.sha1(password + salt)
        return h.hexdigest()


    # ----------------------------------------------------------------------------------------------

    def _updateAttempts(self, username, attempts, lastAttempt):
        self._cur.execute(
            '''
            UPDATE user_profiles
            SET attempts = %s, last_attempt = %s
            WHERE user_name = %s
            ''',
            (attempts, lastAttempt, username)
        )
        self._db.commit()


    # ----------------------------------------------------------------------------------------------

    def removeAllProfiles(self):
        self._cur.execute(
            '''
            DELETE FROM user_profiles
            '''
        )
        self._db.commit()
