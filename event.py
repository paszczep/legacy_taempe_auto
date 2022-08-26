import os
from datetime import datetime
from csv import DictReader
import time

DATETIME_FORMAT = "%d/%m/%Y %H:%M"


class Event:
    def __init__(self, plan_row: dict):
        self.container = plan_row['container']
        self.time = time.mktime(datetime.strptime(plan_row['datetime'], DATETIME_FORMAT).timetuple())
        self.temperature = plan_row['temperature']


def get_events_list() -> list:
    base_dir = os.path.dirname(__file__)
    file_dir = os.path.join(base_dir, 'schedule.csv')
    open_file = open(file_dir, 'r')
    reader = DictReader(open_file)
    schedule = [Event(row) for row in reader if row['temperature'] != '']
    for event in schedule:
        print(
            datetime.fromtimestamp(event.time).strftime(DATETIME_FORMAT),
            event.container,
            f'{event.temperature}°C',
            sep='\t')
    return schedule
