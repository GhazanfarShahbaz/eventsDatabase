import sqlite3 as sql
from datetime import datetime
from stringcolor import cs

dayPrefix = {
    1: "1st",
    2: "2nd",
    3: "3rd",
    4: "4th",
    6: "6th",
    6: "6th",
    7: "7th",
    8: "8th",
    9: "9th",
    10: "10th",
    11: "11th",
    12: "12th",
    13: "13th",
    14: "14th",
    16: "16th",
    16: "16th",
    17: "17th",
    18: "18th",
    19: "19th",
    20: "20th",
    21: "21st",
    22: "22nd",
    23: "23rd",
    24: "24th",
    26: "26th",
    26: "26th",
    27: "27th",
    28: "28th",
    29: "29th",
    30: "30th",
    31: "31st",
}

allowedRecurring = {
    "no",
    "daily", 
    "monthly", 
    "yearly"
    }

def connectToDb():
    connection = sql.connect("events.db")
    return connection, connection.cursor()

def initDatabase() -> None:
    connection = sql.connect("events.db")
    cursor = connection.cursor()
    # add recurringUntil, change hour to int
    eventsTable = """
                    Create Table if not exists events(
                        name text not null,
                        day integer not null,
                        month integer not null,
                        year integer,
                        hour int,
                        minutes int,
                        recurring text,
                        endson text,
                        eventtype text,
                        dateadded text
                    );
                  """

    cursor.execute(eventsTable)

    connection.close() 

def addToDatabase(eventName: str, day: int, month: int, year: int, hour: int, minutes:int, recurring: str,endson:str, eventType: str) -> None:
    connection, cursor = connectToDb()
    date = datetime.now()

    if not(day and month and year and eventName):
        print("Missing vital information, not added")
        return
    if not hour:
        hour = 12 
    if not minutes:
        minutes = 0
    if eventType == "":
        eventType = "none"
    recurring = recurring.lower()
    if recurring not in allowedRecurring :
        recurring = "no" 
    if not endson:
        endson = "never"

    

    insertString = f'Insert into events(name, day, month, year, hour, minutes, recurring, endson, eventtype, dateadded) Values("{eventName}", "{day}", "{month}", "{year}", "{hour}","{minutes}", "{recurring}","{endson}", "{eventType}", "{date.month}/{date.day}/{date.year}")'

    cursor.execute(insertString)

    connection.commit()
    connection.close()

def printRow(rowData: tuple) -> None:
    occursOnString = ""

    minutes = str(rowData[5])
    if len(minutes) == 1:
        minutes = "0" + minutes

    amOrPm = "AM" if rowData[4] <= 12 else "PM"

    if rowData[6] == "no":
        date = f'{rowData[2]}/{rowData[1]}/{rowData[3]}'
        occursOnString = f" occurs on {cs(date, 'dodgerblue').bold()} at {cs(rowData[4], 'blue4').bold()}:{cs(minutes, 'blue4').bold()} {cs(amOrPm, 'blue4').bold()}"
    elif rowData[6] == "yearly":
        date = f"{rowData[2]}/{rowData[1]}"
        occursOnString = f" occurs on {cs(date, 'dodgerblue').bold()} every year at {cs(rowData[4], 'blue4').bold()}:{cs(minutes, 'blue4').bold()} {cs(amOrPm, 'blue4').bold()}"
    elif rowData[6] == "monthly":
        date = f"{dayPrefix[rowData[2]]}"
        occursOnString = f" occurs on the  {cs(date, 'dodgerblue').bold()} of every month at {cs(rowData[4], 'blue4').bold()}:{cs(minutes, 'blue4').bold()} {cs(amOrPm, 'blue4').bold()}"
    elif rowData[6] == "daily":
        occursOnString = f" occurs {cs('every day', 'dodgerblue').bold()} at {cs(rowData[4], 'blue4').bold()}:{cs(minutes, 'blue4').bold()} {cs(amOrPm, 'blue4').bold()}"
    print(f'{cs(rowData[0], "grey4").bold()}{occursOnString}')

def printDatabase() -> None:
    connection, cursor = connectToDb()
    data = cursor.execute("Select * from Events")
    for row in data:
        printRow(row)
    
    connection.close()

def databaseToCsv() -> None:
    connection, cursor = connectToDb()
    data = cursor.execute("Select * from Events")
    

    currentFile = open("events.csv", "w")

    columnString = ""
    for t in data.description:
        columnString += t[0] + ", "

    columnString = columnString[:len(columnString)-2]
    currentFile.write(columnString + "\n")

    for eventRow in data:
        eventString = eventRow[0]
        for columns in eventRow[1:]:
            eventString += f", {columns}"

        currentFile.write(eventString + "\n")

    currentFile.close()
    connection.close()

def filterByName(eventName: str, exactMatch: bool) -> None:
    connection, cursor = connectToDb()
    data = None
    if exactMatch:
        data = cursor.execute(f'Select * from events where name = "{eventName}"')
    else:
        data = cursor.execute(f'Select * from events where name like "%{eventName}%"') 

    for row in data:
        printRow(row)
    if not data:
        print("No results found")
    connection.close()

def filterData(eventName: str, day: int, month: int, year: int, hour: int, minute:int, recurring: str, endson: str, eventType: str, exactEventName=False,  before= False, after = False, beforeHour = False, afterHour = False, beforeEndsOn = False,afterEndsOn = False, beforeMinute = False, afterMinute = False, stopFilter = "") -> None:
    """Add date filter"""
    connection, cursor = connectToDb()
    query = 'Select * from events'
    filterString = ""
    if eventName:
        curr = ""

        if exactEventName:
            curr = f'name = "{eventName}"'
        else:
            curr = f'name like "%{eventName}%"'
        
        filterString += f' and {curr}' if filterString else f" where {curr}"

    if recurring and recurring in allowedRecurring:
        curr = f'recurring = "{recurring}"'
        filterString += f' and {curr}' if filterString else f" where {curr}"
    
    if eventType:
        curr = f'eventtype = "{eventType}"'
        filterString += f' and {curr}' if filterString else f" where {curr}"

    if day or month or year and not(before and after):
        operation = "="
        if before or after:
            operation = ">=" if after else "<=" 

        if day: 
            curr = f'day {operation} "{day}"'
            filterString += f' and {curr}' if filterString else f" where {curr}"

        if month:
            curr = f'month {operation} "{month}"'
            filterString += f' and {curr}' if filterString else f" where {curr}"

        if year:
            curr = f'year {operation} "{year}"'
            filterString += f' and {curr}' if filterString else f" where {curr}"
    
    if hour and not(beforeHour and afterHour):
        operation = "="
        if beforeHour or afterHour:
            operation = ">=" if afterHour else "<=" 
        
        curr = f'hour {operation} "{hour}"'
        filterString += f' and {curr}' if filterString else f" where {curr}"

    if minute!= -1 and minute -1 >= 0 and not(beforeMinute and afterMinute):
        operation = "="
        if beforeMinute or afterMinute:
            operation = ">=" if afterMinute else "<=" 
        
        curr = f'minutes {operation} "{minute}"'
        filterString += f' and {curr}' if filterString else f" where {curr}"

    if endson and not(beforeEndsOn and afterEndsOn):
        operation = "="
        if beforeEndsOn or afterEndsOn:
            operation = ">=" if afterEndsOn else "<=" 
        
        curr = f'endson {operation} "{endson}"'
        filterString += f' and {curr}' if filterString else f" where {curr}"

    if stopFilter:
        stopFilter = stopFilter.split("/")
        if stopFilter[0].strip():
            curr = f'month < "{stopFilter[0]}"'
            filterString += f' and {curr}' if filterString else f" where {curr}"
        if stopFilter[1].strip():
            curr = f'day < "{stopFilter[1]}"'
            filterString += f' and {curr}' if filterString else f" where {curr}"
        if stopFilter[2].strip():
            curr = f'year < "{stopFilter[2]}"'
            filterString += f' and {curr}' if filterString else f" where {curr}"

    query += filterString

    data = cursor.execute(query)
    print(query)
    for row in data:
        printRow(row)
    if not data:
        print("No results found")
    connection.close()
