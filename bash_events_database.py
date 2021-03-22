import argparse
from eventsDatabase import filterData
from datetime import datetime

parser = argparse.ArgumentParser()

parser.add_argument("-f","--filter", help="Type of filter: today, month or year", type=str)

args = parser.parse_args()



def gate() -> None:
    filterEvents(args.filter)

def filterEvents(filterRange) -> None:
    acceptedArguments = {"today", "month", "year"}
    if  filterRange.strip() in acceptedArguments:
        todaysDate = datetime.now()
        if filterRange == "today":
            filterData(None, todaysDate.day, todaysDate.month, todaysDate.year, None, None, None, None, None)
        # elif filterRange == "month":
        #     filterData(None, todaysDate.day, todaysDate.month, todaysDate.year, None, None, None, None, None, stopFilter=f"{todaysDate.month +1}/ /")
        # elif filterRange == "year":
        #     filterData(None, todaysDate.day, todaysDate.month, todaysDate.year, None, None, None, None, None, stopFilter=f" / /{todaysDate.year +1}")
        

