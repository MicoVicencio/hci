import tkinter as tk
from PIL import Image, ImageTk 
from tkinter import ttk
from tkcalendar import DateEntry
import json
class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1230x600")
        self.alltask = {}
        
        # Create the main frame
                # Create the main frame
        frontFrame = tk.Frame(self.root, width=1100, height=500, bg="white")
        frontFrame.pack_propagate(False)  # Prevent the frame from resizing to fit its contents
        frontFrame.pack(padx=10, pady=10)

        # Configure the grid to manage layout properly
        frontFrame.grid_columnconfigure(0, weight=1)  # Left side (logo column)
        frontFrame.grid_columnconfigure(1, weight=3)  # Middle section
        frontFrame.grid_columnconfigure(2, weight=1)  # Right side (bell/exit)
        frontFrame.grid_columnconfigure(3, weight=1)  # For Add button
        frontFrame.grid_rowconfigure(2, weight=1)  # Result frame row

        # Load and resize the logo image
        logo = Image.open("HCI project/logo.png")
        logo = logo.resize((190, 130), Image.LANCZOS)
        img = ImageTk.PhotoImage(logo)

        # Create and place the logo label in the grid (Left side, row 0)
        log = tk.Label(frontFrame, image=img, bg="white")
        log.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        log.image = img

        # Create a frame for bell and exit icons (Right side, row 0)
        bell_exit_frame = tk.Frame(frontFrame, bg="white")
        bell_exit_frame.grid(row=0, column=2, padx=10, pady=10, sticky="ne")

        # Load and resize the bell image
        bell = Image.open("HCI project/bell.png")
        bell = bell.resize((70, 60), Image.LANCZOS)
        bel = ImageTk.PhotoImage(bell)

        # Create and place the bell label in the bell_exit_frame
        be = tk.Label(bell_exit_frame, image=bel, bg="white")
        be.pack(side="left", padx=5)
        be.image = bel

        # Load and resize the exit image
        exit = Image.open("HCI project/exit.png")
        exit = exit.resize((70, 60), Image.LANCZOS)
        exi = ImageTk.PhotoImage(exit)

        # Create and place the exit label in the bell_exit_frame
        ex = tk.Label(bell_exit_frame, image=exi, bg="white")
        ex.pack(side="left", padx=5)
        ex.image = exi

        # Load and resize the search image
        search = Image.open("HCI project/search.png")
        search = search.resize((40, 40), Image.LANCZOS)  # Reduced size for better alignment
        searc = ImageTk.PhotoImage(search)

        # Create a small frame to hold both search logo and search bar for closer alignment
        searchFrame = tk.Frame(frontFrame, bg="white")
        searchFrame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Place the search icon in the searchFrame
        sear = tk.Label(searchFrame, image=searc, bg="white")
        sear.pack(side="left", padx=5)  # Small padding to keep it close to the search bar
        sear.image = searc

        # Create and place the search bar in the searchFrame
        self.searchbar_placeholder = "Search Task"
        self.searchBar = tk.Entry(searchFrame, width=50, font=("Arial", 13))
        self.searchBar.insert(0, self.searchbar_placeholder)
        self.searchBar.bind('<FocusIn>', self.on_entry_clickSearch)
        self.searchBar.bind('<FocusOut>', self.on_focusoutSearch)
        self.searchBar.pack(side="left", padx=5, ipady=10)  # Keep the entry close to the icon

        # Create result frame for displaying results
        self.resultFrame = tk.Frame(frontFrame, width=1000, height=300, bg="grey", borderwidth=2, relief="solid")
        self.resultFrame.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        self.resultFrame.grid_propagate(False)

        # Create a scrollbar for the listbox
        scrollbar = tk.Scrollbar(self.resultFrame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create the Listbox widget inside the resultFrame
        self.listbox = tk.Listbox(self.resultFrame, yscrollcommand=scrollbar.set, width=1000, height=300,font=("Arial",15))
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.listbox.bind("<<ListboxSelect>>",self.display_selected_task)

        # Configure the scrollbar to work with the Listbox
        scrollbar.config(command=self.listbox.yview)
        

        # Load and resize the add image
        add = Image.open("HCI project/add.png")
        add = add.resize((70, 60), Image.LANCZOS)
        ad = ImageTk.PhotoImage(add)

        # Create and place the add label in the grid
        a = tk.Label(frontFrame, image=ad, bg="white")
        a.grid(row=3, column=4, padx=10, pady=10)
        a.image = ad

        a.bind("<Button-1>", self.add_List)
        self.load_tasks_from_file()
        
    def load_tasks_from_file(self):
        try:
            # Open the JSON file and load the data
            with open('HCI project/task.json', 'r') as json_file:
                self.alltask = json.load(json_file)  # Load data into self.alltask
                print("Tasks loaded successfully:", self.alltask)
        except FileNotFoundError:
            print("The file 'task.json' was not found.")
        except json.JSONDecodeError:
            print("Error decoding JSON from the file.")
        except Exception as e:
            print("An error occurred:", str(e))
            
        self.add_listbox()


    def add_listbox(self):
       # Clear the Listbox
        self.listbox.delete(0, tk.END)
        
        # Loop through the alltask dictionary and add titles to the Listbox
        for task_key, task_info in self.alltask.items():
            self.listbox.insert(tk.END, task_info["title"])
            
            
    def on_entry_clickSearch(self, event):
        if self.searchBar.get() == self.searchbar_placeholder:
            self.searchBar.delete(0, "end")
    
    def on_focusoutSearch(self, event):
        if not self.searchBar.get():
            self.searchBar.insert(0, self.searchbar_placeholder)
            
    def add_List(self,event):
        self.createList = tk.Toplevel()
        self.createList.geometry("700x800")
        self.createList.config(bg="#518D45")
        title = tk.Label(self.createList,text="Adding New Task",font=("Arial",20),bg="#518D45",fg="white")
        title.pack(padx=20,pady=20)
        
        self.tit = "Title:"
        self.due = "Due Date:"
        
        self.title_entry = tk.Entry(self.createList,width=30,font=("Arial",15),fg="#518D45")
        self.title_entry.pack(padx=20,pady=20,ipady=10)
        self.title_entry.insert(0, self.tit)
        
        self.duedate = tk.Button(self.createList,width=30,text="Due Date",command=self.showCalendar,font=("Arial",14),fg="#518D45")
        self.duedate.pack(padx=20,pady=20)
        
        self.title_entry.bind('<FocusIn>', self.on_entry_clickTitle)
        self.title_entry.bind('<FocusOut>', self.on_focusoutTitle)
        
        
        self.duedate = tk.Button(self.createList,width=40,height=10,text="Due Date",command=self.showCalendar)
        
        self.options  = ["Academic", "Personal", "Goals", "Home"]
        self.category = ttk.Combobox(self.createList,values=self.options,font=("Arial",15),foreground="#518D45")
        self.category.set("Select Category")
        self.category.pack(padx=20,pady=20)
        
        self.description = tk.Text(self.createList,width=55,height=15,font=("Arial",15),fg="#518D45")
        self.description.pack(padx=20,pady=20)
        
        save = tk.Button(self.createList,text="Save",font=("Arial",15),fg="#518D45",command=self.getDetails)
        save.pack(padx=20,pady=20)
        
    def getDetails(self):
        title = self.title_entry.get()
        due_date = self.full_time
        cat_value = self.category.get()
        task_txt = self.description.get("1.0", tk.END)
        self.current_size_of_dicttask = len(self.alltask)
        
        # Create a task_info dictionary
        task_info = {
                "title": title,
                "due_date": due_date,
                "category": cat_value,
                "context": task_txt
        }

        # Create a unique task key for the new task
        task = "task" + str(self.current_size_of_dicttask + 1)

        # Add the new task to the alltask dictionary
        self.alltask[task] = task_info

        # Print the current alltask dictionary to the console
        print(self.alltask)

        # Save the entire alltask dictionary to a JSON file
        filename = 'HCI project/task.json'
        with open(filename, 'w') as json_file:
                json.dump(self.alltask, json_file, indent=4)  # Save the entire dictionary

        # Load the data back from the JSON file and print it
        with open(filename, 'r') as json_file:
                load = json.load(json_file)
        print(load)    

        # Update the Listbox and close the Toplevel window
        self.add_listbox()
        self.createList.destroy()

        
    def display_selected_task(self, event):
        # Create a new Toplevel window to show task details
        details_window = tk.Toplevel()
        details_window.geometry("700x400")
        details_window.config(bg="#518D45")

        # Title label
        title_label = tk.Label(details_window, text="Task Details", font=("Arial", 20), bg="#518D45", fg="white")
        title_label.pack(pady=20)

        selected_index = self.listbox.curselection()
        index = selected_index[0]
        task = "task" + str(index + 1)

        # Display other task information as labels
        for key, value in self.alltask[task].items():
            if key != "context":  # Exclude the context from being displayed as a label
                tk.Label(details_window, text=f"{key.capitalize()}: {value}", font=("Arial", 15), bg="#518D45", fg="white").pack(pady=5)

        # Create a Text widget to display the task context
        task_info_text = tk.Text(details_window, wrap="word", font=("Arial", 15), bg="#ffffff", fg="#518D45", height=10)
        task_info_text.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Insert task context into the Text widget
        task_info_text.insert(tk.END, self.alltask[task]["context"])

  
       
    def showCalendar(self):
        self.calendar = tk.Toplevel()
        # DateEntry for date selection
        self.date_label = tk.Label(self.calendar, text="Due Date:")
        self.date_label.grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = DateEntry(self.calendar, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        # Comboboxes for hours and minutes
        self.hour_label = tk.Label(self.calendar, text="Hour:")
        self.hour_label.grid(row=1, column=0, padx=5, pady=5)
        self.hour_combobox = ttk.Combobox(self.calendar, values=list(range(1, 13)), width=5)  # 1 to 12
        self.hour_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.hour_combobox.current(0)  # Set default to 1

        self.minute_label = tk.Label(self.calendar, text="Minute:")
        self.minute_label.grid(row=2, column=0, padx=5, pady=5)
        self.minute_combobox = ttk.Combobox(self.calendar, values=list(range(60)), width=5)  # 0 to 59
        self.minute_combobox.grid(row=2, column=1, padx=5, pady=5)
        self.minute_combobox.current(0)  # Set default to a

        # Combobox for AM/PM selection
        self.ampm_label = tk.Label(self.calendar, text="AM/PM:")
        self.ampm_label.grid(row=3, column=0, padx=5, pady=5)
        self.ampm_combobox = ttk.Combobox(self.calendar, values=["AM", "PM"], width=5)
        self.ampm_combobox.grid(row=3, column=1, padx=5, pady=5)
        self.ampm_combobox.current(0)  # Set default to AM

        # Button to show selected date and time
        self.show_button = tk.Button(self.calendar, text="Submit Time",command=self.show_date_time)
        self.show_button.grid(row=4, column=0, columnspan=2, pady=5)
        
    def show_date_time(self):
        date = self.date_entry.get()
        hour = self.hour_combobox.get()
        minute = self.minute_combobox.get()
        ampm = self.ampm_combobox.get()
        if len(minute) == 1:
            minute = "0" + minute
        self.full_time = f"{date} {hour}:{minute} {ampm}"
        self.calendar.destroy()
        print(self.full_time)
        self.duedate.config(text=self.full_time)
        
        
    
        
        
    def get_category(self):
        self.selected_category = self.category.get()
        print(self.selected_category)
        
    def on_entry_clickTitle(self,event):
        if self.title_entry.get() == self.tit:
            self.title_entry.delete(0, "end")  # delete all the text in the entry
            self.title_entry.config(fg="#518D45")

    def on_focusoutTitle(self,event):
        if self.title_entry.get() == '':
            self.title_entry.insert(0, self.tit)
            self.title_entry.config(fg='#518D45')
    def on_entry_clickDue(self,event):
        if self.duedate_entry.get() == self.due:
            self.duedate_entry.delete(0, "end")  # delete all the text in the entry
            self.duedate_entry.config(fg="#518D45")

    def on_focusoutDue(self,event):
        if self.duedate_entry.get() == '':
            self.duedate_entry.insert(0, self.due)
            self.duedate_entry.config(fg='#518D45')
        
        
        
        
        
        
        
        
        

root = tk.Tk()
app = App(root)
root.mainloop()
