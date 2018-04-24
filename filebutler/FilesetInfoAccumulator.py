from __future__ import absolute_import
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
from .util import str2size, size2str, warning
from .Buckets import Buckets
from .FilesetInfo import FilesetInfo

class FilesetInfoAccumulator(object):

    def __init__(self, attrs):
        self._total = FilesetInfo()
        self._users = {}
        self._datasets = {}
        self._sizebuckets = Buckets([str2size(s) for s in attrs['sizebuckets']] if 'sizebuckets' in attrs else [])
        self._sizes = [None] * self._sizebuckets.len

    def add(self, filespec):
        self._total.add(1, filespec.size)

        # user
        if filespec.user in self._users:
            user = self._users[filespec.user]
        else:
            user = FilesetInfo()
            self._users[filespec.user] = user
        user.add(1, filespec.size)

        # dataset
        if filespec.dataset in self._datasets:
            dataset = self._datasets[filespec.dataset]
        else:
            dataset = FilesetInfo()
            self._datasets[filespec.dataset] = dataset
        dataset.add(1, filespec.size)

        # size
        i = self._sizebuckets.indexContaining(filespec.size)
        sizes0 = self._sizes[i]
        if sizes0 is None:
            sizes0 = FilesetInfo()
            self._sizes[i] = sizes0
        sizes0.add(1, filespec.size)

    def accumulate(self, info, sel):
        self._total.add(info.nFiles, info.totalSize)
        if sel.owner is not None:
            if sel.owner not in self._users:
                user0 = FilesetInfo()
                self._users[sel.owner] = user0
            else:
                user0 = self._users[sel.owner]
            user0.add(info.nFiles, info.totalSize)
        if sel.dataset is not None:
            if sel.dataset not in self._datasets:
                dataset0 = FilesetInfo()
                self._datasets[sel.dataset] = dataset0
            else:
                dataset0 = self._datasets[sel.dataset]
            dataset0.add(info.nFiles, info.totalSize)
        if sel.sizebucket is not None:
            i = self._sizebuckets.index(sel.sizebucket)
            sizes0 = self._sizes[i]
            if sizes0 is None:
                sizes0 = FilesetInfo()
                self._sizes[i] = sizes0
            sizes0.add(info.nFiles, info.totalSize)

    def decumulate(self, info, sel):
        self._total.remove(info.nFiles, info.totalSize)
        if sel.owner is not None:
            if sel.owner in self._users:
                user0 = self._users[sel.owner]
                user0.remove(info.nFiles, info.totalSize)
                if user0.nFiles == 0:
                    # remove user, since no files left
                    self._users.pop(sel.owner, None)
        if sel.dataset is not None:
            if sel.dataset in self._datasets:
                dataset0 = self._datasets[sel.dataset]
                dataset0.remove(info.nFiles, info.totalSize)
                if dataset0.nFiles == 0:
                    # remove dataset, since no files left
                    self._datasets.pop(sel.dataset, None)
        if sel.sizebucket is not None:
            i = self._sizebuckets.index(sel.sizebucket)
            sizes0 = self._sizes[i]
            sizes0.remove(info.nFiles, info.totalSize)
            if sizes0.nFiles == 0:
                # remove sizes, since no files left
                self._sizes[i] = None

    def fmt_total(self):
        return "total %s" % str(self._total)

    def fmt_users(self):
        lines = [self.fmt_total()]
        for user in sorted(list(self._users.items()), key=lambda u: u[1].totalSize, reverse=True):
            name = user[0]
            info = user[1]
            # exclude trivial small stuff
            if info.totalSize > 1024:
                lines.append("%s %s" % (name, str(info)))
        return '\n'.join(lines)

    def iterusers(self):
        return iter(self._users.items())

    def fmt_datasets(self):
        lines = [self.fmt_total()]
        for dataset in sorted(list(self._datasets.items()), key=lambda u: u[1].totalSize, reverse=True):
            name = dataset[0]
            info = dataset[1]
            # exclude trivial small stuff
            if info.totalSize > 1024:
                lines.append("%s %s" % (name, str(info)))
        return '\n'.join(lines)

    def fmt_sizes(self):
        lines = [self.fmt_total()]
        last = len(self._sizes) - 1
        for i in range(last + 1):
            if self._sizes[i] is not None:
                info = self._sizes[i]
                # exclude trivial small stuff
                if info.totalSize > 1024:
                    if i < last:
                        interval = "[%s, %s)" % (size2str(self._sizebuckets.bound(i)), size2str(self._sizebuckets.bound(i + 1)))
                    else:
                        interval = "[%s, .)" % size2str(self._sizebuckets.bound(i))
                    lines.append("%-11s %s" % (interval, str(info)))
        return '\n'.join(lines)
