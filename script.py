from initDB import *
import argparse
from random import randint, choice

if __name__ == "__main__":

    #parse user input
    parser = argparse.ArgumentParser(description='Populates Bus Drivers Schedule Database')
    parser.add_argument('user', help='username for database connection')
    parser.add_argument('password', help='password for database connection')
    parser.add_argument('-c', '--clean', help='Just clean. Don\'t populate', action='store_true', default=False)
    parser.add_argument('-b', help='Number of unique buses. Default=250', type=int, default=250)
    parser.add_argument('-d', help='Number of unique drivers. Default=1.000', type=int, default=1000)
    parser.add_argument('-s', help='Number of schedules. Default=1.000.000', action=ScheduleValidator, type=int, default=1000000)
    parser.add_argument('-m', help='Schedule starting month', choices=[m for m in range(1,13)], type=int, default=1)
    args = parser.parse_args()

    try:
        #connect to MongoDB
        atlas = Atlas(args.user, args.password, args.d, args.b, args.s, args.m)
        atlas.connect()
        print(f'==> Successfully estabilished connection to MongoDB Atlas\n')
        print(atlas.params)
        print('\n==== If you would like to change the data generation, please see \'$ python initDb.py -h\' for instructions\n')
    except Exception as e:
        print(e)
        exit(0)
   
    try:
        #populate with random data based on user input
        if(args.clean):
            atlas.clean()
        else:
            atlas.populate()
    except Exception as e:
        print(e)