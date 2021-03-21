data =  {"Event Name" : 57, 
         "Day" : 82,
         "Month" : 74,
         "Year" :80, 
         "Hour": 80, 
         "Minutes": 71, 
         "Recurring": 65,
         "Ends On": 70, 
         "Event Type": 61, 
        }


current = 350
for x, y in data.items():
    # print()
    variableName = ""
    for c in x:
        if c == " ":
            c = "_"
        variableName += c.lower()
    variableName += "_2_"

    # print(f'{variableName}text = tk.Label(root, text = "{x}:")')
    # print(f'window.create_window({y}, {current}, window={variableName}text)')

    # print()
    # print(f'{variableName}input = tk.Entry(root)')
    # print(f'window.create_window(200,{current}, window={variableName}input) ')
    
    current += 25
    # print()

current = 0

checkNames = {"", "Hour", "EndsOn", "Minute"}
for m in checkNames:
    print(f"checkbox_{m.lower()}_before = tk.IntVar(root)")
    print(f'checkBox_{m.lower()}_before_button = tk.Checkbutton(root, text="{m} Before", variable=checkbox_{m.lower()}_before)')
    print(f'window.create_window(100, {575+current}, window=checkBox_{m.lower()}_before_button) ')

    print()

    print()

    print(f"checkbox_{m.lower()}_after = tk.IntVar(root)")
    print(f'checkBox_{m.lower()}_after_button = tk.Checkbutton(root, text="{m} After", variable=checkbox_{m.lower()}_after)')
    print(f'window.create_window(225, {575+current}, window=checkBox_{m.lower()}_after_button) ')


    print()
    print()
    # print(f"checkbox_{m}_after = tk.IntVar(root)")

    # checked_exact = tk.IntVar(root)
    # checkBox_definition = tk.Checkbutton(root, text="Exact Match", variable=checked_exact)
    # window.create_window(375, 575, window=checkBox_definition)  

    current += 25