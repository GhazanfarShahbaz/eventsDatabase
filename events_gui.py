from datetime import date
import tkinter as tk
import PySimpleGUI as sg
from eventsDatabase import addToTable, filterDatabase, printDatabase

def addToDatabaseLabels() -> None:
    def addToDatabaseGate() -> None:
        event_name = event_name_input.get().strip()
        begin_date = begin_date_input.get().strip()
        time = time_input.get().strip()
        recurs = recurs_input.get().strip()
        last_reccurance = last_reccurance_input.get().strip()
        type_of_event = type_of_event_input.get().strip()
        description = desription_input.get().strip()
        addToTable(event_name, begin_date, time, recurs, last_reccurance, type_of_event, description)

    event_name_text = tk.Label(root, text = "Event Name:")
    window.create_window(57, 50, window=event_name_text)  
    event_name_input = tk.Entry(root) 
    window.create_window(200, 50, window=event_name_input)

    begin_date_text = tk.Label(root, text = "Begin Date:")
    window.create_window(60 , 75, window=begin_date_text)
    begin_date_input = tk.Entry(root) 
    window.create_window(200, 75, window=begin_date_input)  

    time_text = tk.Label(root, text = "Time:")
    window.create_window(79, 100, window=time_text)  
    time_input = tk.Entry(root) 
    window.create_window(200, 100, window=time_input)

    recurs_text = tk.Label(root, text = "Recurs:")
    window.create_window(74, 125, window=recurs_text)  
    recurs_input = tk.Entry(root) 
    window.create_window(200, 125, window=recurs_input)

    last_reccurance_text = tk.Label(root, text = "Last Recurrance:")
    window.create_window(46, 150, window=last_reccurance_text)  
    last_reccurance_input = tk.Entry(root) 
    window.create_window(200, 150, window=last_reccurance_input)

    type_of_event_text = tk.Label(root, text = "Type of Event:")
    window.create_window(55, 175, window=type_of_event_text) 
    type_of_event_input = tk.Entry(root) 
    window.create_window(200, 175, window=type_of_event_input)

    desription_text = tk.Label(root, text = "Description:")
    window.create_window(62, 200, window=desription_text)  
    desription_input = tk.Entry(root) 
    window.create_window(200, 200, window=desription_input)

    button_one = tk.Button(root, text='Add to Database', command=addToDatabaseGate)
    button_one.config(fg="white")
    window.create_window(193, 275, window=button_one)

def filterDataLabels() -> None:
    def filterDataGate():
        event_name = event_name_2_input.get().strip()
        begin_date = begin_date_2_input.get().strip()
        recurs = recurs_2_input.get().strip()
        time = time_2_input.get().strip()
        if time:
            time = int(time)
        last_reccurance = last_reccurance_2_input.get().strip()

        if last_reccurance:
            last_reccurance = int(last_reccurance)

        last_reccurance = last_reccurance_2_input.get().strip()
        type_of_event = type_of_event_2_input.get().strip()
        date_added = date_added_input.get().strip()
        description = description_2_input.get().strip()
        end_date = end_date_filter_input.get().strip()
        end_time = end_time_filter_input.get().strip()

        filterDatabase(event_name, begin_date, time, recurs, last_reccurance, type_of_event, date_added, description, end_date, end_time)

    event_name_2_text = tk.Label(root, text = "Event Name:")
    window.create_window(57, 350, window=event_name_2_text)

    event_name_2_input = tk.Entry(root)
    window.create_window(200,350, window=event_name_2_input) 

    begin_date_2_text = tk.Label(root, text = "Begin Date:")
    window.create_window(60, 375, window=begin_date_2_text)

    begin_date_2_input = tk.Entry(root)
    window.create_window(200,375, window=begin_date_2_input) 

    time_2_text = tk.Label(root, text = "Time:")
    window.create_window(79, 400, window=time_2_text)

    time_2_input = tk.Entry(root)
    window.create_window(200,400, window=time_2_input) 

    recurs_2_text = tk.Label(root, text = "Recurs:")
    window.create_window(73, 425, window=recurs_2_text)

    recurs_2_input = tk.Entry(root)
    window.create_window(200,425, window=recurs_2_input) 

    last_reccurance_2_text = tk.Label(root, text = "Last Recurrance:")
    window.create_window(45, 450, window=last_reccurance_2_text)

    last_reccurance_2_input = tk.Entry(root)
    window.create_window(200,450, window=last_reccurance_2_input) 

    type_of_event_2_text = tk.Label(root, text = "Event Type:")
    window.create_window(60, 475, window=type_of_event_2_text)

    type_of_event_2_input = tk.Entry(root)
    window.create_window(200, 475, window=type_of_event_2_input) 

    date_added_text= tk.Label(root, text = "Date Added:")
    window.create_window(59, 500, window=date_added_text)

    date_added_input = tk.Entry(root)
    window.create_window(200,500, window=date_added_input) 

    description_2_text = tk.Label(root, text = "Description:")
    window.create_window(60, 525, window=description_2_text)

    description_2_input = tk.Entry(root)
    window.create_window(200,525, window=description_2_input) 

    end_date_filter_text = tk.Label(root, text = "End Date:")
    window.create_window(66, 550, window=end_date_filter_text)

    end_date_filter_input = tk.Entry(root)
    window.create_window(200,550, window=end_date_filter_input) 


    end_time_filter_text = tk.Label(root, text = "End Time:")
    window.create_window(66, 575, window=end_time_filter_text)

    end_time_filter_input = tk.Entry(root)
    window.create_window(200,575, window=end_time_filter_input) 

    checkbox_before_last_occurence =  tk.IntVar(root)
    checkbox_before_last_occurence_button = tk.Checkbutton(root, text="Before Last Occurence", variable=checkbox_before_last_occurence)
    window.create_window(185, 600, window=checkbox_before_last_occurence_button) 

    button_two = tk.Button(root, text='Filter Data', command=filterDataGate)
    button_two.config(fg="white")
    window.create_window(193, 700, window=button_two)

root=tk.Tk()

window = tk.Canvas(root, width=350, height=1000)
window.pack()

addToDatabaseLabels()
filterDataLabels()

button_three = tk.Button(root, text='Print Database', command=printDatabase)
button_three.config(fg="white")
window.create_window(193, 725, window=button_three)

exitButton = tk.Button(root, text="Quit", command=root.quit)  # Close Button
window.create_window(200, 800, window=exitButton)

root.mainloop()
