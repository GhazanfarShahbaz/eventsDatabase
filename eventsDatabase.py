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
                            begin_date text not null,
                            time integer,
                            end_time integer,
                            recurs text, 
                            last_recurrance text,
                            date_added text, 
                            type_of_event text,
                            description text
                        );
                    """)

    connection.commit()
    connection.close()


def addToTable(eventName, startDate, time = None, end_time = None, recurs = None, last_recurrance = None, type_of_event = None, description = None) -> bool:

    if not(eventName and startDate) or (last_recurrance and not recurs):
        return False 

    connection, cursor = connectToDb()
    data = cursor.execute("Select Count(id) from events")
    count = data.fetchone()[0]

    if not time:
        time = 0
    if not end_time:
        end_time = time
    
    data = cursor.execute(f'Select * from events where event_name = "{eventName}" and time = "{time}" and end_time = "{end_time}"and begin_date = "{startDate if startDate else None}" and recurs = "{recurs if recurs else None}" and description = "{description if description else None}"')

    exists = data.fetchone()

    todaysDate = datetime.now()
    dateAdded = f"{todaysDate.month}/{todaysDate.day}/{todaysDate.year}" 

    if exists:
        print("This entry already exists")
        return False
    
    cursor.execute(f'''
                        Insert into events(id, event_name, begin_date, time, end_time, recurs, last_recurrance, date_added, type_of_event, description) 
                        VALUES(
                            "{count}",
                            "{eventName}", 
                            "{startDate}", 
                            "{time}", 
                            "{end_time}", 
                            "{recurs if recurs else None}", 
                            "{last_recurrance if last_recurrance else None}", 
                            "{dateAdded}", 
                            "{type_of_event if type_of_event else None}", 
                            "{description if description else None}"
                            )
                    ''')

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
    if row[4] == "None" or not row[4]:
        return
    eventString = f"""{row[1]} {dateToString(row[2])} at {timeToString(row[3])} - {timeToString(row[4])}"""

    # print(row)
    print(eventString)

    

def  dateToString(date: str) -> str:
    date = date.split("/")
    return f"{monthName[int(date[0])]} {dayPrefix[int(date[1])]} {date[2]}"


def timeToString(timeString: int) -> str:
    timeString = str(timeString)
    
    if len(timeString) < 4:
        timeString = "0"*(4-len(timeString)) + timeString

    hour = int(timeString[:2])
    hour = hour - 12
    amOrPm = "AM " if hour < 0 else "PM"
    hour = abs(hour)

    return f"{hour}:{timeString[:2]} {amOrPm}"

createTable()
