import argparse
from eventsDatabase import filterDatabase, monthDays, performQuery
from datetime import date, datetime
import os 


def filterEvents(filterRange) -> None:
    acceptedArguments = {"today", "weekly", "month", "year"}
    if  filterRange.strip() in acceptedArguments:
        todaysDate = datetime.now()
        if filterRange == "today":
            filterDatabase(begin_date=f"{todaysDate.month}/{todaysDate.day}/{todaysDate.year}")

        elif filterRange == "weekly":
            currentDay = date.today().isoweekday()
            firstDay  = todaysDate.day - currentDay
            firstMonth = todaysDate.month 
            firstYear = todaysDate.year 
            if firstDay < 0:
                daysInPreviousMonth = None 
                if firstMonth == 1:
                    firstMonth = 12
                    daysInPreviousMonth = monthDays[12]
                    firstYear -= 1 
                else:
                    firstMonth -= 1
                    daysInPreviousMonth = monthDays[firstMonth]

                firstDay = daysInPreviousMonth + firstDay 
                

            lastDay = (7-currentDay) + todaysDate.day 
            lastMonth = todaysDate.month 
            lastYear =todaysDate.year

            if lastDay > monthDays[lastMonth]:
                lastDay = lastDay%monthDays[lastMonth] 
                lastMonth += 1
                if lastMonth == 13:
                    lastYear += 1
                    
            filterDatabase(begin_date=f"{firstMonth}/{firstDay}/{firstYear}", end_date_filter=f"{lastMonth}/{lastDay}/{lastMonth}" )

        elif filterRange == "month":
            filterDatabase(begin_date=f"{todaysDate.month}/{1}/{todaysDate.year}", end_date_filter=f"{todaysDate.month}/{monthDays[todaysDate.month]}/{todaysDate.year}" )

        elif filterRange == "year":
            filterDatabase(begin_date=f"{1}/{1}/{todaysDate.year}", end_date_filter=f"{1}/{1}/{todaysDate.year + 1}" )

parser = argparse.ArgumentParser()

parser.add_argument("-f","--filter", help="Type of filter: today, weekly, month or year", type=str)
parser.add_argument("-q","--query", help="Write a sql query", nargs='+')
parser.add_argument("--gui", help="run gui", action="store_true")

args = parser.parse_args()

if args.filter:
    filterEvents(args.filter)

if args.query:
    query = ""
    for word in args.query:
        if word == "all":
            word = "*"
        query += word + " "

    performQuery(query)

if args.gui:
    os.system('python3 /Users/ghazshahbaz/documents/eventsdatabase/events_gui.py')


