import tkinter as tk
import PySimpleGUI as sg

root=tk.Tk()

window = tk.Canvas(root, width=350, height=1000)
window.pack()


# def addToDatabase(eventName: str, day: int, month: int, year: int, hour: int, minutes:int, recurring: str,endson:str, eventType: str) -> None:

event_name_text = tk.Label(root, text = "Event Name:")
window.create_window(57, 50, window=event_name_text)  

day_text = tk.Label(root, text = "Day:")
window.create_window(82 , 75, window=day_text)  

month_text = tk.Label(root, text = "Month:")
window.create_window(74, 100, window=month_text)  

year_text = tk.Label(root, text = "Year:")
window.create_window(80, 125, window=year_text)  

hour_text = tk.Label(root, text = "Hour:")
window.create_window(80, 150, window=hour_text)  

minutes_text = tk.Label(root, text = "Minutes:")
window.create_window(71, 175, window=minutes_text)  

recurring_text = tk.Label(root, text = "Recurring:")
window.create_window(65, 200, window=recurring_text) 

endson_text = tk.Label(root, text = "Ends On:")
window.create_window(70, 225, window=endson_text)  

event_type_text = tk.Label(root, text = "Event Type:")
window.create_window(61, 250, window=event_type_text)  

event_name_input = tk.Entry(root) 
window.create_window(200, 50, window=event_name_input)

day_input = tk.Entry(root) 
window.create_window(200, 75, window=day_input)

month_input = tk.Entry(root) 
window.create_window(200, 100, window=month_input)


year_input = tk.Entry(root) 
window.create_window(200, 125, window=year_input)


hour_input = tk.Entry(root) 
window.create_window(200, 150, window=hour_input)

minutes_input = tk.Entry(root) 
window.create_window(200, 175, window=minutes_input)

recurring_input = tk.Entry(root) 
window.create_window(200, 200, window=recurring_input)


endson_input = tk.Entry(root) 
window.create_window(200, 225, window=endson_input)

event_type_input = tk.Entry(root) 
window.create_window(200, 250, window=event_type_input)

button_one = tk.Button(root, text='Add to Database', command=None)
button_one.config(fg="white")
window.create_window(193, 300, window=button_one)


event_name_2_text = tk.Label(root, text = "Event Name:")
window.create_window(57, 350, window=event_name_2_text)

event_name_2_input = tk.Entry(root)
window.create_window(200,350, window=event_name_2_input) 

day_2_text = tk.Label(root, text = "Day:")
window.create_window(82, 375, window=day_2_text)

day_2_input = tk.Entry(root)
window.create_window(200,375, window=day_2_input) 

month_2_text = tk.Label(root, text = "Month:")
window.create_window(74, 400, window=month_2_text)

month_2_input = tk.Entry(root)
window.create_window(200,400, window=month_2_input) 

year_2_text = tk.Label(root, text = "Year:")
window.create_window(80, 425, window=year_2_text)

year_2_input = tk.Entry(root)
window.create_window(200,425, window=year_2_input) 

hour_2_text = tk.Label(root, text = "Hour:")
window.create_window(80, 450, window=hour_2_text)

hour_2_input = tk.Entry(root)
window.create_window(200,450, window=hour_2_input) 

minutes_2_text = tk.Label(root, text = "Minutes:")
window.create_window(71, 475, window=minutes_2_text)

minutes_2_input = tk.Entry(root)
window.create_window(200,475, window=minutes_2_input) 

recurring_2_text = tk.Label(root, text = "Recurring:")
window.create_window(65, 500, window=recurring_2_text)

recurring_2_input = tk.Entry(root)
window.create_window(200,500, window=recurring_2_input) 

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


checkbox_endson_before = tk.IntVar(root)
checkBox_endson_before_button = tk.Checkbutton(root, text="Ends On Before", variable=checkbox_endson_before)
window.create_window(125, 600, window=checkBox_endson_before_button) 


checkbox_endson_after = tk.IntVar(root)
checkBox_endson_after_button = tk.Checkbutton(root, text="Ends On After", variable=checkbox_endson_after)
window.create_window(250, 600, window=checkBox_endson_after_button) 


checkbox_minute_before = tk.IntVar(root)
checkBox_minute_before_button = tk.Checkbutton(root, text="Minute Before", variable=checkbox_minute_before)
window.create_window(120, 625, window=checkBox_minute_before_button) 


checkbox_minute_after = tk.IntVar(root)
checkBox_minute_after_button = tk.Checkbutton(root, text="Minute After", variable=checkbox_minute_after)
window.create_window(245, 625, window=checkBox_minute_after_button) 


checkbox_hour_before = tk.IntVar(root)
checkBox_hour_before_button = tk.Checkbutton(root, text="Hour Before", variable=checkbox_hour_before)
window.create_window(114, 650, window=checkBox_hour_before_button) 


checkbox_hour_after = tk.IntVar(root)
checkBox_hour_after_button = tk.Checkbutton(root, text="Hour After", variable=checkbox_hour_after)
window.create_window(239, 650, window=checkBox_hour_after_button) 

exitButton = tk.Button(root, text="Quit", command=root.quit)  # Close Button
window.create_window(200, 750, window=exitButton)

root.mainloop()