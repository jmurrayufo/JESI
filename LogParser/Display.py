from os import system, name 
from datetime import timedelta


class Display:


    def __init__(self, args, parser):
        self.args = args
        self.parser = parser


    def display(self):
        # Clear screen for display
        if name == 'nt': 
            system('cls') 
        else: 
            system('clear') 

        # Loop through all but the last (special) timebox
        for time_box in self.args.time_boxes[:-1]:
            print(f"Time Delta: {time_box}")

            # Handy data shortcuts
            data = self.parser.data[time_box] 
            box_seconds = max(1,time_box.total_seconds())

            print(f"  Total Damage Sent: {data['damage_to']:,.0f} ({data['damage_to']/box_seconds:,.1f} dps)")
            print(f"  Total Damage Tanked: {data['damage_from']:,.0f} ({data['damage_from']/box_seconds:,.1f} dps)")
            print(f"  Bounties Collected: {data['isk']:,.2f} ISK ({data['isk']/box_seconds*60*60/1e6:,.2f} Misk/hr)")
            
            if self.args.box_totals > 0:
                new_lines = "" if self.args.box_totals > 1 else "\n"
                self._sub_display(data['damage_ship_to'], "  Top Damage Done Target:", 1, new_lines)
                self._sub_display(data['damage_ship_from'], "  Top Damage Recieved Source:", 1, new_lines)
                self._sub_display(data['damage_type_to'], "  Top Damage Type Dealt:", 1, new_lines)
                self._sub_display(data['damage_type_from'], "  Top Damage Type Recieved:", 1, new_lines)
                self._sub_display(data['damage_system_to'], "  Top Damage System Dealt:", 1, new_lines)
                self._sub_display(data['damage_system_from'], "  Top Damage System Recieved:", 1, new_lines)

                if len(list(data['damage_system_from'].keys())):
                    print(f"  Top Damage System Recieved:", end="")
                    for _system in list(data['damage_system_from'].keys())[:1]:
                        print(f" {_system} ({data['damage_system_from'][_system]:,.0f})")
            print()

        session_seconds =  max(1, (self.parser._last_dt - self.parser._first_dt ).total_seconds())

        # Special loop for last timebox. Keeping this in a forloop allows for handle break statements
        for time_box in self.args.time_boxes[-1:]:
            print(f"Time Delta: {timedelta(seconds=session_seconds)} (Current Session)")

            # Handy data shortcuts
            data = self.parser.data[time_box] 
            box_seconds = session_seconds

            print(f"  Total Damage Sent: {data['damage_to']:,.0f} ({data['damage_to']/box_seconds:,.1f} dps)")
            print(f"  Total Damage Tanked: {data['damage_from']:,.0f} ({data['damage_from']/box_seconds:,.1f} dps)")
            print(f"  Bounties Collected: {data['isk']:,.2f} ISK ({data['isk']/box_seconds*60*60/1e6:,.2f} Misk/hr)")
            
            if self.args.box_totals > 0:
                new_lines = "" if self.args.box_totals > 1 else "\n"
                new_lines = "\n"
                self._sub_display(data['damage_ship_to'], "  Top Damage Done Target:", self.args.box_totals, new_lines)
                self._sub_display(data['damage_ship_from'], "  Top Damage Recieved Source:", self.args.box_totals, new_lines)
                self._sub_display(data['damage_type_to'], "  Top Damage Type Dealt:", self.args.box_totals, new_lines)
                self._sub_display(data['damage_type_from'], "  Top Damage Type Recieved:", self.args.box_totals, new_lines)
                self._sub_display(data['damage_system_to'], "  Top Damage System Dealt:", self.args.box_totals, new_lines)
                self._sub_display(data['damage_system_from'], "  Top Damage System Recieved:", self.args.box_totals, new_lines)


    def _sub_display(self, sub_data, caption, box_totals, endl):
        if len(list(sub_data.keys())):
            print(caption, end=endl)
            total = sum(sub_data.values())
            for ship in list(sub_data.keys())[:box_totals]:
                print(f"    {sub_data[ship]:12,.0f} {ship} ({sub_data[ship]/total:.1%})")
