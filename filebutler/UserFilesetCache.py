# Copyright 2017 Simon Guest
#
# This file is part of filebutler.
#
# Filebutler is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Filebutler is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with filebutler.  If not, see <http://www.gnu.org/licenses/>.

import os.path

class UserFilesetCache(object):

    def __init__(self, path, next):
        self._path = path
        self._next = next
        self._users = {}        # of fileset, indexed by integer user

        # load stubs for all users found
        if os.path.exists(self._path):
            for u in os.listdir(self._path):
                self._users[u] = None # stub

    def _subpath(self, u):
        return os.path.join(self._path, u)

    def _fileset(self, u):
        """On demand creation of child filesets."""
        if self._users.has_key(u):
            fileset = self._users[u]
        else:
            fileset = None
        if fileset is None:
            fileset = self._next(self._subpath(u))
            self._users[u] = fileset
        return fileset

    def select(self, filter=None):
        users = sorted(self._users.keys())
        for u in users:
            if filter is None or filter.owner is None or u == filter.owner:
                # no yield from in python 2, so:
                for filespec in self._fileset(u).select(filter):
                    yield filespec

    def create(self):
        if not os.path.exists(self._path):
            os.makedirs(self._path)

    def add(self, filespec):
        fileset = self._fileset(filespec.user)
        fileset.add(filespec)

    def flush(self):
        for fileset in self._users.values():
            fileset.flush()

