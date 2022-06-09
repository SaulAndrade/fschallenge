import argparse
from pymongo import MongoClient
import pymongo
import datetime

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
    params : Param
        represents the parameters obtained from user input that will influence database operations

    Methods
    -------
    connect():
        Estabilishes a valid connection with MongoDB Atlas and returns a reference to the database
    """

    def __init__(self, usr, pwd, n_drivers, n_buses, n_schedules, s_month):
        self.usr = usr
        self.pwd = pwd
        self.params = Params(n_drivers, n_buses, n_schedules, s_month)

    def __repr__(self):
        return f'Atlas - Parameters: {self.params.n_drivers} drivers, {self.params.n_buses} buses, {self.params.n_schedules} schedules, starting month: {self.params.s_month}'

    def connect(self):
        """brief description"""
        connectStr = f'mongodb+srv://{self.usr}:{self.pwd}@cluster0.yecy6.mongodb.net/?retryWrites=true&w=majority'
        client = MongoClient(connectStr)
        db = client['audela']

        try:
            db['users'].find_one()
            return db
        except:
            raise Exception(f'Auth went wrong for user \'{self.usr}\'. Please try again.')

    def populate(self):
        """Cleans all previously inserted data and populates the database with random records generated based on user input"""

        self.clean()
        pass

    def clean(self):
        """Purge all the database records"""

        pass

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Populates Bus Drivers Schedule Database')
    parser.add_argument('user', help='username for database connection')
    parser.add_argument('password', help='password for database connection')
    parser.add_argument('-c', '--clean', help='Just clean. Don\'t populate', action='store_true', default=False)
    parser.add_argument('-b', help='Number of unique buses. Default=250', type=int, default=250)
    parser.add_argument('-d', help='Number of unique drivers. Default=1.000', type=int, default=1000)
    parser.add_argument('-s', help='Number of schedules. Default=1.000.000', type=int, default=1000000)
    parser.add_argument('-m', help='Schedule starting month', choices=[m for m in range(1,13)], type=int, default=1)
    args = parser.parse_args()
    
    try:
        atlas = Atlas(args.user, args.password, args.d, args.b, args.s, args.m)
        atlas.connect()
        print(f'Successfully estabilished connection to MongoDB\n{atlas}')
        print('If you would like to change the parameters above, please see \'$ python initDb.py -h\' for instructions')
    except Exception as e:
        print(e)

    

