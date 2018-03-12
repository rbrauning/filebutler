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

from builtins import str
from builtins import object
import datetime
import pytz
import tzlocal

class Localtime(object):

    def __init__(self):
        self._epoch = datetime.datetime.utcfromtimestamp(0)
        self._localtimezone = pytz.timezone(str(tzlocal.get_localzone()))

    def datetime(self, *args):
        return datetime.datetime(*args)

    def t(self, *args):
        dt = self.datetime(*args)
        return (dt - self._epoch).total_seconds()
