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
        re_matchers['combat_miss'] = r"""
            {}
            (.*)\smisses\syou\scompletely
        """.format(re_matchers['base'])
        re_matchers['combat_miss_2'] = r"""
            {}
            Your\s
            (.*)
            \smisses\s
            (.*)
            \scompletely\s-\s
            (.*)
        """.format(re_matchers['base'])
        re_matchers['generic'] = r"""
            {}
            (.*)
        """.format(re_matchers['base'])
        re_matchers['bounty'] = r"""
            {}
            <font\ssize=\d+><b><color=0x\w+>
            (.*)
            \sISK
        """.format(re_matchers['base'])
        base_match = re.match(re_matchers['base'], line, re.X)

        if not base_match:
            return None
        if base_match.group(3) == 'combat':
            match_object = re.search(re_matchers['combat_hit'], line, re.X)
            if match_object:
                # print(line)
                return Combat(match_object)
            #print(f"Match line \n{line}\n with \n{re_matchers['combat_miss']}")
            match_object = re.match(re_matchers['combat_miss'], line, re.X)
            if match_object:
                return CombatMiss(match_object)
            match_object = re.match(re_matchers['combat_miss_2'], line, re.X)
            if match_object:
                return CombatMiss(match_object)
        if base_match.group(3) == 'bounty':
            match_object = re.match(re_matchers['bounty'], line, re.X)
            if match_object:
                return Bounty(match_object)
        match_object = re.search(re_matchers['generic'], line, re.X)
        if match_object and match_object.group(3) in ['notify', 'question', 'None', 'warning', 'hint', 'info']:
            return Generic(match_object)
        # print(re_matchers['combat_hit'])
        return Unknown(match_object)


class RowBase:
    def __init__(self, match_object):
        self.date = match_object.group(1)
        self.time = match_object.group(2)

        dt_string = f"{self.date} {self.time}"
        self.datetime = datetime.datetime.strptime(dt_string, "%Y.%m.%d %H:%M:%S")


class Bounty(RowBase):
    def __init__(self, match_object):
        """ TODO: Parse this out
        """
        super().__init__(match_object)
        self.isk = float(match_object.group(4).replace(',','_'))
        pass


class CombatMiss(RowBase):
    def __init__(self, match_object):
        """ TODO: Parse this out
        """
        super().__init__(match_object)
        pass


class CombatMiss(RowBase):
    def __init__(self, match_object):
        """ TODO: Parse this out
        """
        super().__init__(match_object)
        pass


class Combat(RowBase):
    pass
    def __init__(self, match_object):
        super().__init__(match_object)

        self.amount = int(match_object.group(4))
        self.to = match_object.group(5) == 'to'
        self.source_target = match_object.group(6)
        self.system = match_object.group(7) if match_object.group(7) is not None else "Unknown"
        # TODO: Parse this into meantingful data!
        self.damage_type = 'Unknown'

    def __str__(self):
        return f"{self.datetime} {self.amount} {'to' if self.to else 'from'} @ {self.source_target} "


class Unknown(RowBase):
    def __init__(self, match_object):
        super().__init__(match_object)


class Generic(RowBase):
    def __init__(self, match_object):
        super().__init__(match_object)
        self.message = match_object.group(4)

