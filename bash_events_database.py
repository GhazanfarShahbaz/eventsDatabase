import argparse
from eventsDatabase import filterDatabase, monthDays, performQuery
from datetime import date, datetime
import os 


def filterEvents(filterRange, calculate) -> None:
    """
    filter events function takes an option today, week, month or year and prints out events that match the query 
    """
    acceptedArguments = {"today", "week", "month", "year"}
    if  filterRange.strip() in acceptedArguments:
        todaysDate = datetime.now()
        if filterRange == "today":
            filterDatabase(begin_date=f"{todaysDate.month}/{todaysDate.day}/{todaysDate.year}",calculateFreeTime=calculate)

        elif filterRange == "week":
            #need to account for leap year
            currentDay = date.today().isoweekday()
            firstDay  = todaysDate.day - currentDay
            firstMonth = todaysDate.month 
            firstYear = todaysDate.year 
            # if the first day is less than 0 then we have to roll over to the previous month
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

            # if the last day is greter than the total days in the month then we have to move the date up and recalculate the date
            if lastDay > monthDays[lastMonth]:
                lastDay = lastDay%monthDays[lastMonth] 
                lastMonth += 1
                if lastMonth == 13:
                    lastYear += 1
                    
            filterDatabase(begin_date=f"{firstMonth}/{firstDay}/{firstYear}", end_date_filter=f"{lastMonth}/{lastDay}/{lastYear}",calculateFreeTime=calculate)

        elif filterRange == "month":

            filterDatabase(begin_date=f"{todaysDate.month}/{1}/{todaysDate.year}", end_date_filter=f"{todaysDate.month}/{monthDays[todaysDate.month]}/{todaysDate.year}",calculateFreeTime=calculate)

        elif filterRange == "year":
            filterDatabase(begin_date=f"{1}/{1}/{todaysDate.year}", end_date_filter=f"{1}/{1}/{todaysDate.year + 1}",calculateFreeTime=calculate)

parser = argparse.ArgumentParser()

#filter takes in a string
parser.add_argument("-f","--filter", help="Type of filter: today, weekly, month or year", type=str)
#query stores true or false
parser.add_argument("-q","--query", help="Write a sql query", action="store_true")
#gui stores true or false
parser.add_argument("--gui", help="run gui", action="store_true")

parser.add_argument("--calculateFreeTime", "-cft", action="store_true")

args = parser.parse_args()

if args.filter:
    filterEvents(args.filter, args.calculateFreeTime)

if args.query:
    "limited fuctionality"

    query = input("Please input: \n")
    performQuery(query, query.split()[0])

if args.gui:
    os.system('python3 /Users/ghazshahbaz/documents/eventsdatabase/events_gui.py') # runs the gui file

if args.calculateFreeTime and not args.filter:
    filterDatabase(begin_date=input("Input the first date(format month/day/year): "), end_date_filter=input("Input the secind date(format month/day/year): "),calculateFreeTime=True)

