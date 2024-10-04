import tkinter as tk
from PIL import Image, ImageTk 
from tkinter import ttk
from tkcalendar import DateEntry
import json
import sys
import os
from tkinter import  messagebox


class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1230x600")
        self.alltask = {}
        self.root.title("To Do List")

        # Create the main frame
        frontFrame = tk.Frame(self.root, width=1100, height=500, bg="white")
        frontFrame.pack_propagate(False)  # Prevent the frame from resizing to fit its contents
        frontFrame.pack(padx=10, pady=10)

        # Configure the grid for the main frame
        frontFrame.grid_columnconfigure(0, weight=1)  # Left column (logo)
        frontFrame.grid_columnconfigure(1, weight=3)  # Middle section (title, search, result)
        frontFrame.grid_columnconfigure(2, weight=1)  # Right column (bell, history, add button)
        frontFrame.grid_rowconfigure(2, weight=1)     # Ensure the row for the button has space

        # Load and resize the logo image
        logo = Image.open("HCI project/logo.png")
        logo = logo.resize((190, 130), Image.LANCZOS)
        img = ImageTk.PhotoImage(logo)

        # Create and place the logo label (row 0, column 0)
        log = tk.Label(frontFrame, image=img, bg="white")
        log.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        log.image = img
        
        # Title label for the app (row 0, column 1)
        todotitle = tk.Label(frontFrame, text="To Do List Application", font=("Times", 35), bg="white",fg="#518D45")
        todotitle.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")

        # Frame for bell and history icons (row 0, column 2)
        bell_history_frame = tk.Frame(frontFrame, bg="white")
        bell_history_frame.grid(row=0, column=2, padx=10, pady=10, sticky="ne")

        # Load and resize the bell image
        bell = Image.open("HCI project/bell.png")
        bell = bell.resize((70, 60), Image.LANCZOS)
        bel = ImageTk.PhotoImage(bell)

        # Place the bell label
        be = tk.Label(bell_history_frame, image=bel, bg="white")
        be.pack(side="left", padx=5)
        be.image = bel

        # Load and resize the history image
        history_img = Image.open("HCI project/history.png")
        history_img = history_img.resize((70, 60), Image.LANCZOS)
        hist_img = ImageTk.PhotoImage(history_img)

        # Place the history label
        history_button = tk.Label(bell_history_frame, image=hist_img, bg="white")
        history_button.pack(side="left", padx=5)
        history_button.image = hist_img
        history_button.bind("<Button-1>", self.open_history_window)

        # Load and resize the search image
        search = Image.open("HCI project/search.png")
        search = search.resize((40, 40), Image.LANCZOS)
        searc = ImageTk.PhotoImage(search)

        # Create frame for search bar and icon (row 1, column 0 & 1)
        searchFrame = tk.Frame(frontFrame, bg="white")
        searchFrame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Place the search icon
        sear = tk.Label(searchFrame, image=searc, bg="white")
        sear.pack(side="left", padx=5)
        sear.image = searc

        # Create the search bar
        self.searchbar_placeholder = "Search Task"
        self.searchBar = tk.Entry(searchFrame, width=50, font=("Arial", 13))
        self.searchBar.insert(0, self.searchbar_placeholder)
        self.searchBar.bind('<FocusIn>', self.on_entry_clickSearch)
        self.searchBar.bind('<FocusOut>', self.on_focusoutSearch)
        self.searchBar.pack(side="left", padx=5, ipady=10)

        # Create result frame (row 2, column 0-3)
        self.resultFrame = tk.Frame(frontFrame, width=1000, height=300, bg="grey", borderwidth=2, relief="solid")
        self.resultFrame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.resultFrame.grid_propagate(False)

        # Scrollbar for the listbox
        scrollbar = tk.Scrollbar(self.resultFrame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.title = tk.Label(self.resultFrame, text="Tasks:", font=("Arial", 15))
        self.title.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create the Listbox widget
        self.listbox = tk.Listbox(self.resultFrame, yscrollcommand=scrollbar.set, width=1000, height=300, font=("Arial", 20))
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.display_selected_task)
        scrollbar.config(command=self.listbox.yview)

        # Load and resize the add image
        add = Image.open("HCI project/add.png")
        add = add.resize((60, 60), Image.LANCZOS)
        ad = ImageTk.PhotoImage(add)

        # Add Button (row 2, column 2)
        add_button = tk.Button(frontFrame, image=ad, bg="white", borderwidth=0, command=self.open_task_window)
        add_button.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")
        add_button.image = ad  # Save reference to prevent garbage collection
        self.add_listbox()
        
        
        

    def open_history_window(self, event):
        # Create a top-level window for the history
        history_window = tk.Toplevel(self.root)
        history_window.title("Task History")
        history_window.geometry("600x400")
        
        # Create a frame to hold the Listbox and Scrollbars
        frame = tk.Frame(history_window)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create a Listbox for the history
        self.history_listbox = tk.Listbox(frame, font=("Arial", 15), width=70)
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create vertical scrollbar
        vertical_scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=self.history_listbox.yview)
        vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Link the scrollbar to the Listbox
        self.history_listbox.config(yscrollcommand=vertical_scrollbar.set)

        # Create horizontal scrollbar
        horizontal_scrollbar = tk.Scrollbar(history_window, orient=tk.HORIZONTAL, command=self.history_listbox.xview)
        horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Link the horizontal scrollbar to the Listbox
        self.history_listbox.config(xscrollcommand=horizontal_scrollbar.set)

        # Create a Delete button
        delete_button = tk.Button(history_window, text="Delete Task", command=self.delete_task_from_history, font=("Arial", 12))
        delete_button.pack(pady=10)

        # Load history from JSON
        self.load_history()

    def load_history(self):
      if os.path.exists('HCI project/archives.json'):
        with open('HCI project/archives.json', 'r') as file:
            history = json.load(file)
            
            # Iterate over each category and task
            for category, tasks in history.items():
                # Insert the category as a header
                self.history_listbox.insert(tk.END, f"{category}:")
                self.history_listbox.itemconfig(tk.END, {'fg': 'blue'})  # Optional: Make category stand out

                for task_name, details in tasks.items():
                    # Format the task details with an 8-space indent
                    where = details.get("where", "N/A")
                    description = details.get("description", "N/A")
                    due_date = details.get("Due Date", "N/A")
                    
                    task_info = f"        {task_name} - Where: {where}, Description: {description}, Due Date: {due_date}"
                    self.history_listbox.insert(tk.END, task_info)

    def delete_task_from_history(self):
        selected_task_index = self.history_listbox.curselection()
        if selected_task_index:
            # Get the selected task name from the Listbox, stripping unnecessary details
            task_info = self.history_listbox.get(selected_task_index).strip()
            # Assume the task name is the first part of the string, before the ' - ' separator
            task_to_delete = task_info.split(' - ')[0]  # Extracting just the task name
            print(f"Attempting to delete task: '{task_to_delete}'")
            
            self.history_listbox.delete(selected_task_index)

            # Load existing archives from archives.json
            try:
                with open('HCI project/archives.json', 'r') as file:
                    archives = json.load(file)
            except FileNotFoundError:
                messagebox.showerror("Error", "Archives file not found.")
                return

            # Check if the task exists in archives
            archive_task_found = False
            for category, tasks in archives.items():
                print(f"Checking category: {category} with tasks: {tasks}")  # Debugging output
                # Use the key name to compare with the extracted task name
                if task_to_delete in tasks:
                    del tasks[task_to_delete]  # Delete the task from the archives category
                    archive_task_found = True
                    print(f"Deleted task '{task_to_delete}' from archives.")  # Debugging output
                    break

            if archive_task_found:
                # Save the updated archives back to archives.json
                with open('HCI project/archives.json', 'w') as file:
                    json.dump(archives, file, indent=4)
                messagebox.showinfo("Task Deleted", f"The task '{task_to_delete}' has been deleted from archives.")
            else:
                messagebox.showwarning("Error", "Task not found in archives.")
        else:
            messagebox.showwarning("Error", "No task selected for deletion.")



    
    def exit_program(self,event):
        self.root.destroy()
        sys.exit()  # Ensures the entire process terminates
        
    def search_on_enter(self, event):
        self.search()  # Call the search method
        
    


    def add_listbox(self):
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
            
        # Clear the Listbox
        self.listbox.delete(0, tk.END)
        
        # Check if 'Personal' category exists and loop through personal tasks
        if "Personal" in self.alltask:
                for task_key, task_info in self.alltask["Personal"].items():
                        # Display the subcategory (task_key) directly in the listbox
                        task_title = task_key
                        print(f"Adding Personal Task: {task_title}")  # Debug print
                        self.listbox.insert(tk.END, f"Personal: {task_title}")
        
        # Check if 'Academic' category exists and loop through academic tasks
        if "Academic" in self.alltask:
                for task_key, task_info in self.alltask["Academic"].items():
                        # Use the 'subject' field as the task title, fall back to default if not available
                        task_title = task_key
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
        
        # Check if the search term is for a specific category
        if self.value_search in ["personal", "academic"]:  # Checking for category terms
                category = self.value_search.capitalize()  # Capitalize to match JSON keys
                tasks = self.alltask.get(category, {})  # Get tasks from the specified category
                
                # Insert all task keys from the selected category into the listbox
                for task_key in tasks.keys():
                    self.listbox.insert(tk.END, task_key)  # Insert task key into the listbox
        else:
                # Get the Personal tasks
                personal_tasks = self.alltask.get("Personal", {})  # Get the Personal tasks
                
                # Iterate through all personal tasks and search for keys that match
                for task_key in personal_tasks.keys():
                    if self.value_search in task_key.lower():  # Check if the search value is in the task key
                        self.listbox.insert(tk.END, task_key)  # Insert matching task key into the listbox
                
                # Get the Academic tasks
                academic_tasks = self.alltask.get("Academic", {})  # Get the Academic tasks
                
                # Iterate through all academic tasks and search for keys that match
                for task_key in academic_tasks.keys():
                    if self.value_search in task_key.lower():  # Check if the search value is in the task key
                        self.listbox.insert(tk.END, task_key)  # Insert matching task key into the listbox

                
    def open_task_window(self):
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
        sub = self.task_combo.get()
        category = self.category_combo.get()

        # File name for storing tasks
        filename = 'HCI project/task.json'
        
        # Load existing tasks or initialize an empty dictionary
        if os.path.exists(filename):
                with open(filename, 'r') as json_file:
                        all_tasks = json.load(json_file)
        else:
                all_tasks = {"Personal": {}, "Academic": {}}  # Ensure these keys match consistently

        # Count existing tasks with the same prefix in the selected category
        chosen = all_tasks.get(category, {})
        number = sum(1 for key in chosen.keys() if key.startswith(sub))

        # Create a unique subname for the new task
        subname = f"{sub}{number}" if number > 0 else sub

        # Determine the correct category and handle both personal and academic tasks
        if category == "Personal":
                # Get personal task entry data
                where = self.where.get().strip()  # Get the entry from 'where' (use subcategory as task key)
                description = self.description_entry.get("1.0", tk.END).strip()
                due_date = self.full_time  # Assume full_time is set when selecting the date

                # Create task info for personal task
                task_info = {
                        "where": where,
                        "description": description,
                        "Due Date": due_date,
                }

                # Add the new personal task to the all_tasks dictionary
                all_tasks["Personal"][subname] = task_info

        elif category == "Academic":
                # Get academic task entry data
                subject = self.subject_entry.get().strip()  # Use subject as the task key
                description = self.description_entry.get("1.0", tk.END).strip()
                due_date = self.full_time  # Assume full_time is set when selecting the date

                # Create task info for academic task
                task_info = {
                        "subject": subject,
                        "description": description,
                        "Due Date": due_date,
                }

                # Add the new academic task to the all_tasks dictionary
                all_tasks["Academic"][subname] = task_info

        # Save the updated all_tasks dictionary to the JSON file
        with open(filename, 'w') as json_file:
                json.dump(all_tasks, json_file, indent=4)

        # Print confirmation of the submitted task
        print(f"Task Submitted: {task_info} in {category} category under key: {subname}")
        self.subcategory_window.destroy()
        self.task_chooser.destroy()
        self.add_listbox()

        
    def display_selected_task(self, event):
        # Ensure something is selected
        if not self.listbox.curselection():
            return  # Exit if nothing is selected

        # Create a new Toplevel window to show task details
        details_window = tk.Toplevel()
        details_window.geometry("800x600")  # Ensure the window is large enough

        # Title label directly in the details_window
        title_label = tk.Label(details_window, text="Task Details", font=("Times", 30, "bold"), pady=20, fg="#518D45")
        title_label.pack()

        # Get the selected index from the listbox
        selected_index = self.listbox.curselection()[0]  # Get the index of the selected task

        # Retrieve the task key
        selected_task_text = self.listbox.get(selected_index)

        # Check whether the selected task belongs to the personal or academic category
        if selected_task_text.startswith("Personal:"):
            category = "Personal"
            task_title = selected_task_text.replace("Personal: ", "")  # Extract task title
        elif selected_task_text.startswith("Academic:"):
            category = "Academic"
            task_title = selected_task_text.replace("Academic: ", "")  # Extract task title
        else:
            return  # Do nothing if no valid task is selected

        # Display Category Label
        category_label = tk.Label(details_window, text=f"Category: {category}", font=("Arial", 20), pady=10, fg="#518D45")
        category_label.pack()

        # Display Subcategory Label (Task Title)
        task_label = tk.Label(details_window, text=f"Task: {task_title}", font=("Arial", 20), pady=10, fg="#518D45")
        task_label.pack()

        # Find the task details using the task title
        task_info = None
        if category in self.alltask and task_title in self.alltask[category]:
            task_info = self.alltask[category][task_title]

        if not task_info:
            return  # Exit if task not found

        # Display task details as labels
        for key, value in task_info.items():
            if key == "description":
                description_text = tk.Text(details_window, font=("Arial", 18), fg="#518D45", height=5, width=50)
                description_text.insert(tk.END, value)  # Insert the description into the Text widget
                description_text.pack(pady=10)
                description_text.config(state=tk.DISABLED)  # Make it read-only
            else:
                tk.Label(details_window, text=f"{key.capitalize()}: {value}", font=("Arial", 18), fg="#518D45").pack(pady=10)

        # Create a Text widget to display the task context if it exists
        if "context" in task_info:
            context_text = tk.Text(details_window, font=("Arial", 18), fg="#518D45", height=10, width=80)
            context_text.pack(padx=10, pady=10)

            # Insert task context into the Text widget
            context_text.insert(tk.END, task_info["context"])
            context_text.config(state=tk.DISABLED)  # Make it read-only

        # Create the "Mark as Done" button
        mark_done_frame = tk.Frame(details_window)
        mark_done_frame.pack(pady=10, anchor="center")  # Pack the frame and center it

        # Mark as Done button
        mark_done_button = tk.Button(mark_done_frame, text="Mark as Done", font=("Arial", 16), command=lambda: self.archive_task(category, task_title),fg="#518D45")
        mark_done_button.pack(side="left", padx=10)  # Pack the button to the left with padding

        # Load and resize the delete image
        delete_image = Image.open("HCI project/delete.png")  # Update with the correct path
        delete_image = delete_image.resize((50, 50), Image.LANCZOS)
        delete_photo = ImageTk.PhotoImage(delete_image)

        # Create a label to display the delete image
        delete_label = tk.Label(mark_done_frame, image=delete_photo)
        delete_label.image = delete_photo  # Keep a reference to the image
        delete_label.pack(side="left", padx=10)  # Pack the label to the left with padding


        # Bind the delete image click to the delete_task method
        delete_label.bind("<Button-1>", lambda e: self.delete_task(category, task_title))

    def delete_task(self, category, task_title):
        # Load existing tasks from task.json
        with open('HCI project/task.json', 'r') as file:
            tasks = json.load(file)

        # Remove the task from the tasks dictionary
        if category in tasks and task_title in tasks[category]:
            task_info = tasks[category][task_title]  # Store task info before deletion
            del tasks[category][task_title]  # Delete the task

            # Write the updated tasks back to task.json
            with open('HCI project/task.json', 'w') as file:
                json.dump(tasks, file, indent=4)

            # Archive the deleted task to archives.json
            self.archive_task(category, task_title, task_info)

            # Update the listbox
            self.add_listbox()

    def archive_task(self, category, task_title, task_info):
        # Load existing archives from archives.json
        try:
            with open('HCI project/archives.json', 'r') as file:
                archives = json.load(file)
        except FileNotFoundError:
            archives = {}

        # Ensure the category exists in archives
        if category not in archives:
            archives[category] = {}
        archives[category][task_title] = task_info  # Add the task info to the archives

        # Write the updated archives back to archives.json
        with open('HCI project/archives.json', 'w') as file:
            json.dump(archives, file, indent=4)


  
       
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
