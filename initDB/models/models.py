import datetime
from random import randint, choice
from dateutil.relativedelta import *
from dateutil import parser as date_parser

class Driver:
    """Class representing a driver"""

    def __init__(self, fname, lname, sin, email):
        self.first_name = fname
        self.last_name = lname
        self.sin = sin
        self.email = email

class Bus:
    """Class representing a bus"""

    def __init__(self, cap, model, make, driver_id):
        self.capacity = cap
        self.model = model
        self.make = make
        self.driver_id = driver_id

class Schedule:
    """Class representing a schedule"""

    def __init__(self, bus_id, day, month, year):
        start_datetime = self.insert_random_time(day, month, year)
        
        self.bus_id = bus_id
        self.start = start_datetime
        self.end = self.add_random_time_span(start_datetime)

    def __repr__(self):
        start = date_parser.parse(self.start)
        end = date_parser.parse(self.end)
        return f'Bus no:{self.bus_id} - {str(start)} - {str(end)}'
    
    @staticmethod
    def insert_random_time(day, month, year):
        """Returns a datetime with random time for a given date"""

        hour = randint(0, 23)
        minute = choice([0, 15, 30 , 45])
        second =  choice([0, 15, 30 , 45])
        return datetime.datetime(year, month, day, hour, minute, second)

    @staticmethod
    def add_random_time_span(start):
        """Adds a random time span to a given datetime"""
        dh = randint(0,6)
        dm = randint(0,3)
        return start + relativedelta(hours=+dh, minutes=+dm*15)
