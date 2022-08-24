import os
from datetime import datetime
from csv import DictReader
import time


class Event:
    def __init__(self, plan_row: dict):
        self.container = plan_row['container']
        self.time = time.mktime(datetime.strptime(plan_row['datetime'], "%d/%m/%Y %H:%M").timetuple())
        self.temperature = plan_row['temperature']


def get_events_list() -> list:
    file = [el for el in os.listdir() if '.csv' in el].pop()
    open_file = open(file, 'r')
    reader = DictReader(open_file)
    schedule = [Event(row) for row in reader]
    for event in schedule:
        print(event.time, event.container, f'{event.temperature} °C', sep='\t')
    return schedule


