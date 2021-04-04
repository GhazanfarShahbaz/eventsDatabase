from os import times
import sqlite3 as sql 
from datetime import datetime
from stringcolor import cs 

"""
    Notes 
    Sqlite accepts dates in the format YYYY-MM-DD 
    turn date mm/dd/yy -> YYYY-MM-DD 
    Query -> WHERE DATE(date) BETWEEN 'some date' AND 'another date'
"""


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
   12: 31
}

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

def connectToDb() -> tuple:
    connection = sql.connect("events.db")       # sql.Connection
    cursor = connection.cursor()                # sql.Cursor
    return connection, cursor   


def createTable() -> None:
    connection, cursor = connectToDb()

    cursor.execute( """
                        Create table if not exists Events(
                            id integer primary key, 
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
        datetime.strptime(date, '%Y-%m-%d')
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
    return f"{date[0]}-{date[1] if int(date[1]) >= 10 else f'0{date[1]}'}-{date[2] if int(date[2]) >= 10 else f'0{date[2]}'}"


def extendTime(time: str) -> str:
    if not time:
        time = ""

    date = "0"*(4-len(time)) + time
    return date


def addToTable(eventName, date, time = None, end_time = None, recurs = None, last_recurrance = None, type_of_event = None, description = None, start_recurrance = None) -> bool:
    time = extendTime(time)
    end_time = extendTime(end_time)
    if not (eventName or date) or (last_recurrance and not recurs) or not(validateDate(time) or validateDate(end_time) or validateDate(date) or validateDate(last_recurrance)):
        print("Failed validation")
        return False

    connection, cursor = connectToDb()
    data = cursor.execute("Select Count(id) from events")
    count = data.fetchone()[0]
    
    # data = cursor.execute(f'Select * from events where event_name = "{eventName}" and time = "{time}" and end_time = "{end_time}"and begin_date = "{date if date else None}" and recurs = "{recurs if recurs else None}" and description = "{description if description else None}"')

    exists = data.fetchone()

    todaysDate = datetime.now()
    dateAdded = extendAndFormatDate(f"{todaysDate.month}/{todaysDate.day}/{todaysDate.year}")
    date = extendAndFormatDate(date)

    if exists:
        print("This entry already exists")
        return False

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
        currentDate = date.split("/")
        currentMonth, currentDay, currentYear = int(currentDate[0]), int(currentDate[1]), int(currentDate[2])
        if not last_recurrance:
            last_recurrance = "12/31/2099"
        currentDate = f"{currentMonth}/{currentDay}/{currentYear}"
        lastDate = last_recurrance.split("/")
        if recurs == "daily":
            print("test")
            print(currentDate, last_recurrance)
            while currentDate < last_recurrance:
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
                connection.commit()
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
                
                currentDate = f"{currentMonth}/{currentDay}/{currentYear}"
                # print("Test added:", currentDate)
            print(currentDate, last_recurrance, currentDate < last_recurrance)




    connection.commit()
    return True


def filterDatabase(eventName = "", begin_date = "", time = -1, recurs = "", last_recurrance = "", eventType = "", dateAdded = "", description = "", end_date_filter = "", end_time_filter = "", before_last_occurence=0 ) -> None:
    #Add Event Type Filter
    connection, cursor = connectToDb()

    query = "Select * from Events "
    filterQuery = ""
    backedQuery = ""
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

    start_date_operation = "="
    end_date_operation = "="

    if begin_date and end_date_filter:
        # date_format = '%m/%d/%Y'
        # print(end_date_filter)
        # try:
        #     datetime.strptime(begin_date, date_format)
        #     datetime.strptime(end_date_filter, date_format)
        # except ValueError:
        #     print("Invalid Format")
        #     return 
        
        if begin_date <= end_date_filter:
            start_date_operation = ">="
            end_date_operation = "<="
        else:
            begin_date, end_date_filter = end_date_filter, begin_date
    if begin_date:
        currentQuery = ""

        if not filterQuery:
            currentQuery = f'where begin_date {start_date_operation} "{begin_date}"'

        else:
            currentQuery = f' and begin_date {start_date_operation} "{begin_date}"'
        
        filterQuery += currentQuery 
        
    if end_date_filter:
        currentQuery = ""

        if not filterQuery:
            currentQuery = f'where begin_date {end_date_operation} "{end_date_filter}"'

        else:
            currentQuery = f' and begin_date {end_date_operation} "{end_date_filter}"'
        
        filterQuery += currentQuery 
    
    if not time and end_time_filter:
        time, end_time_filter = end_time_filter, time

    start_time_operation = "="
    end_time_operation = "="

    if time and end_time_filter:
        if time <= end_time_filter:
            start_time_operation = ">="
            end_time_operation = "<="
        else:
            start_time_operation = "<="
            end_time_operation = ">="
    #Combine statement above
    if time:
        currentQuery = ""

        if not filterQuery:
            currentQuery = f'where time {start_time_operation} "{time}"'

        else:
            currentQuery = f' and time {start_time_operation} "{time}"'
        
        filterQuery += currentQuery 
        backedQuery += f'time {start_time_operation} "{time}"' if not backedQuery else  f' and time {start_time_operation} "{time}"'
        
    if end_time_filter:
        currentQuery = ""

        if not filterQuery:
            currentQuery = f'where time {end_time_operation} "{end_time_filter}"'

        else:
            currentQuery = f' and time {end_time_operation} "{end_time_filter}"'
        
        filterQuery += currentQuery 
        backedQuery += f'time {end_time_operation} "{end_time_filter}"' if not backedQuery else  f' and time {end_time_operation} "{end_time_filter}"'
    
    if recurs:
        recurs = recurs.lower()
        currentQuery = f'recurs = "{recurs}"' if recurs != "none" else f'recurs is "{null}"'
        backedQuery = currentQuery if not backedQuery else f" and {currentQuery}"
    
        if not filterQuery:
            currentQuery = "where " + currentQuery
        else: 
            currentQuery = " and" + currentQuery

        currentQuery += filterQuery

    if not recurs and filterQuery:
        currentQuery = ""
        backedQuery = "" if not backedQuery else "and" + backedQuery
        if begin_date and end_date_filter:
            currentQuery = f"or (last_recurrance >= {begin_date} and (last_recurrance <= {end_date_filter} or last_recurrance is Null) and {filterQuery[5:]})"
        elif begin_date:
            currentQuery = f"or (begin_date <= {begin_date} and (last_recurrance >= {begin_date} or last_recurrance is Null) {backedQuery})"
            None
        
        filterQuery = f"where ({filterQuery[5:]}) {currentQuery}"
        
    query += filterQuery
    print(query)
    data = cursor.execute(query)

    for row in data:
        printRow(row)
    

    connection.close()




def printDatabase() -> None:
    connection, cursor = connectToDb()

    data = cursor.execute("Select * from Events limit 1")
    isEmpty = False if data.fetchone() else True
    if isEmpty:
        print("Database is empty :(")
    else:
        data = cursor.execute("Select * from Events")
        for row in data:
            print(row)
            printRow(row)


    connection.close()


def printRow(row) -> None:
    """
    Rows[0] = id
    Rows[1] = event name
    Rows[2] = start date 
    Rows[3] = time 
    Rows[4] = end time 
    Rows[5] = recurs 
    Rows[6] = last recurrance 
    Rows[7] = date added 
    Rows[8] = type of event
    Rows[9] = description
    """
    # if row[4] == "None" or not row[4]:
    #     return
    eventString = f"""{row[1]} {dateToString(row[2])} at {timeToString(row[3])} - {timeToString(row[4])}"""

    if row[5] != "None" and row[5]:
        eventString += f" recurs {row[5]}"
        if row[6] != "None" and row[6]:
            eventString += f" until {row[6]}"

    if row[9] != "None" and row[9]:
        eventString += f" and is a {row[9]} type event"
    # print(row) 
    print(eventString)

    

def  dateToString(date: str) -> str:
    date = date.split("/")
    return f"{monthName[int(date[0])]} {dayPrefix[int(date[1])]} {date[2]}".strip()


def timeToString(timeString: int) -> str:
    timeString = str(timeString).strip()
    
    if len(timeString) < 4:
        timeString = "0"*(4-len(timeString)) + timeString
    print(timeString)
    hour = int(timeString[:2])
    amOrPm = "AM" if hour >= 12 else "PM"

    if hour  > 12:
        hour %= 12
    elif hour == 0:
        hour = 12
    hour = abs(hour)

    return f"{hour}:{timeString[2:]} {amOrPm}"

createTable()
