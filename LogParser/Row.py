import re
import datetime

class Row:
    """
    Parse row of a log, present data about it.
    """



    def __new__(cls, line):

        re_matchers = {}
        re_matchers['base'] = r"""
            \[\s
            (\d{4}\.\d{2}\.\d{2})  # Date
            \s*
            (\d{2}:\d{2}:\d{2})    # Time
            \s\]
            \s*
            \((\w+)\)               # Log Type
            \s*
        """
        re_matchers['combat_hit'] = r"""
            {}
            <color=0x\w+>
            <b>(\d+)</b>            # Amount
            \s
            <color=0x\w+>
            <font\ size=\d+>
            (to|from)               # To or From
            </font>
            \s
            <b><color=0x\w+>
            (.*)                    # Source/Target
            </b><font\ size=\d+><color=0x\w+>
            \s-\s
            (?:(.*)                    # Weapon System
            \s-\s)?
            (.*)                    # Hit description
        """.format(re_matchers['base'])
        re_matchers['generic'] = "{}".format(re_matchers['base'])
        # print(re.match(Row.re_matchers['datetime'], line))
        # print(re.search(Row.re_matchers['log_type'], line))
        # print(re_matchers['datetime']+r"\ +"+re_matchers['log_type'])
        if not re.search(re_matchers['base'], line, re.X):
            return None
        match_object = re.search(re_matchers['combat_hit'], line, re.X)
        if match_object:
            # print(line)
            return Combat(match_object)
        match_object = re.search(re_matchers['generic'], line, re.X)
        if match_object and match_object.group(3) in ['notify', 'question', 'None', 'warning']:
            return Generic(match_object)
        # print(re_matchers['combat_hit'])
        return Unknown(match_object)


class Combat:
    pass
    def __init__(self, match_object):

        self.date = match_object.group(1)
        self.time = match_object.group(2)

        dt_string = f"{self.date} {self.time}"
        self.datetime = datetime.datetime.strptime(dt_string, "%Y.%m.%d %H:%M:%S")

        self.amount = int(match_object.group(4))
        self.to = match_object.group(5) == 'to'
        self.source_target = match_object.group(6)
        self.system = match_object.group(7)
        # TODO: Parse this into meantingful data!
        self.damage_type = 'Unknown'

    def __str__(self):
        return f"{self.datetime} {self.amount} {'to' if self.to else 'from'} @ {self.source_target} "

class Unknown:
    def __init__(self, match_object):

        self.date = match_object.group(1)
        self.time = match_object.group(2)

        dt_string = f"{self.date} {self.time}"
        self.datetime = datetime.datetime.strptime(dt_string, "%Y.%m.%d %H:%M:%S")

class Generic:
    def __init__(self, match_object):

        self.date = match_object.group(1)
        self.time = match_object.group(2)

        dt_string = f"{self.date} {self.time}"
        self.datetime = datetime.datetime.strptime(dt_string, "%Y.%m.%d %H:%M:%S")