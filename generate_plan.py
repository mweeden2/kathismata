# Created by MW on 8/15/19
# Modified 11/13/19

# This script generates a daily Psalm reading plan
#   for reading one Psalm from the appropriate
#   kathismata for the day and rotating to the next
#   each week.


import argparse
import json
import functools
import operator
from datetime import datetime, timedelta
import sys

starting_psalm_date = (datetime.strptime("11-01-2019", "%m-%d-%Y"), 147)

weekday_mapping = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednessday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
}


def main():

    parser = argparse.ArgumentParser(description="[app description]")
    parser.add_argument("-v", "--verbose",
                        help="be verbose about it", action="store_true")
    parser.add_argument("start_date", help="the starting date of the schedule")
    parser.add_argument("end_date", help="the ending date of the schedule")
    args = parser.parse_args()

    # ===========================================================
    #  parse date args
    # ===========================================================
    start_date = datetime.today()
    end_date = datetime.today()
    try:
        start_date = datetime.strptime(args.start_date, "%Y%m%d")
    except:
        print("Please provide a valid start date of the form YYYYMMDD (i.e. 20290101).")
        return
    try:
        end_date = datetime.strptime(args.end_date, "%Y%m%d")
    except:
        print("Please provide a valid end date of the form YYYYMMDD (i.e. 20290101).")
        return

    # ===========================================================
    #  Generate the plan
    # ===========================================================
    with open("./kathismata.json", "r") as kf:
        with open("./schedule.json", "r") as sf:

            kathismata = json.load(kf)["kathismata"]
            schedule = json.load(sf)["schedule"]

            # Set up counter to keep track of what the current Psalm per weekday
            psalm_counter = {k: 0 for k in weekday_mapping.keys()}

        for i in range((end_date - start_date).days + 1):

            day = start_date+timedelta(days=i)

            c = psalm_counter[day.weekday()]
            s = schedule[weekday_mapping[day.weekday()]]

            # gather lists of this day's psalms
            mk = s['morning']['kathismata']
            ek = s['evening']['kathismata']

            if len(mk) == 0:
                print('none')

            else:
                print(find_psalm(mk, kathismata, c))

            if len(ek) == 0:
                print('none')
            else:
                print(find_psalm(ek, kathismata, c))
                ec = c  # % (ek[-1] - ek[0])

            print(str(i) + '\t' + str(day) + '\t' +
                  str(weekday_mapping[day.weekday()]) + '\t' +
                  str(s) + ' ' +
                  str(c) + ' ' +
                  str(range(mk[0], mk[-1])))  # + ' ' +
            # str(range(ek[0]))) # + ' ' +

            psalm_counter[day.weekday()] += 1

        print(psalm_counter)


def find_psalm(sch, kmata, c):
    ml = functools.reduce(list.__add__, [list(
        range(kmata[i-1]['start'], kmata[i-1]['end']+1)) for i in sch])
    mc = operator.mod(c, ml[-1] - ml[0])
    return ml[mc]


if __name__ == "__main__":
    main()
