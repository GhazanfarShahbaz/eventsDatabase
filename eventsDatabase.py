from os import times
import sqlite3 as sql 
from datetime import datetime
from stringcolor import cs 

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
                            recurs text, 
                            last_recurrance text,
                            date_added text, 
                            type_of_event text,
                            description text
                        );
                    """)

    connection.commit()
    connection.close()


def addToTable(eventName, startDate, time = None, recurs = None, last_recurrance = None, type_of_event = None, description = None) -> bool:
    if not(eventName and startDate) or (last_recurrance and not recurs):
        return False 

    connection, cursor = connectToDb()
    data = cursor.execute("Select Count(id) from events")
    count = data.fetchone()[0]

    data = cursor.execute(f'Select * from events where event_name = "{eventName}" and time = "{time if not None else null}" and begin_date = "{startDate if not None else null}" and recurs = "{recurs if not None else null}" and description = "{description if not None else null}"')

    exists = data.fetchone()

    todaysDate = datetime.now()
    dateAdded = f"{todaysDate.month}/{todaysDate.day}/{todaysDate.year}" 

    if exists:
        print("EXISts")
        return False

    #For loop to add recurring events
    cursor.execute(f'''
                        Insert into events(id, event_name, begin_date, time, recurs, last_recurrance, date_added, type_of_event, description) 
                        VALUES(
                            "{count}",
                            "{eventName}", 
                            "{startDate}", 
                            "{time if not None else null}", 
                            "{recurs if not None else null}", 
                            "{last_recurrance if not None else null}", 
                            "{dateAdded}", 
                            "{type_of_event if not None else null}", 
                            "{description if not None else null}"
                            )
                    ''')

    connection.commit()
    return True


def filterDatabase(eventName = "", begin_date = "", time = -1, recurs = "", last_recurrance = "", dateAdded = "", description = "", end_date_filter = "", end_time_filter = "", before_last_occurence=0 ) -> None:
    connection, cursor = connectToDb()

    query = "Select * from events "
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
        date_format = '%m/%d/%Y'
        try:
            datetime.strptime(begin_date, date_format)
            datetime.strptime(end_date_filter, date_format)
        except ValueError:
            return 
        
        if begin_date <= end_date_filter:
            start_date_operation = ">="
            end_date_operation = "<="
        else:
            begin_date, end_date_filter = end_date_filter, begin_date
            # start_date_operation = "<="
            # end_date_operation = ">="
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

    if not recurs:
        currentQuery = ""

        if begin_date and end_date_filter:
            currentQuery = f"or (last_recurrance >= {begin_date} and last_recurrance <= {end_date_filter} and {filterQuery[5:]})"
        elif begin_date:
            currentQuery = f"or (begin_date <= {begin_date} and last_recurrance >= {begin_date} and {backedQuery}"
            None
        
        filterQuery = f"{filterQuery} {currentQuery}"
        
    query += filterQuery
    data = cursor.execute(query)

    for row in data:
        printRow(data)
    

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


    connection.close()


def printRow(row) -> None:
    timeString = ""
    if row[3]:
        timeRow = str(row[3])
        hour = 0 
        minute = 0

        for char in timeRow[:2]:
            hour = hour*10 + char 
        
        for char in timeRow[2:]:
            minute = minute*10 + char 

        # if hour > 12:

    if not row[4]:
        rowString = f"{row[1]} occurs on {row[2]}"
    # rowString = f"{row[1]} occurs {since if row[4] else on}"
    



# createTable()
# addToTable("test", "03/20/20")


createTable()
