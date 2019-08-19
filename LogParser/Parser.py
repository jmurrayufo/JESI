import copy
import datetime
from collections import defaultdict

from . import Row

class Parser:

    def __init__(self, log_path):
        self.log_path = log_path


    def parse(self):
        self._to = 0
        self._from = 0

        self._to_1min = 0
        self._from_1min = 0

        self._to_5min = 0
        self._from_5min = 0

        self._to_30min = 0
        self._from_30min = 0

        self._to_60min = 0
        self._from_60min = 0

        self._targets_60min = defaultdict(lambda: 0)
        self._sources_60min = defaultdict(lambda: 0)

        self._type_to_60min = defaultdict(lambda: 0)
        self._type_from_60min = defaultdict(lambda: 0)

        self._system_to_60min = defaultdict(lambda: 0)
        self._system_from_60min = defaultdict(lambda: 0)

        self.now = datetime.datetime.now() + datetime.timedelta(hours=6)
        self._1min = datetime.timedelta(minutes=1)
        self._5min = datetime.timedelta(minutes=5)
        self._30min = datetime.timedelta(minutes=30)
        self._60min = datetime.timedelta(minutes=60)

        self._first_dt = None
        self._last_dt = copy.copy(self.now)
        with open(self.log_path, 'r') as fp:
            for line in fp:
                # print(line,end='')
                r = Row.Row(line)

                if self._first_dt is None and r is not None:
                    self._first_dt = r.datetime

                if type(r) is not Row.Combat:
                    continue
                self._last_dt = r.datetime

                if r.to:
                    self._parse_to(r)
                else:
                    self._parse_from(r)
        if self._first_dt == None:        
            self._first_dt = copy.copy(self.now)

        # Sort various dicts

        self._targets_60min = dict(sorted(self._targets_60min.items(), key=lambda kv: kv[1], reverse=True))
        self._sources_60min = dict(sorted(self._sources_60min.items(), key=lambda kv: kv[1], reverse=True))

        self._type_to_60min = dict(sorted(self._type_to_60min.items(), key=lambda kv: kv[1], reverse=True))
        self._type_from_60min = dict(sorted(self._type_from_60min.items(), key=lambda kv: kv[1], reverse=True))

        self._system_to_60min = dict(sorted(self._system_to_60min.items(), key=lambda kv: kv[1], reverse=True))
        self._system_from_60min = dict(sorted(self._system_from_60min.items(), key=lambda kv: kv[1], reverse=True))


    def _parse_to(self, r):
        self._to += r.amount
        if self.now - r.datetime < self._1min:
            self._to_1min  += r.amount
        if self.now - r.datetime < self._5min:
            self._to_5min += r.amount
        if self.now - r.datetime < self._30min:
            self._to_30min += r.amount
        if self.now - r.datetime < self._60min:
            self._to_60min += r.amount
        if self.now - r.datetime < self._60min:
            self._targets_60min[r.source_target] += r.amount
            self._type_to_60min[r.damage_type] += r.amount
            self._system_to_60min[r.system] += r.amount

    def _parse_from(self, r):
        self._from += r.amount
        if self.now - r.datetime < self._1min:
            self._from_1min  += r.amount
        if self.now - r.datetime < self._5min:
            self._from_5min += r.amount
        if self.now - r.datetime < self._30min:
            self._from_30min += r.amount
        if self.now - r.datetime < self._60min:
            self._from_60min += r.amount
        if self.now - r.datetime < self._60min:
            self._sources_60min[r.source_target] += r.amount
            self._type_from_60min[r.damage_type] += r.amount
            self._system_from_60min[r.system] += r.amount




