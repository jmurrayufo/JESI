
import logging
import re
import argparse
import datetime
from pathlib import Path

from . import Row, Parser


logs_location = Path("/media/sf_C_DRIVE/Users/John/Documents/EVE/logs/GameLogs/")

latest_log = sorted(logs_location.glob("*.txt"), key=lambda x: x.stat().st_mtime, reverse=True)[0]

parser = Parser.Parser(latest_log)
parser.parse()

start = datetime.datetime.now()

end = datetime.datetime.now()

session_seconds =  (parser._last_dt - parser._first_dt ).total_seconds()


print(f"Session Seconds: {session_seconds:,.0f}")
print(f"     Damge Sent: {parser._to:,} ({parser._to/session_seconds:.1f} dps)")
print(f"   Damge Tanked: {parser._from:,} ({parser._from/session_seconds:.1f} dps)")


print( "\n\n Last 60 Seconds:")
print(f"     Damge Sent: {parser._to_1min:,} ({parser._to_1min/(1*60):.1f} dps)")
print(f"   Damge Tanked: {parser._from_1min:,} ({parser._from_1min/(1*60):.1f} dps)")


print( "\n\n Last 5 Minutes:")
print(f"     Damge Sent: {parser._to_5min:,} ({parser._to_5min/(5*60):.1f} dps)")
print(f"   Damge Tanked: {parser._from_5min:,} ({parser._from_5min/(5*60):.1f} dps)")


print( "\n\n Last 30 Minutes:")
print(f"     Damge Sent: {parser._to_30min:,} ({parser._to_30min/(30*60):.1f} dps)")
print(f"   Damge Tanked: {parser._from_30min:,} ({parser._from_30min/(30*60):.1f} dps)")


print( "\n\n Last 60 Minutes:")
print(f"     Damge Sent: {parser._to_60min:,} ({parser._to_60min/(60*60):.1f} dps)")
print(f"   Damge Tanked: {parser._from_60min:,} ({parser._from_60min/(60*60):.1f} dps)")


print( "\n\n Damage by source/sarget in last 60 minutes:")
print("                Targets:")
# for target in parser._targets_60min:
for target in list(parser._targets_60min.keys())[:10]:
    print(f"   {target:>35}: {parser._targets_60min[target]:7,.0f}")
print("                Sources:")
for source in list(parser._sources_60min.keys())[:10]:
    print(f"   {source:>35}: {parser._sources_60min[source]:7,.0f}")


print( "\n\n Damage by type in last 60 minutes:")
print("                Type Dealt:")
for type_to in list(parser._type_to_60min.keys())[:10]:
    print(f"   {type_to:>35}: {parser._type_to_60min[type_to]:7,.0f}")
print("                Type Recieved:")
for type_from in list(parser._type_from_60min.keys())[:10]:
    print(f"   {type_from:>35}: {parser._type_from_60min[type_from]:7,.0f}")


print( "\n\n Damage by system in last 60 minutes:")
print("                Sources:")
for system_to in list(parser._system_to_60min.keys())[:10]:
    print(f"   {system_to:>35}: {parser._system_to_60min[system_to]:7,.0f}")
print("                Targets:")
for system_from in list(parser._system_from_60min.keys())[:10]:
    print(f"   {system_from:>35}: {parser._system_from_60min[system_from]:7,.0f}")