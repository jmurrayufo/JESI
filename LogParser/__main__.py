
import logging
import re
import argparse
import datetime
from datetime import timedelta
from pathlib import Path
import pprint

from . import Row, Parser


logs_location = Path("/media/sf_C_DRIVE/Users/John/Documents/EVE/logs/GameLogs/")

latest_log = sorted(logs_location.glob("*.txt"), key=lambda x: x.stat().st_mtime, reverse=True)[0]

parser = Parser.Parser(latest_log)

start = datetime.datetime.now()

end = datetime.datetime.now()

time_boxes = [
    # timedelta(seconds=10),
    timedelta(minutes=1),
    timedelta(minutes=5),
    # timedelta(minutes=30),
    timedelta(minutes=60),
    timedelta.max,
    ]

parser.parse(time_boxes)

# print(parser.data)


for time_box in time_boxes[:-1]:
    print(f"Time Delta: {time_box}")
    # Handy data shortcuts
    data = parser.data[time_box] 
    box_seconds = time_box.total_seconds()
    # TODO: Handle final timebox with some sanity
    print(f"  Total Damage Sent: {data['damage_to']:,.0f} ({data['damage_to']/box_seconds:,.1f} dps)")
    print(f"  Total Damage Tanked: {data['damage_from']:,.0f} ({data['damage_from']/box_seconds:,.1f} dps)")
    
    if len(list(data['damage_ship_to'].keys())):
        print(f"  Top Damage Done Target:", end="")
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

session_seconds =  (parser._last_dt - parser._first_dt ).total_seconds()

for time_box in time_boxes[-1:]:
    print(f"Time Delta: {timedelta(seconds=session_seconds)} (Current Session)")
    # Handy data shortcuts
    data = parser.data[time_box] 
    box_seconds = time_box.total_seconds()
    # TODO: Handle final timebox with some sanity
    print(f"  Total Damage Sent: {data['damage_to']:,.0f} ({data['damage_to']/box_seconds:,.1f} dps)")
    print(f"  Total Damage Tanked: {data['damage_from']:,.0f} ({data['damage_from']/box_seconds:,.1f} dps)")
    
    if len(list(data['damage_ship_to'].keys())):
        print(f"  Top Damage Done Target:")
        for ship in list(data['damage_ship_to'].keys())[:]:
            print(f"    {ship} ({data['damage_ship_to'][ship]:,.0f})")
    if len(list(data['damage_ship_from'].keys())):
        print(f"  Top Damage Recieved Source:")
        for ship in list(data['damage_ship_from'].keys())[:]:
            print(f"    {ship} ({data['damage_ship_from'][ship]:,.0f})")

    if len(list(data['damage_type_to'].keys())):
        print(f"  Top Damage Type Dealt:")
        for _type in list(data['damage_type_to'].keys())[:]:
            print(f"    {_type} ({data['damage_type_to'][_type]:,.0f})")
    if len(list(data['damage_type_from'].keys())):
        print(f"  Top Damage Type Recieved:")
        for _type in list(data['damage_type_from'].keys())[:]:
            print(f"    {_type} ({data['damage_type_from'][_type]:,.0f})")

    if len(list(data['damage_system_to'].keys())):
        print(f"  Top Damage System Dealt:")
        for _system in list(data['damage_system_to'].keys())[:]:
            print(f"    {_system} ({data['damage_system_to'][_system]:,.0f})")
    if len(list(data['damage_system_from'].keys())):
        print(f"  Top Damage System Recieved:")
        for _system in list(data['damage_system_from'].keys())[:]:
            print(f"    {_system} ({data['damage_system_from'][_system]:,.0f})")
    print()