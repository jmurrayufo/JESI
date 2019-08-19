
from datetime import timedelta
from pathlib import Path
import argparse
import datetime
import logging
import pprint
import re
import time

from . import Row, Parser, Display

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-n', dest='refresh', default=5, type=float,
    help='Seconds between refreshes')
parser.add_argument('--logpath', 
    default='/media/sf_C_DRIVE/Users/John/Documents/EVE/logs/GameLogs/',
    help='Location to look for logs in')
parser.add_argument('-v', '--verbose', action='count', default=0,
    help='More verbose stats')
parser.add_argument('-b', '--box_totals', type=int, default=0,
    help='Number of slots for grouped stats (eg: show top 10 Damage done to targets)')
parser.add_argument('-s', '--summary', action='store_true', default=False,
    help='Just display a summery and exit')

args = parser.parse_args()
args.time_boxes = [
    # timedelta(seconds=10),
    timedelta(minutes=1),
    timedelta(minutes=5),
    # timedelta(minutes=30),
    timedelta(minutes=60),
    timedelta.max,
]

if args.summary:
    args.box_totals = 9999

if args.verbose > 0:
    print(args)
    print("Sleeping for 5 before screens clear...")
    time.sleep(5)

assert args.refresh >= 1, "Refresh rate too high, please pick a more sane value!"

def main_loop(args):
    

    while 1:
        logs_location = Path(args.logpath)
        latest_log = sorted(logs_location.glob("*.txt"), key=lambda x: x.stat().st_mtime, reverse=True)[0]

        parser = Parser.Parser(latest_log)
        parser.parse(args.time_boxes)
        display = Display.Display(args, parser)
        display.display()

        if args.summary:
            break
        time.sleep(args.refresh)

main_loop(args)



