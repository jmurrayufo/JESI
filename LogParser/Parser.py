import copy
import datetime
from collections import defaultdict

from . import Row

class Parser:

    def __init__(self, log_path):
        self.log_path = log_path


    def parse(self, time_boxes):
        """
        Accept list of time buckets to fill. Return a dict 
        """

        self.time_boxes = list(time_boxes)

        # Init data array
        self.data = defaultdict(lambda: 
            {
                'damage_to':0,
                'damage_from':0,
                'damage_ship_to':defaultdict(lambda: 0),
                'damage_ship_from':defaultdict(lambda: 0),
                'damage_type_to':defaultdict(lambda: 0),
                'damage_type_from':defaultdict(lambda: 0),
                'damage_system_to':defaultdict(lambda: 0),
                'damage_system_from':defaultdict(lambda: 0)
            }
        )

        # self.timeboxes.append(datetime.timedelta.max)

        self.now = datetime.datetime.now() + datetime.timedelta(hours=6)

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
        for time_delta in self.time_boxes:
            self.data[time_delta]['damage_ship_to'] = dict(sorted(self.data[time_delta]['damage_ship_to'].items(), key=lambda kv: kv[1], reverse=True))
            self.data[time_delta]['damage_ship_from'] = dict(sorted(self.data[time_delta]['damage_ship_from'].items(), key=lambda kv: kv[1], reverse=True))

            self.data[time_delta]['damage_type_to'] = dict(sorted(self.data[time_delta]['damage_type_to'].items(), key=lambda kv: kv[1], reverse=True))
            self.data[time_delta]['damage_type_from'] = dict(sorted(self.data[time_delta]['damage_type_from'].items(), key=lambda kv: kv[1], reverse=True))

            self.data[time_delta]['damage_system_to'] = dict(sorted(self.data[time_delta]['damage_system_to'].items(), key=lambda kv: kv[1], reverse=True))
            self.data[time_delta]['damage_system_from'] = dict(sorted(self.data[time_delta]['damage_system_from'].items(), key=lambda kv: kv[1], reverse=True))


    def _parse_to(self, r):
        for time_delta in self.time_boxes:
            if self.now - r.datetime < time_delta:
                self.data[time_delta]['damage_to'] += r.amount
                self.data[time_delta]['damage_ship_to'][r.source_target] += r.amount
                self.data[time_delta]['damage_type_to'][r.damage_type] += r.amount
                self.data[time_delta]['damage_system_to'][r.system] += r.amount

    def _parse_from(self, r):
        for time_delta in self.time_boxes:
            if self.now - r.datetime < time_delta:
                self.data[time_delta]['damage_from'] += r.amount
                self.data[time_delta]['damage_ship_from'][r.source_target] += r.amount
                self.data[time_delta]['damage_type_from'][r.damage_type] += r.amount
                self.data[time_delta]['damage_system_from'][r.system] += r.amount




