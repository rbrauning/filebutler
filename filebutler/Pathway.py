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

import grp
import pwd
import re
import string

class Pathway(object):

    def __init__(self):
        self._datasetRegex = None
        self._datasetReplace = None
        self._ignorePathRegexes = []

    def setDatasetRegex(self, datasetRegex, datasetReplace):
        self._datasetRegex = re.compile(datasetRegex)
        self._datasetReplace = datasetReplace

    def clearDatasetRegex(self):
        self._datasetRegex = None
        self._datasetReplace = None

    def datasetFromPath(self, path):
        noDatasetFound = '-'
        if self._datasetRegex is None:
            return noDatasetFound
        dataset, n = re.subn(self._datasetRegex, self._datasetReplace, path, 1)
        if n == 1:
            return dataset
        else:
            return noDatasetFound

    def setIgnorePathsFrom(self, ignorefilepath):
        self._ignorePathRegexes = []
        with open(ignorefilepath) as f:
            for line in f:
                i_hash = string.find(line, '#')
                if i_hash != -1:
                    regex = line[:i_hash].strip()
                else:
                    regex = line.strip()
                if regex != '':
                    self._ignorePathRegexes.append(re.compile(regex))

    def ignored(self, path):
        for r in self._ignorePathRegexes:
            if re.search(r, path):
                return True
        return False
