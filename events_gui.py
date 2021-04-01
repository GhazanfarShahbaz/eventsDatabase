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

        minutes = minutes_2_input.get().strip()
        if minutes == "":
            minutes = -1
        else:
            minutes = int(minutes)
        
        type_of_event = type_of_event_2_input.get().strip()
        desription = ends_on_2_input.get().strip()
        event_type = event_type_2_input.get().strip()
        event_name_exact =  checkbox_exact_event_name.get()
        before = checkbox__before.get()
        after = checkbox__after.get()
        before_last_reccurance = checkbox_last_reccurance_before.get()
        after_last_reccurance =  checkbox_last_reccurance_after.get()
        before_minute = checkbox_minute_before.get()
        after_minute = checkbox_minute_after.get() 
        before_ends_on = checkbox_desription_before.get()
        after_ends_on = checkbox_desription_after.get()

        filterDatabase(event_name, begin_date, time, recurs, last_reccurance, minutes, type_of_event, desription, event_name_exact, event_type, before, after, before_last_reccurance, after_last_reccurance, before_ends_on, after_ends_on, before_minute, after_minute)

    event_name_2_text = tk.Label(root, text = "Event Name:")
    window.create_window(57, 350, window=event_name_2_text)

    event_name_2_input = tk.Entry(root)
    window.create_window(200,350, window=event_name_2_input) 

    begin_date_2_text = tk.Label(root, text = "begin_date:")
    window.create_window(82, 375, window=begin_date_2_text)

    begin_date_2_input = tk.Entry(root)
    window.create_window(200,375, window=begin_date_2_input) 

    time_2_text = tk.Label(root, text = "time:")
    window.create_window(74, 400, window=time_2_text)

    time_2_input = tk.Entry(root)
    window.create_window(200,400, window=time_2_input) 

    recurs_2_text = tk.Label(root, text = "recurs:")
    window.create_window(80, 425, window=recurs_2_text)

    recurs_2_input = tk.Entry(root)
    window.create_window(200,425, window=recurs_2_input) 

    last_reccurance_2_text = tk.Label(root, text = "last_reccurance:")
    window.create_window(80, 450, window=last_reccurance_2_text)

    last_reccurance_2_input = tk.Entry(root)
    window.create_window(200,450, window=last_reccurance_2_input) 

    minutes_2_text = tk.Label(root, text = "Minutes:")
    window.create_window(71, 475, window=minutes_2_text)

    minutes_2_input = tk.Entry(root)
    window.create_window(200,475, window=minutes_2_input) 

    type_of_event_2_text = tk.Label(root, text = "type_of_event:")
    window.create_window(65, 500, window=type_of_event_2_text)

    type_of_event_2_input = tk.Entry(root)
    window.create_window(200,500, window=type_of_event_2_input) 

    ends_on_2_text = tk.Label(root, text = "Ends On:")
    window.create_window(70, 525, window=ends_on_2_text)

    ends_on_2_input = tk.Entry(root)
    window.create_window(200,525, window=ends_on_2_input) 

    event_type_2_text = tk.Label(root, text = "Event Type:")
    window.create_window(61, 550, window=event_type_2_text)

    event_type_2_input = tk.Entry(root)
    window.create_window(200,550, window=event_type_2_input) 


    checkbox__before = tk.IntVar(root)
    checkBox__before_button = tk.Checkbutton(root, text=" Before", variable=checkbox__before)
    window.create_window(100, 575, window=checkBox__before_button) 


    checkbox__after = tk.IntVar(root)
    checkBox__after_button = tk.Checkbutton(root, text=" After", variable=checkbox__after)
    window.create_window(225, 575, window=checkBox__after_button) 


    checkbox_desription_before = tk.IntVar(root)
    checkBox_desription_before_button = tk.Checkbutton(root, text="Ends On Before", variable=checkbox_desription_before)
    window.create_window(125, 600, window=checkBox_desription_before_button) 


    checkbox_desription_after = tk.IntVar(root)
    checkBox_desription_after_button = tk.Checkbutton(root, text="Ends On After", variable=checkbox_desription_after)
    window.create_window(250, 600, window=checkBox_desription_after_button) 


    checkbox_minute_before = tk.IntVar(root)
    checkBox_minute_before_button = tk.Checkbutton(root, text="Minute Before", variable=checkbox_minute_before)
    window.create_window(120, 625, window=checkBox_minute_before_button) 


    checkbox_minute_after = tk.IntVar(root)
    checkBox_minute_after_button = tk.Checkbutton(root, text="Minute After", variable=checkbox_minute_after)
    window.create_window(245, 625, window=checkBox_minute_after_button) 


    checkbox_last_reccurance_before = tk.IntVar(root)
    checkBox_last_reccurance_before_button = tk.Checkbutton(root, text="last_reccurance Before", variable=checkbox_last_reccurance_before)
    window.create_window(114, 650, window=checkBox_last_reccurance_before_button) 


    checkbox_last_reccurance_after = tk.IntVar(root)
    checkBox_last_reccurance_after_button = tk.Checkbutton(root, text="last_reccurance After", variable=checkbox_last_reccurance_after)
    window.create_window(239, 650, window=checkBox_last_reccurance_after_button) 


    checkbox_exact_event_name =  tk.IntVar(root)
    checkbox_exact_event_name_button = tk.Checkbutton(root, text="last_reccurance After", variable=checkbox_exact_event_name)
    window.create_window(170, 675, window=checkbox_exact_event_name_button) 

    button_two = tk.Button(root, text='Filter Data', command=filterDataGate)
    button_two.config(fg="white")
    window.create_window(193, 700, window=button_two)

root=tk.Tk()

window = tk.Canvas(root, width=350, height=1000)
window.pack()

addToDatabaseLabels()
# filterDataLabels()

button_three = tk.Button(root, text='Print Database', command=printDatabase)
button_three.config(fg="white")
window.create_window(193, 725, window=button_three)

exitButton = tk.Button(root, text="Quit", command=root.quit)  # Close Button
window.create_window(200, 800, window=exitButton)

root.mainloop()
