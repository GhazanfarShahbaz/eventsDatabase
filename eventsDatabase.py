from os import times
import sqlite3 as sql 
from datetime import datetime
from stringcolor import cs 

monthDays = {
   1: 31, 
   2: 28, #28 during leap year
   3: 31, 
   4: 30, 
   5: 31, 
   6: 30,
   7: 31,
   8: 31,
   9: 30,
   10: 31,
   11: 30,
   12: 31
}

dayPrefix = {
    1: "1st",
    2: "2nd",
    3: "3rd",
    4: "4th",
    5: "5th",
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
    15: "15th",
    16: "16th",
    17: "17th",
    18: "18th",
    19: "19th",
    20: "20th",
    21: "21st",
    22: "22nd",
    23: "23rd",
    24: "24th",
    25: "25th",
    26: "26th",
    26: "26th",
    27: "27th",
    28: "28th",
    29: "29th",
    30: "30th",
    31: "31st",
}

monthName = {
    1: "January", 
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

allowed_recurs = {"no", "daily", "weekly", "monthly", "yearly"}
weekdays = {
    "m": 1,
    "t" : 2, 
    "w": 3, 
    "th": 4, 
    "f": 5, 
    "sat": 6, 
    "sun": 0
}

vowels = {'a', 'e', 'i', 'o', 'u'}

def connectToDb() -> tuple:
    connection = sql.connect("/Users/ghazshahbaz/documents/tools/eventsdatabase/events.db")       # sql.Connection
    cursor = connection.cursor()                # sql.Cursor
    return connection, cursor   


def createTable() -> None:
    connection, cursor = connectToDb()

    cursor.execute( """
                        Create table if not exists Events(
                            id integer not null, 
                            event_name text not null,
                            date text not null,
                            time integer,
                            end_time integer,
                            recurs text,
                            start_recurrance text, 
                            last_recurrance text,
                            date_added text, 
                            type_of_event text,
                            description text
                        );
                    """)

    connection.commit()
    connection.close()

def validateDate(date: str) -> bool:
    if not date:
        return True

    try:
        datetime.strptime(date, '%m/%d/%Y')
    except ValueError:
        return False
    return True

def validateTime(time: str) -> bool:
    try:
        int(time)
    except ValueError:
        return False
    hour = int(time[:2])
    if hour >= 24:
        return False 
    return True if int(time[2:]) < 60 else False

def extendAndFormatDate(date: str) -> str:
    dateList = date.split("/")
    return f"{dateList[2]}-{dateList[0] if int(dateList[0]) >= 10  or len(dateList[0]) > 1 else f'0{dateList[0]}'}-{dateList[1] if int(dateList[1]) >= 10  or len(dateList[1]) > 1 else f'0{dateList[1]}'}"


def extendTime(time: str) -> str:
    if not time:
        time = ""

    date = "0"*(4-len(time)) + time
    return date

def chechIfLeapYear(year) -> bool:
    """
        year: int 
        returns true if a year is a leap year false if not 
    """
    # a number is a leap year if it is divisible by 4 of divisible by 100 and 400
    return (year%4 == 0 and (year%100 > 0 or (year%100 == 0 and year%400 == 0)))


def addToTable(eventName, date, time = None, end_time = None, recurs = None, last_recurrance = None, type_of_event = None, description = None, start_recurrance = None) -> bool:
    time = extendTime(time)
    end_time = extendTime(end_time)
    if not (eventName or date) or (last_recurrance and not recurs) or not(validateTime(time) or validateTime(end_time) or validateDate(date) or validateDate(last_recurrance)):
        print("Failed validation")
        return False

    connection, cursor = connectToDb()
    data = cursor.execute("Select Count(distinct(id)) from events")
    count = data.fetchone()[0]
    
    #check for duplicates

    todaysDate = datetime.now()
    dateAdded = extendAndFormatDate(f"{todaysDate.month}/{todaysDate.day}/{todaysDate.year}")
    date = extendAndFormatDate(date)


    recurs = recurs.lower() if recurs else "no" 

    if recurs == "no":
        cursor.execute(f'''
                            Insert into events(id, event_name, date, time, end_time, recurs, last_recurrance, start_recurrance, date_added, type_of_event, description) 
                            VALUES(
                                "{count}",
                                "{eventName}", 
                                "{date}", 
                                "{time}", 
                                "{end_time}", 
                                "{recurs}", 
                                "{last_recurrance if last_recurrance else None}", 
                                "{start_recurrance if start_recurrance else None}", 
                                "{dateAdded}", 
                                "{type_of_event if type_of_event else None}", 
                                "{description if description else None}"
                                )
                        ''')
    else:
        currentDate = date.split("-")
        currentYear, currentMonth, currentDay = int(currentDate[0]), int(currentDate[1]), int(currentDate[2])

        if not last_recurrance:
            last_recurrance = "2099-12-31"
        else:
            last_recurrance = extendAndFormatDate(last_recurrance)
        lastDate = last_recurrance.split("-") 
        lastDatetime = datetime(int(lastDate[0]), int(lastDate[1]), int(lastDate[2])) #yy mm dd
        currentDate = extendAndFormatDate(f"{currentMonth}/{currentDay}/{currentYear}")
        print("Started Adding")
        
        if recurs == "daily":
            while datetime(currentYear, currentMonth , currentDay) <= lastDatetime:
                cursor.execute(f'''
                        Insert into events(id, event_name, date, time, end_time, recurs, last_recurrance, start_recurrance, date_added, type_of_event, description) 
                        VALUES(
                            "{count}",
                            "{eventName}", 
                            "{currentDate}", 
                            "{time}", 
                            "{end_time}", 
                            "{recurs}", 
                            "{last_recurrance}", 
                            "{date}", 
                            "{dateAdded}", 
                            "{type_of_event if type_of_event else None}", 
                            "{description if description else None}"
                            )
                    ''')
                if currentMonth != 2 or (not chechIfLeapYear(currentYear)):
                    if currentDay + 1 <= monthDays[currentMonth]:
                        currentDay += 1
                    elif currentDay + 1 > monthDays[currentMonth]:
                        if currentMonth < 12:
                            currentMonth += 1
                            currentDay = 1
                        else:
                            currentMonth = 1
                            currentDay = 1
                            currentYear += 1
                else:
                    if currentDay + 1 <= 29:
                        currentDay += 1
                    else:
                        currentMonth += 1
                        currentDay = 1
                    
                
                currentDate = extendAndFormatDate(f"{currentMonth}/{currentDay}/{currentYear}")
        

        elif recurs == "weekly":
            while datetime(currentYear, currentMonth , currentDay) <= lastDatetime:
                cursor.execute(f'''
                        Insert into events(id, event_name, date, time, end_time, recurs, last_recurrance, start_recurrance, date_added, type_of_event, description) 
                        VALUES(
                            "{count}",
                            "{eventName}", 
                            "{currentDate}", 
                            "{time}", 
                            "{end_time}", 
                            "{recurs}", 
                            "{last_recurrance}", 
                            "{date}", 
                            "{dateAdded}", 
                            "{type_of_event if type_of_event else None}", 
                            "{description if description else None}"
                            )
                ''')
                currentDay += 7
                if currentDay > monthDays[currentMonth]:
                    if currentMonth != 2 or (not chechIfLeapYear(currentYear)):
                        currentDay %= monthDays[currentMonth] 
                    else:
                        currentDay %= 29
                    if currentMonth < 12:
                        currentMonth += 1
                    else:
                        currentMonth = 1
                        currentYear += 1
                currentDate = extendAndFormatDate(f"{currentMonth}/{currentDay}/{currentYear}")

        elif recurs == "monthly":
            while datetime(currentYear, currentMonth , currentDay) <= lastDatetime:
                cursor.execute(f'''
                        Insert into events(id, event_name, date, time, end_time, recurs, last_recurrance, start_recurrance, date_added, type_of_event, description) 
                        VALUES(
                            "{count}",
                            "{eventName}", 
                            "{currentDate}", 
                            "{time}", 
                            "{end_time}", 
                            "{recurs}", 
                            "{last_recurrance}", 
                            "{date}", 
                            "{dateAdded}", 
                            "{type_of_event if type_of_event else None}", 
                            "{description if description else None}"
                            )
                ''')
                currentMonth += 1
                if currentMonth > 12:
                    currentMonth = 1
                    currentYear += 1
        
                currentDate = extendAndFormatDate(f"{currentMonth}/{currentDay}/{currentYear}")
        elif recurs == "yearly":
            while datetime(currentYear, currentMonth , currentDay) <= lastDatetime:
                cursor.execute(f'''
                        Insert into events(id, event_name, date, time, end_time, recurs, last_recurrance, start_recurrance, date_added, type_of_event, description) 
                        VALUES(
                            "{count}",
                            "{eventName}", 
                            "{currentDate}", 
                            "{time}", 
                            "{end_time}", 
                            "{recurs}", 
                            "{last_recurrance}", 
                            "{date}", 
                            "{dateAdded}", 
                            "{type_of_event if type_of_event else None}", 
                            "{description if description else None}"
                            )
                ''')

                currentYear += 1

                currentDate = extendAndFormatDate(f"{currentMonth}/{currentDay}/{currentYear}")
        else:
            recurs = recurs.split(",")
            days = set()
            for recur in recurs:
                if recur not in weekdays.keys():
                    print("Invalid sequence")
                    return False
                else:
                    days.add(weekdays[recur])
            
            recurString = ""
            recurList = sorted(recurs)
            recurString = recurList[0]

            for recur in recurList[1:]:
                recurString += f"/{recur}"

            while datetime(currentYear, currentMonth , currentDay) <= lastDatetime:
                if int(datetime(currentYear, currentMonth, currentDay).strftime("%w")) in days: #datetime.strptime(currentDate, '%Y-%m-%d').isoweekday() in days:
                   cursor.execute(f'''
                        Insert into events(id, event_name, date, time, end_time, recurs, last_recurrance, start_recurrance, date_added, type_of_event, description) 
                        VALUES(
                            "{count}",
                            "{eventName}", 
                            "{currentDate}", 
                            "{time}", 
                            "{end_time}", 
                            "{recurString}", 
                            "{last_recurrance}", 
                            "{date}", 
                            "{dateAdded}", 
                            "{type_of_event if type_of_event else None}", 
                            "{description if description else None}"
                            )
                    ''')

                if currentMonth != 2 or not chechIfLeapYear(currentYear):
                    if currentDay + 1 <= monthDays[currentMonth]:
                        currentDay += 1
                    elif currentDay + 1 > monthDays[currentMonth]:
                        if currentMonth < 12:
                            currentMonth += 1
                            currentDay = 1
                        else:
                            currentMonth = 1
                            currentDay = 1
                            currentYear += 1
                else:
                    if currentDay + 1 <= 29:
                        currentDay += 1
                    else:
                        currentMonth += 1
                        currentDay = 1
                
                currentDate = extendAndFormatDate(f"{currentMonth}/{currentDay}/{currentYear}")

                

        print("Finished adding")



    connection.commit()
    return True


def filterDatabase(eventName = "", begin_date = "", time = -1, recurs = "", last_recurrance = "", eventType = "", dateAdded = "", description = "", end_date_filter = "", end_time_filter = "", before_last_occurence=0, calculateFreeTime=False) -> None:
    #Add Event Type Filter
    query = "Select * from Events "
    filterQuery = ""
    if eventName:
        currentQuery = ""
        eventName = eventName.lower()

        if not filterQuery:
            currentQuery = f'where event_name = "{eventName}"'

        else:
            currentQuery = f' and event_name = "{eventName}"'
        
        filterQuery += currentQuery 

    if not begin_date and end_date_filter: 
        begin_date, end_date_filter = end_date_filter, begin_date

    if begin_date and end_date_filter:
        begin_date = extendAndFormatDate(begin_date)
        end_date_filter = extendAndFormatDate(end_date_filter)
        currentQuery = ""

        if not filterQuery:
            currentQuery = f'where date(date) between "{begin_date}" and "{end_date_filter}"'
        else:
            currentQuery = f' and date(date) between "{begin_date}" and "{end_date_filter}"'
        
        filterQuery += currentQuery
    elif begin_date:
        begin_date = extendAndFormatDate(begin_date)
        currentQuery = ""

        if not filterQuery:
            currentQuery = f'where date = "{begin_date}"'

        else:
            currentQuery = f' and date = "{begin_date}"'
        
        filterQuery += currentQuery 
    
    if not time and end_time_filter:
        time, end_time_filter = end_time_filter, time

    start_time_operation = "="
    end_time_operation = "="

    if time != -1 and end_time_filter:
        if time <= end_time_filter:
            start_time_operation = ">="
            end_time_operation = "<="
        else:
            start_time_operation = "<="
            end_time_operation = ">="
    #Combine statement above
    if time != -1:
        currentQuery = ""

        if not filterQuery:
            currentQuery = f'where time {start_time_operation} "{time}"'

        else:
            currentQuery = f' and time {start_time_operation} "{time}"'
        
        filterQuery += currentQuery 
        
    if end_time_filter:
        currentQuery = ""

        if not filterQuery:
            currentQuery = f'where time {end_time_operation} "{end_time_filter}"'

        else:
            currentQuery = f' and time {end_time_operation} "{end_time_filter}"'
        
        filterQuery += currentQuery 
    
    if recurs:
        recurs = recurs.lower()
        currentQuery = f'recurs = "{recurs}"' if recurs != "none" else f'recurs is "{None}"'
    
        if not filterQuery:
            currentQuery = "where " + currentQuery
        else: 
            currentQuery = " and" + currentQuery

        filterQuery += currentQuery
    
    query += filterQuery
    if not calculateFreeTime:
        performQuery(query, "select")
    else:
        performQuery(query, "calculate")


def printDatabase() -> None:
    connection, cursor = connectToDb()

    data = cursor.execute("Select * from Events limit 1")
    isEmpty = False if data.fetchone() else True
    if isEmpty:
        print("Database is empty :(")
    else:
        data = cursor.execute("Select * from Events group by id")
        for row in data:
            printRow(row)

    connection.close()


def performQuery(query, selectType) -> None:
    connection, cursor = connectToDb()
    if selectType == "select":
        data = cursor.execute(query + " limit 1")
        filterType = None
        try:
            filterType = query.split()[1] 
        except:
            print("Error")
            return

        printFull = True if filterType.strip() == "*" else False
        if not data.fetchone():
            print("No results to print.")
        else:
            print("Events")
            query += " group by id ORDER BY date(date) ASC, time ASC"
            data = cursor.execute(query)

            for row in data:
                if printFull:
                    printRow(row)
                else:
                    print(row)

        print()

    elif selectType == "calculate":
        data = cursor.execute(query + " limit 1")

        if not data.fetchone():
            print("No results to print.")
        else: 
            query += " ORDER BY date(date) ASC, time ASC" # using distinct will exclude dates
            calculateFreeTime(cursor.execute(query))
    else:
        cursor.execute(query)
        connection.commit()
    connection.close()


def printRow(row) -> None:
    if row[4] == "None" or not row[4]:
        return
    eventString = f"""{cs(row[1], "dodgerblue")} {dateToString(row[2])} at {timeToString(row[3])} - {timeToString(row[4])}"""
    if row[5] != "None" and row[5]:
        eventString += f" recurs {orderRecurrance(row[5])}"
        if row[6] != "None" and row[6]:
            eventString += f" until {dateToString(row[7])}"

    if row[9] != "None" and row[9]:
        eventString += f" and is {'a' if row[9][0].lower() not in vowels else 'an'} {cs(row[9], 'blue3')} type event"

    print(eventString)

def orderRecurrance(reccuranceString: str) -> str:
    string = reccuranceString

    if "/" in reccuranceString:
        listForm = [None,None,None,None,None,None,None]

        for day in reccuranceString.split("/"):
            listForm[weekdays[day]] = day 

        string = ""
        for days in listForm:
            if days:
                if not string:
                    string += days
                else:
                    string += "/" + days

    return cs(string, "red")

def dateToString(date: str) -> str:
    date = date.split("-")
    return cs(f"{monthName[int(date[1])]} {dayPrefix[int(date[2])]} {date[0]}".strip(), "grey4")


def timeToString(timeString: int) -> str:
    timeString = str(timeString).strip()
    
    if len(timeString) < 4:
        timeString = "0"*(4-len(timeString)) + timeString
    hour = int(timeString[:2])
    amOrPm = "AM" if hour < 12 else "PM"

    if hour  > 12:
        hour %= 12
    elif hour == 0:
        hour = 12
    hour = abs(hour)

    return cs(f"{hour}:{timeString[2:]} {amOrPm}", "yellow")

def databaseToCsv() -> None:
    connection, cursor = connectToDb()
    data = cursor.execute("Select * from Events")

    currentFile = open("/Users/ghazshahbaz/documents/eventsdatabase/events.csv", "w")

    columnString = ""
    for t in data.description:
        columnString += t[0] + ", "

    columnString = columnString[:len(columnString)-2]
    currentFile.write(columnString + "\n")

    for eventRow in data:
        eventString = str(eventRow[0])
        for columns in eventRow[1:]:
            eventString += f", {columns}"

        currentFile.write(eventString + "\n")

    currentFile.close()
    connection.close()


def calculateFreeTime(data: list) -> None:
    # can be improved by checking if specific events have been seen together before so that appending wont be needed
    print("Events")

    timesTaken = {}
    eventsSeen = set()
    for row in data:
        if row[2] not in eventsSeen:
            printRow(row)
            eventsSeen.add(row[2])

        if row[2] not in timesTaken.keys():
            if not (row[3] == row[4] and row[3] == 0): # this would be the default insert where time is 0000
                timesTaken[row[2]] = [[row[3], row[4]]]
        else:
            addTimeStart = row[3]
            addTimeEnd = row[4]

            #data is ordered only need to check previous entry for collision
            previous = timesTaken[row[2]][-1] 
            if not previous[1] < addTimeStart and not previous[0] > addTimeEnd:
                timesTaken[row[2]][-1] = [min(previous[0], addTimeStart), max(previous[1], addTimeEnd)]
            else:
                timesTaken[row[2]].append([addTimeStart, addTimeEnd])

    print("\nFree Times")
    for date, times in timesTaken.items():
        previousTimes = 800
        print(dateToString(date), end = ": ")
        length = len(times)
        current = 0
        for start, end in times:
            if current == 0 and start < previousTimes:
                previousTimes = start 
            elif current > 0:
                print(cs(", ", 'white'), end="")
                if current == length - 1 and end >= 2200:
                    print("and ", end="")
                
            print(cs(f"{timeToString(previousTimes)} to {timeToString(start)}", 'yellow'), end="")
            previousTimes = end
            current += 1

        if previousTimes < 2200: #2200 is sleep time :)
            if current > 0:
                print(cs(", and ", 'white'), end="")
            print(cs(f"{timeToString(previousTimes)} to {timeToString(2200)}", 'yellow'))

        if length  == 0:
            print(cs("No free times on this day", "red"))

    print(cs("Note: Dates not included are either free or full for the whole day\n", "red").bold())
                    


    
        