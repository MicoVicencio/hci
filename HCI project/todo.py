import tkinter as tk
from PIL import Image, ImageTk 
from tkinter import ttk
from tkcalendar import DateEntry
import json
import sys
import os


class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1230x600")
        self.alltask = {}
        self.root.title("To do List")
        
        # Create the main frame
        frontFrame = tk.Frame(self.root, width=1100, height=500, bg="white")
        frontFrame.pack_propagate(False)  # Prevent the frame from resizing to fit its contents
        frontFrame.pack(padx=10, pady=10)

        # Configure the grid to manage layout properly
        frontFrame.grid_columnconfigure(0, weight=1)  # Left side (logo column)
        frontFrame.grid_columnconfigure(1, weight=3)  # Middle section
        frontFrame.grid_columnconfigure(2, weight=1)  # For Add button
        frontFrame.grid_columnconfigure(3, weight=1)  # Right side (bell/exit)
        frontFrame.grid_rowconfigure(2, weight=1)  # Result frame row

        # Load and resize the logo image
        logo = Image.open("HCI project/logo.png")
        logo = logo.resize((190, 130), Image.LANCZOS)
        img = ImageTk.PhotoImage(logo)

        # Create and place the logo label in the grid (Left side, row 0)
        log = tk.Label(frontFrame, image=img, bg="white")
        log.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        log.image = img
        
        todotitle = tk.Label(frontFrame,text="To Do List Application",font=("Arial",25),bg="white")
        todotitle.grid(row=0,column=1,padx=10,pady=10,sticky="nswe")

        # Create a frame for bell and exit icons (Right side, row 0)
        bell_exit_frame = tk.Frame(frontFrame, bg="white")
        bell_exit_frame.grid(row=0, column=3, padx=10, pady=10, sticky="ne")  # Changed to column 3

        # Load and resize the bell image
        bell = Image.open("HCI project/bell.png")
        bell = bell.resize((70, 60), Image.LANCZOS)
        bel = ImageTk.PhotoImage(bell)

        # Create and place the bell label in the bell_exit_frame
        be = tk.Label(bell_exit_frame, image=bel, bg="white")
        be.pack(side="left", padx=5)
        be.image = bel

        # Load and resize the exit image
        exit_img = Image.open("HCI project/exit.png")  # Changed variable name to avoid conflict
        exit_img = exit_img.resize((70, 60), Image.LANCZOS)
        exi = ImageTk.PhotoImage(exit_img)

        # Create and place the exit label in the bell_exit_frame
        ex = tk.Label(bell_exit_frame, image=exi, bg="white")
        ex.pack(side="left", padx=5)
        ex.image = exi
        ex.bind("<Button-1>", self.exit_program)

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
        self.title = tk.Label(self.resultFrame, text="Tasks:", font=("Arial", 15))
        self.title.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.searchBar.bind("<Return>", self.search_on_enter)

        # Create the Listbox widget inside the resultFrame
        self.listbox = tk.Listbox(self.resultFrame, yscrollcommand=scrollbar.set, width=1000, height=300, font=("Arial", 15))
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.listbox.bind("<<ListboxSelect>>", self.display_selected_task)

        # Configure the scrollbar to work with the Listbox
        scrollbar.config(command=self.listbox.yview)

        # Load and resize the add image
        add = Image.open("HCI project/add.png")
        add = add.resize((70, 60), Image.LANCZOS)
        ad = ImageTk.PhotoImage(add)

        # Create and place the add label in the grid
        a = tk.Label(frontFrame, image=ad, bg="white")
        a.grid(row=3, column=3, padx=10, pady=10)  # Adjusted to column 2
        a.image = ad

        a.bind("<Button-1>", self.open_task_window)
        self.load_tasks_from_file()
    
    def exit_program(self,event):
        self.root.destroy()
        sys.exit()  # Ensures the entire process terminates
        
    def search_on_enter(self, event):
        self.search()  # Call the search method
        
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
        
        # Check if 'personal' category exists and loop through personal tasks
        if "personal" in self.alltask:
            for task_key, task_info in self.alltask["personal"].items():
                # Use the 'where' field as the title for personal tasks
                task_title = task_info.get("where", "Untitled Personal Task")
                print(f"Adding Personal Task: {task_title}")  # Debug print
                self.listbox.insert(tk.END, f"Personal: {task_title}")
        
        # Check if 'academic' category exists and loop through academic tasks
        if "academic" in self.alltask:
            for task_key, task_info in self.alltask["academic"].items():
                # Use the 'subject' field as the title for academic tasks
                task_title = task_info.get("subject", "Untitled Academic Task")
                print(f"Adding Academic Task: {task_title}")  # Debug print
                self.listbox.insert(tk.END, f"Academic: {task_title}")

        # Print a message if no tasks are found
        if not self.listbox.size():
            print("No tasks found to display.")


            
    def search(self):
        # Get the value from the search bar
        self.value_search = self.searchBar.get().lower()  # Convert input to lowercase for case-insensitive search
    
    # Clear the Listbox before adding new results
        self.listbox.delete(0, tk.END)
    
    # Iterate through all tasks and search for titles that match
        for task_key, task_info in self.alltask.items():
            title = task_info.get("title", "").lower()  # Convert title to lowercase
            if self.value_search in title:
                self.listbox.insert(tk.END, task_info["title"]) 
                
    def open_task_window(self,event):
        # Create a new Toplevel window
        self.task_chooser =  tk.Toplevel()
        self.task_chooser.title("Task Manager")
        self.task_chooser.geometry("400x300")

        # Create a label to prompt the user to choose a task category
        self.label = tk.Label(self.task_chooser, text="Choose Task", font=("Arial", 20,"bold"))
        self.label.pack(pady=10)
        
        self.Clabel = tk.Label(self.task_chooser, text="Categories", font=("Arial", 14))
        self.Clabel.pack(pady=10)

        # Create a Combobox for task categories
        self.category_combo = ttk.Combobox(self.task_chooser, values=["Academic", "Personal"], font=("Arial", 12))
        self.category_combo.pack(pady=10)
        self.category_combo.bind("<<ComboboxSelected>>", self.on_category_selected)
        
        self.Slabel = tk.Label(self.task_chooser, text="Sub Categories", font=("Arial", 14))
        self.Slabel.pack(pady=10)

        # Create a Combobox for tasks (Initially empty, will populate based on category selection)
        self.task_combo = ttk.Combobox(self.task_chooser, font=("Arial", 12))
        self.task_combo.pack(pady=10)

        # Add buttons for actions
        self.add_task_button = tk.Button(self.task_chooser, text="Next", font=("Arial", 12), command=self.identifier_task)
        self.add_task_button.pack(pady=10)
    
    def identifier_task(self):
        category = self.category_combo.get()
        if category == "Academic":
            self.open_academic_task_window()
        elif category == "Personal":
            self.open_personal_task_window()
        

        
        
    def on_category_selected(self, event):
        # Get the selected category
        category = self.category_combo.get()

        # Define academic and personal tasks
        academic_tasks = ["Submit Assignment", "Prepare for Exam", "Attend Class", "Group Project Meeting"]
        personal_tasks = ["Grocery Shopping", "Pay Bills", "Clean", "Cook"]

        # Populate the task combo based on selected category
        if category == "Academic":
            self.task_combo['values'] = academic_tasks
        elif category == "Personal":
            self.task_combo['values'] = personal_tasks

        # Set the first task as default in the task combo box
        self.task_combo.current(0)
    
    
    
    def open_academic_task_window(self):
        self.subcategory_window = tk.Toplevel(self.root)
        self.subcategory_window.title("Task Subcategory")

        # Set a larger size for the window
        self.subcategory_window.geometry("400x300")

        # Subject Entry
        self.subject_label = tk.Label(self.subcategory_window, text="Subject:", font=('Arial', 12))
        self.subject_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')  # Align to the west
        self.subject_entry = tk.Entry(self.subcategory_window, font=('Arial', 12), width=30)
        self.subject_entry.grid(row=0, column=1, padx=10, pady=10)

        # Description Entry
        self.description_label = tk.Label(self.subcategory_window, text="Description:", font=('Arial', 12))
        self.description_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.description_entry = tk.Text(self.subcategory_window, height=5, width=30, font=('Arial', 12))
        self.description_entry.grid(row=1, column=1, padx=10, pady=10)

        # Due Date Label
        self.due_date_label = tk.Label(self.subcategory_window, text="Due Date:", font=('Arial', 12))
        self.due_date_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        # Due Date Button
        self.due_date_button = tk.Button(self.subcategory_window, text="Select Due Date", command=self.showCalendar, font=('Arial', 12), width=20)
        self.due_date_button.grid(row=2, column=1, padx=10, pady=10)

        # Submit Button
        self.submit_button = tk.Button(self.subcategory_window, text="Submit", command=self.submit_task, font=('Arial', 12), width=20)
        self.submit_button.grid(row=3, column=1, padx=10, pady=20, sticky='ew')  # Align with Due Date Button

        # Make the layout more spacious
        for i in range(4):
            self.subcategory_window.grid_rowconfigure(i, weight=1)
        for j in range(2):
            self.subcategory_window.grid_columnconfigure(j, weight=1)
    
    def open_personal_task_window(self):
        self.subcategory_window = tk.Toplevel(self.root)
        self.subcategory_window.title("Personal Task")

        # Set a larger size for the window
        self.subcategory_window.geometry("400x300")

        # Personal Task Selection (using a Combobox)
        self.task_label = tk.Label(self.subcategory_window, text="Where:", font=('Arial', 12))
        self.task_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.where = tk.Entry(self.subcategory_window, font=('Arial', 12), width=30)
        self.where.grid(row=0, column=1, padx=10, pady=10)

        # Description Entry
        self.description_label = tk.Label(self.subcategory_window, text="Description:", font=('Arial', 12))
        self.description_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.description_entry = tk.Text(self.subcategory_window, height=5, width=30, font=('Arial', 12))
        self.description_entry.grid(row=1, column=1, padx=10, pady=10)

        # Due Date Label
        self.due_date_label = tk.Label(self.subcategory_window, text="Due Date:", font=('Arial', 12))
        self.due_date_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        # Due Date Button
        self.due_date_button = tk.Button(self.subcategory_window, text="Select Due Date", command=self.showCalendar, font=('Arial', 12), width=20)
        self.due_date_button.grid(row=2, column=1, padx=10, pady=10)

        # Submit Button
        self.submit_button = tk.Button(self.subcategory_window, text="Submit", command=self.submit_task, font=('Arial', 12), width=20)
        self.submit_button.grid(row=3, column=1, padx=10, pady=20, sticky='ew')  # Align with Due Date Button

        # Make the layout more spacious
        for i in range(4):
            self.subcategory_window.grid_rowconfigure(i, weight=1)
        for j in range(2):
            self.subcategory_window.grid_columnconfigure(j, weight=1)
            

        
    def add_task(self):
        # Get the selected task from the task combo box
        selected_task = self.task_combo.get()
        if selected_task:
            print(f"Task '{selected_task}' added to the list!")
        else:
            print("No task selected!")
                
            
    def on_entry_clickSearch(self, event):
        if self.searchBar.get() == self.searchbar_placeholder:
            self.searchBar.delete(0, "end")
    
    def on_focusoutSearch(self, event):
        if not self.searchBar.get():
            self.searchBar.insert(0, self.searchbar_placeholder)
            
    
        
    def submit_task(self):
        # Load existing tasks or initialize an empty dictionary
        sub = self.task_combo.get()
        category = self.category_combo.get()
        filename = 'HCI project/task.json'
        if os.path.exists(filename):
                with open(filename, 'r') as json_file:
                        all_tasks = json.load(json_file)
        else:
                all_tasks = {"Personal": {}, "Academic": {}}

        # Determine the correct category (assume self.category holds either 'personal' or 'academic')
        
        if category == "Personal":
                # Get personal task entry data
                where = self.where.get().strip()  # Get the entry from 'where' (use subcategory as task key)
                description = self.description_entry.get("1.0", tk.END).strip()
                due_date = self.full_time  # Assume full_time is set when selecting the date

                # Create task info for personal task
                task_info = {
                        "where": where,  # The 'where' field is now used as the task title
                        "description": description,
                        "due_date": due_date,
                }

                # Use the subcategory (where) as the task key, if it's not empty
                task_key = sub if sub else f"personal{len(all_tasks.get('personal', {}))}"

                # Add the new personal task to the all_tasks dictionary
                all_tasks["Personal"][task_key] = task_info
                
                

        elif category == "Academic":
                # Get academic task entry data
                subject = self.subject_entry.get().strip()  # Use subject as the task key
                description = self.description_entry.get("1.0", tk.END).strip()
                due_date = self.full_time  # Assume full_time is set when selecting the date

                # Create task info for academic task
                task_info = {
                        "subject": subject,  # The 'subject' field is now used as the task title
                        "description": description,
                        "due_date": due_date,
                }

                # Use the subject as the task key, if it's not empty
                task_key = sub if sub else f"academic{len(all_tasks.get('academic', {}))}"

                # Add the new academic task to the all_tasks dictionary
                all_tasks["academic"][task_key] = task_info

        # Save the updated all_tasks dictionary to the JSON file
        with open(filename, 'w') as json_file:
                json.dump(all_tasks, json_file, indent=4)

        # Print confirmation of the submitted task
        print(f"Task Submitted: {task_info} in {category} category under key: {task_key}")

        # Clear the fields after submission

        


        
    def display_selected_task(self, event):
        # Ensure something is selected
        if not self.listbox.curselection():
            return  # Exit the function if nothing is selected

        # Create a new Toplevel window to show task details
        details_window = tk.Toplevel()
        details_window.geometry("700x400")
        details_window.config(bg="#518D45")

        # Title label
        title_label = tk.Label(details_window, text="Task Details", font=("Arial", 20), bg="#518D45", fg="white")
        title_label.pack(pady=20)

        # Get the selected index from the listbox
        selected_index = self.listbox.curselection()[0]  # Get the index of the selected task

        # Retrieve the task key (e.g., "Personal: Cook" or "Academic: Submit Assignment")
        selected_task_text = self.listbox.get(selected_index)

        # Check whether the selected task belongs to the personal or academic category
        if selected_task_text.startswith("Personal:"):
            category = "personal"
            task_title = selected_task_text.replace("Personal: ", "")  # Extract task title
        elif selected_task_text.startswith("Academic:"):
            category = "academic"
            task_title = selected_task_text.replace("Academic: ", "")  # Extract task title
        else:
            return  # Do nothing if no valid task is selected

        # Find the task details using the task title (where/subject)
        task_info = None
        for key, task in self.alltask[category].items():
            if (category == "personal" and task.get("where") == task_title) or (category == "academic" and task.get("subject") == task_title):
                task_info = task
                break
        
        if not task_info:
            return  # Exit if task not found
        
        # Display task details as labels
        for key, value in task_info.items():
            if key != "context":  # Exclude 'context' from being displayed as a label
                tk.Label(details_window, text=f"{key.capitalize()}: {value}", font=("Arial", 15), bg="#518D45", fg="white").pack(pady=5)

        # Create a Text widget to display the task context
        if "context" in task_info:
            task_info_text = tk.Text(details_window, wrap="word", font=("Arial", 15), bg="#ffffff", fg="#518D45", height=10)
            task_info_text.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

            # Insert task context into the Text widget
            task_info_text.insert(tk.END, task_info["context"])
            task_info_text.config(state=tk.DISABLED)  # Make it read-only


  
       
    def showCalendar(self):
        self.calendar = tk.Toplevel()
        
        # Date selection
        self.date_label = tk.Label(self.calendar, text="Due Date:", font=("Helvetica", 14))
        self.date_label.grid(row=0, column=0)  # Adjusted padding
        self.date_entry = DateEntry(self.calendar, width=16, background='darkblue', foreground='white', borderwidth=2, font=("Helvetica", 14))
        self.date_entry.grid(row=0, column=1)  # Adjusted padding
        
        # Button to show selected date and time
        self.show_button = tk.Button(self.calendar, text="Submit Time", command=self.show_date_time, font=("Helvetica", 14))
        self.show_button.grid(row=3, column=0, columnspan=2, pady=(10, 20))
        
        # Frame for time selection
        self.time_frame = tk.Frame(self.calendar)
        self.time_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Time Label
        self.time_label = tk.Label(self.time_frame, text="Select Time:", font=("Helvetica", 14))
        self.time_label.grid(row=0, column=0, columnspan=6)
        
        # Hour Spinbox (1 to 12)
        self.hour_label = tk.Label(self.time_frame, text="Hour:", font=("Helvetica", 14))
        self.hour_label.grid(row=1, column=0)
        self.hour_spinbox = tk.Spinbox(self.time_frame, from_=1, to=12, width=5, font=("Helvetica", 14))
        self.hour_spinbox.grid(row=1, column=1, padx=10)

        # Minute Spinbox (0 to 59)
        self.minute_label = tk.Label(self.time_frame, text="Minute:", font=("Helvetica", 14))
        self.minute_label.grid(row=1, column=2)
        self.minute_spinbox = tk.Spinbox(self.time_frame, from_=0, to=59, width=5, font=("Helvetica", 14))
        self.minute_spinbox.grid(row=1, column=3, padx=10)
        
        # AM/PM Combobox
        self.ampm_label = tk.Label(self.time_frame, text="AM/PM:", font=("Helvetica", 14))
        self.ampm_label.grid(row=1, column=4)
        self.ampm_combobox = ttk.Combobox(self.time_frame, values=["AM", "PM"], width=8, font=("Helvetica", 14))
        self.ampm_combobox.grid(row=1, column=5, padx=10)
        self.ampm_combobox.current(0)  # Default to AM
 

        
    def show_date_time(self):
        # Get the selected date and time
        date = self.date_entry.get()
        hour = self.hour_spinbox.get()  # Updated to use Spinbox
        minute = self.minute_spinbox.get()  # Updated to use Spinbox
        ampm = self.ampm_combobox.get()
        
        # Ensure the minute is two digits
        if len(minute) == 1:
            minute = "0" + minute
        
        # Format the full date and time string
        self.full_time = f"{date} {hour}:{minute} {ampm}"
        
        # Close the calendar window
        self.calendar.destroy()
        
        # Update the label with the due date
        self.due_date_button.config(text=self.full_time)
        print(self.full_time)

        
        
    
        
        
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
