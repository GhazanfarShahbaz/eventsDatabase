import argparse
from eventsDatabase import filterData, monthDays
from datetime import date, datetime

parser = argparse.ArgumentParser()

parser.add_argument("-f","--filter", help="Type of filter: today, month or year", type=str)

args = parser.parse_args()



def gate() -> None:
    filterEvents(args.filter)

def filterEvents(filterRange) -> None:
    acceptedArguments = {"today", "weekly" "month", "year"}
    if  filterRange.strip() in acceptedArguments:
        todaysDate = datetime.now()
        if filterRange == "today":
            filterData(begindate=f"{todaysDate.month}/{todaysDate.day}/{todaysDate.year}")

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
                    
            filterData(begindate=f"{firstMonth}/{firstDay}/{firstYear}", end_date_filter=f"{lastMonth}/{lastDay}/{lastMonth}" )

        elif filterRange == "month":
            filterData(begindate=f"{todaysDate.month}/{1}/{todaysDate.year}", end_date_filter=f"{todaysDate.month}/{monthDays[todaysDate.month]}/{todaysDate.year}" )

        elif filterRange == "month":
            filterData(begindate=f"{1}/{1}/{todaysDate.year}", end_date_filter=f"{1}/{1}/{todaysDate.yea + 1}" )