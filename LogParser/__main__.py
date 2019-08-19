
from datetime import timedelta
from os import system, name 
from pathlib import Path
import argparse
import datetime
import logging
import pprint
import re
import time

from . import Row, Parser

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

if args.verbose > 0:
    print(args)
    print("Sleeping for 5 before screens clear...")
    time.sleep(5)

assert args.refresh >= 1, "Refresh rate too high, please pick a more sane value!"

def main_loop(args):
    
    box_totals = args.box_totals if args.summary == False else 9999

    while 1:
        logs_location = Path(args.logpath)
        latest_log = sorted(logs_location.glob("*.txt"), key=lambda x: x.stat().st_mtime, reverse=True)[0]

        parser = Parser.Parser(latest_log)

        time_boxes = [
            # timedelta(seconds=10),
            timedelta(minutes=1),
            timedelta(minutes=5),
            # timedelta(minutes=30),
            timedelta(minutes=60),
            timedelta.max,
            ]

        parser.parse(time_boxes)

        # Clear screen for display
        if name == 'nt': 
            system('cls') 
        else: 
            system('clear') 

        # Loop through all but the last (special) timebox
        for time_box in time_boxes[:-1]:
            print(f"Time Delta: {time_box}")
            # Handy data shortcuts
            data = parser.data[time_box] 
            box_seconds = max(1,time_box.total_seconds())
            # TODO: Handle final timebox with some sanity
            print(f"  Total Damage Sent: {data['damage_to']:,.0f} ({data['damage_to']/box_seconds:,.1f} dps)")
            print(f"  Total Damage Tanked: {data['damage_from']:,.0f} ({data['damage_from']/box_seconds:,.1f} dps)")
            #print(f"  Bounties Collected: {data['isk']} ISK")
            print(f"  Bounties Collected: {data['isk']:,.2f} ISK ({data['isk']/box_seconds*60*60/1e6:,.2f} Misk/hr)")
            
            if args.box_totals > 0:
                new_lines = "" if args.box_totals > 1 else "\n"
                if len(list(data['damage_ship_to'].keys())):
                    print(f"  Top Damage Done Target:", end=new_lines)
                    for ship in list(data['damage_ship_to'].keys())[:1]:
                        print(f" {ship} ({data['damage_ship_to'][ship]:,.0f})")
                if len(list(data['damage_ship_from'].keys())):
                    print(f"  Top Damage Recieved Source:", end="")
                    for ship in list(data['damage_ship_from'].keys())[:1]:
                        print(f" {ship} ({data['damage_ship_from'][ship]:,.0f})")

                if len(list(data['damage_type_to'].keys())):
                    print(f"  Top Damage Type Dealt:", end="")
                    for _type in list(data['damage_type_to'].keys())[:1]:
                        print(f" {_type} ({data['damage_type_to'][_type]:,.0f})")
                if len(list(data['damage_type_from'].keys())):
                    print(f"  Top Damage Type Recieved:", end="")
                    for _type in list(data['damage_type_from'].keys())[:1]:
                        print(f" {_type} ({data['damage_type_from'][_type]:,.0f})")

                if len(list(data['damage_system_to'].keys())):
                    print(f"  Top Damage System Dealt:", end="")
                    for _system in list(data['damage_system_to'].keys())[:1]:
                        print(f" {_system} ({data['damage_system_to'][_system]:,.0f})")
                if len(list(data['damage_system_from'].keys())):
                    print(f"  Top Damage System Recieved:", end="")
                    for _system in list(data['damage_system_from'].keys())[:1]:
                        print(f" {_system} ({data['damage_system_from'][_system]:,.0f})")
            print()

        session_seconds =  max(1, (parser._last_dt - parser._first_dt ).total_seconds())

        for time_box in time_boxes[-1:]:
            print(f"Time Delta: {timedelta(seconds=session_seconds)} (Current Session)")
            # Handy data shortcuts
            data = parser.data[time_box] 
            box_seconds = session_seconds
            # TODO: Handle final timebox with some sanity
            print(f"  Total Damage Sent: {data['damage_to']:,.0f} ({data['damage_to']/box_seconds:,.1f} dps)")
            print(f"  Total Damage Tanked: {data['damage_from']:,.0f} ({data['damage_from']/box_seconds:,.1f} dps)")
            print(f"  Bounties Collected: {data['isk']:,.2f} ISK ({data['isk']/box_seconds*60*60/1e6:,.2f} Misk/hr)")
            
            if args.box_totals > 0:
                new_lines = "" if args.box_totals > 1 else "\n"

                sub_data = data['damage_ship_to']
                if len(list(sub_data.keys())):
                    print(f"  Top Damage Done Target:")
                    total = sum(sub_data.values())
                    for ship in list(sub_data.keys())[:box_totals]:
                        print(f"    {sub_data[ship]:12,.0f} {ship} ({sub_data[ship]/total:.1%})")

                if len(list(data['damage_ship_from'].keys())):
                    print(f"  Top Damage Recieved Source:")
                    for ship in list(data['damage_ship_from'].keys())[:box_totals]:
                        print(f"    {ship} ({data['damage_ship_from'][ship]:,.0f})")

                if len(list(data['damage_type_to'].keys())):
                    print(f"  Top Damage Type Dealt:")
                    for _type in list(data['damage_type_to'].keys())[:box_totals]:
                        print(f"    {_type} ({data['damage_type_to'][_type]:,.0f})")

                if len(list(data['damage_type_from'].keys())):
                    print(f"  Top Damage Type Recieved:")
                    for _type in list(data['damage_type_from'].keys())[:box_totals]:
                        print(f"    {_type} ({data['damage_type_from'][_type]:,.0f})")

                if len(list(data['damage_system_to'].keys())):
                    print(f"  Top Damage System Dealt:")
                    for _system in list(data['damage_system_to'].keys())[:box_totals]:
                        print(f"    {_system} ({data['damage_system_to'][_system]:,.0f})")

                if len(list(data['damage_system_from'].keys())):
                    print(f"  Top Damage System Recieved:")
                    for _system in list(data['damage_system_from'].keys())[:box_totals]:
                        print(f"    {_system} ({data['damage_system_from'][_system]:,.0f})")

        if args.summary:
            break
        time.sleep(args.refresh)

main_loop(args)
