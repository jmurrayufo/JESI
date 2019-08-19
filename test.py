#!/usr/bin/env python 

import logging
import re
import argparse
import datetime
from pathlib import Path

from LogParser import Row, Parser


logs_location = Path("/media/sf_C_DRIVE/Users/John/Documents/EVE/logs/GameLogs/20190818_212723.txt")

# latest_log = sorted(logs_location.glob("*.txt"), key=lambda x: x.stat().st_mtime, reverse=True)[0]


with open(logs_location, 'r') as fp:
    for line in fp:
        # print(line,end='')
        r = Row.Row(line)
        if type(r) == Row.Unknown:
            print(line)


