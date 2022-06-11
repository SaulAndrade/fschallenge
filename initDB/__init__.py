import argparse
from random import randint, choice
from pymongo import MongoClient
from dateutil import parser as date_parser
import calendar
from datetime import datetime
from initDB.models.models import Driver, Bus, Schedule

MONTHS_SPAN = 3

class Params:
    """
    Wrapper class for the Atlas parameters read from user input

    ...

     Attributes
    ----------
    n_drivers : int
        number of unique drivers to be inserted into the database
    n_buses : int
        number of unique buses to be inserted into the database
    n_schedules : int
        number of unique schedules to be inserted into the database, spaning through 3 months, starting on the first day of s_month
    s_month : int
        month to start scheduling
    """
    def __init__(self, n_drivers, n_buses, n_schedules, s_month):
        self.n_drivers = n_drivers
        self.n_buses = n_buses
        self.n_schedules = n_schedules
        self.s_month = s_month

    def __repr__(self):
        return f'Parameters:\n*drivers: {self.n_drivers}\n*buses: {self.n_buses}\n*schedules: {self.n_schedules}'

class Atlas:
    """
    A class built to handle database connection and required operations

    ...

    Attributes
    ----------
    usr : str
        database username
    pwd : str
        database password for usr
    db : MongoClient
        connection to MongoDb
    params : Param
        represents the parameters obtained from user input that will influence database operations
    drivers : list
        schedules to be inserted into the database
    buses : list
        schedules to be inserted into the database
    schedules : list
        schedules to be inserted into the database

    Methods
    -------
    connect():
        Estabilishes a valid connection with MongoDB Atlas and returns a reference to the database
    """

    def __init__(self, usr, pwd, n_drivers, n_buses, n_schedules, s_month):
        self.usr = usr
        self.pwd = pwd
        self.db = None
        self.params = Params(n_drivers, n_buses, n_schedules, s_month)
        self.drivers = []
        self.buses = []
        self.schedules = []

    def __repr__(self):
        return f'Atlas - Parameters: {self.params.n_drivers} drivers, {self.params.n_buses} buses, {self.params.n_schedules} schedules, starting month: {self.params.s_month}'

    def connect(self):
        """Estabilishes a valid connection with MongoDB Atlas and returns a reference to the database"""

        connectStr = f'mongodb+srv://{self.usr}:{self.pwd}@cluster0.yecy6.mongodb.net/?retryWrites=true&w=majority'
        client = MongoClient(connectStr)
        db = client['audela']

        try:
            db['users'].find_one()
            self.db = db
        except:
            raise Exception(f'Auth went wrong for user \'{self.usr}\'. Please try again.')

    def populate(self):
        """Cleans all previously inserted data and populates the database with random records generated based on user input"""

        self.clean()

        print('==> Populating Database')

        #populating drivers
        driver_dicts = self.populate_drivers()
        try:
            result = self.db['drivers'].insert_many(driver_dicts)
            driver_ids = result.inserted_ids
        except Exception as e:
            raise Exception(f'Failed to insert drivers into the database: {e}')

        #populating buses
        bus_dicts = self.populate_buses(driver_ids)
        try:
            result = self.db['buses'].insert_many(bus_dicts)
            bus_ids = result.inserted_ids
        except Exception as e:
            raise Exception(f'Failed to insert buses into the database: {e}')

        #populating schedules    
        sch_dicts = self.populate_shcedules(bus_ids)
        try:
            result = self.db['schedules'].insert_many(sch_dicts)
        except Exception as e:
            raise Exception(f'Failed to insert schedules into the database: {e}')

    def clean(self):
        """Purge all the database records"""

        print('==> Purging Database')
        try:
            for collection in self.db.list_collection_names():
                self.db[collection].delete_many({})
        except Exception as e:
            raise Exception(f'Cleaning went wrong. Failed to clean {collection} data: {e}')

    def populate_drivers(self):
        """
        Generates driver dictionaries to be inserted into the database
        
        Returns
        -------
        driver_dicts : list
            list of driver dictionaries to be inserted in the database
        """

        print('==== Populating drivers')
        surnames = ['Smith', 'Brown', 'Tremblay', 'Martin', 'Roy', 'Gagnon', 'Lee', 'Wilson', 'Johnson', 'MacDonald']
        driver_dicts = []
        for n in range(self.params.n_drivers):
            driver = Driver(f'Driver_{n}', choice(surnames), str(randint(1, 99999999)).zfill(8), f'Driver_{n}@drivers.audela.ca')
            self.drivers.append(driver)
            driver_dicts.append(driver.__dict__)

        return driver_dicts

    def populate_buses(self, driver_ids):
        """
        Generates bus dictionaries to be inserted into the database
        
        Parameters
        ----------
        driver_ids : list
            list of driver ids present in the database

        Returns
        -------
        bus_dicts : list
            list of bus dictionaries to be inserted in the database
        """

        print('==== Populating buses')
        makes = ['Honda', 'Mazda', 'Chevrolet', 'Volvo', 'Tesla', 'BMW', 'Mercedez', 'Fiat']
        bus_dicts = []
        for n in range(self.params.n_buses):
            bus = Bus(randint(10, 50), f'Model {randint(1,6)}', choice(makes), choice(driver_ids))
            self.buses.append(bus)
            bus_dicts.append(bus.__dict__)

        return bus_dicts

    def populate_shcedules(self, bus_ids):
        """
        Generates schedule dictionaries to be inserted into the database
        
        Parameters
        ----------
        bus_ids : list
            list of bus ids present in the databse

        Returns
        -------
        sch_dicts : list
            list of schedule dictionaries to be inserted in the database
        """

        print('==== Populating Schedules')
        #break down number number of schedules equally throughot MONTHS_SPAN {3} months
        n_schedules_per_month = int(self.params.n_schedules / MONTHS_SPAN)
        schedules_per_month_list = [ n_schedules_per_month for n in range(MONTHS_SPAN) ]
        schedules_per_month_list[-1] += self.params.n_schedules % MONTHS_SPAN

        current_month = self.params.s_month
        current_year = datetime.now().year

        schedules=[]
        for n_schedule in schedules_per_month_list:
            days_in_month = calendar.monthrange(current_year, current_month)[1]

            #pick a random day for each schedule in the current month generate the schedule object
            for i in range(n_schedule):
                random_day = randint(1, days_in_month)
                schedule = Schedule(choice(bus_ids), random_day, current_month, current_year)
                schedules.append(schedule)
            current_month+=1
            
        self.schedules = [sch for sch in schedules]
        sch_dicts = [sch.__dict__ for sch in schedules]
        return sch_dicts

class ScheduleValidator(argparse.Action):
    """Implementation of the argparse.Action class to validate minimum number of schedules to be generated"""

    def __init__(
        self,
        option_strings, 
        dest=None, 
        nargs=1, 
        default=None, 
        required=False, 
        metavar=None,
        type = None,
        help = None):
        
        super().__init__(
            option_strings,
            dest=dest, 
            nargs=nargs, 
            default=default, 
            required=required, 
            metavar=metavar,
            type = type,
            help = help
        )

    def __call__(self, parser, namespace, values, option_string):
        n_sch = values[0]
        try:
            setattr(namespace, self.dest, n_sch)
            assert(n_sch>=MONTHS_SPAN)
        except:
            raise argparse.ArgumentError(self, f'Number of schedules should be at least equal to {MONTHS_SPAN}')