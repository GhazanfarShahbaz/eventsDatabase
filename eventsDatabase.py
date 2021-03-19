import sqlite3 as sql
from sqlite3.dbapi2 import connect
import tkinter as tk 
import datetime 

from stringcolor import cs

dayPrefix = {
    1: "1st",
    2: "2nd",
    3: "3rd",
    4: "4th",
    5: "5th",
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
    27: "27th",
    28: "28th",
    29: "29th",
    30: "30th",
    31: "31st",
}

def connectToDb():
    connection = sql.connect("events.db")
    return connection, connection.cursor()


def initDatabase() -> None:
    connection = sql.connect("events.db")
    cursor = connection.cursor()

    eventsTable = """
                    Create Table if not exists events(
                        name text not null,
                        day integer not null,
                        month integer not null,
                        year integer,
                        time text,
                        recurring text,
                        eventtype text
                    );
                  """

    cursor.execute(eventsTable)

    connection.close() 

def addToDatabase(eventName: str, day: int, month: int, year: int, time: str, recurring: str, eventType: str) -> None:
    connection, cursor = connectToDb()

    if recurring == "":
        recurring = "no" 

    insertString = f'Insert into events(name, day, month, year, time, recurring, eventtype) Values("{eventName}", "{day}", "{month}", "{year}", "{time}", "{recurring}", "{eventType}")'

    cursor.execute(insertString)

    connection.commit()
    connection.close()

def printRow(rowData) -> None:
    occursOnString = ""
    if rowData[5] == "no":
        date = f'{rowData[2]}/{rowData[1]}/{rowData[3]}'
        occursOnString = f" occurs on {cs(date, 'dodgerblue').bold()} at {cs(rowData[4], 'blue4').bold()}"
    elif rowData[5] == "yearly":
        date = f"{rowData[2]}/{rowData[1]}"
        occursOnString = f" occurs on {cs(date, 'dodgerblue').bold()} every year at {cs(rowData[4], 'yellow').bold()}"
    elif rowData[5] == "monthly":
        date = f"{dayPrefix[rowData[2]]}"
        occursOnString = f" occurs on the  {cs(date, 'dodgerblue').bold()} of every month at {cs(rowData[4], 'blue4').bold()}"
    elif rowData[5] == "daily":
        occursOnString = f" occurs {cs('every day', 'dodgerblue').bold()} at {cs(rowData[4], 'blue4').bold()}"
    print(f'{cs(rowData[0], "grey4").bold()}{occursOnString}')


def printDatabase() -> None:
    connection, cursor = connectToDb()
    data = cursor.execute("Select * from Events")
    
    for row in data:
        printRow(row)
    
    connection.close()


def filterData(eventName: str, day: int, month: int, year: int, time: str, recurring: str, eventType: str) -> None:
    None


# initDatabase()
# addToDatabase("My Birthday", 27, 8, 2001, "12:00 AM", "yearly", "birthday")
printDatabase()