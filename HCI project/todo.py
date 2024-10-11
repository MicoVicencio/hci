import tkinter as tk
from PIL import Image, ImageTk 
from tkinter import ttk
from tkcalendar import DateEntry
import json
import sys
import os
from tkinter import  messagebox
from datetime import datetime, timedelta
import time
import threading
from tkinter import Label,Frame,Button
import mysql.connector


class App:
    def __init__(self, root):
        self.root = root
        self.connect_to_database()
        
        self.alltask = {}
        self.json_folder = 'HCI project/json_files'
        if not os.path.exists(self.json_folder):
            os.makedirs(self.json_folder)
            
        self.data = {}

        # Call the main window setup
        
        self.root.title("Login")
        self.root.withdraw()
        # Placeholder texts
        self.placeholder_username = "Username"
        self.placeholder_password = "Password"

        # Hardcoded valid credentials for login


        # Load image
        imgPath = r"C:\Users\micov\OneDrive\Desktop\HCI project\face.png"
        img = Image.open(imgPath)
        new_size = (120, 100)  # Specify the new size (width, height)
        img_resized = img.resize(new_size, Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(img_resized)

        
        # Show login by default
        self.show_login()
        
        
        
    def connect_to_database(self):
        try:
            self.db_connection = mysql.connector.connect(
                host='localhost',         # Replace with your host
                user='root',     # Replace with your MySQL username
                password='micopogi',  # Replace with your MySQL password
                database='users'        # Database name
            )
            self.db_cursor = self.db_connection.cursor()
            print("Database connection successful!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Connection Error", f"Error: {err}")
            sys.exit(1)
        

    def show_login(self):

        # Clear the main frame
        self.login_window = tk.Toplevel()
        self.login_window.title("Login")
        self.main_frame = Frame(self.login_window, bg="#518d45", height=500, width=900)
        self.main_frame.pack_propagate(False)
        self.main_frame.pack(padx=50, pady=50)
        self.login_window.geometry("900x600")
        self.login_window.config(bg="white")
        self.main_frame.config(bg="#518d45")
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Create title label
        title_label = Label(self.main_frame, text="Login", bg="#518d45", fg="white", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)

        # Create image label
        label = Label(self.main_frame, image=self.photo, bg="#518d45")
        label.pack(padx=10, pady=10)

        # Username entry
        self.username = tk.Entry(self.main_frame, fg='#505050', font=("Arial", 12), width=40)
        self.username.insert(0, self.placeholder_username)
        self.username.bind('<FocusIn>', self.on_entry_click)
        self.username.bind('<FocusOut>', self.on_focusout)
        self.username.pack(padx=10, pady=10, ipady=9)

        # Password entry
        self.password = tk.Entry(self.main_frame, fg='#505050', font=("Arial", 12), show='*', width=40)
        self.password.insert(0, self.placeholder_password)
        self.password.bind('<FocusIn>', self.on_entry_clickP)
        self.password.bind('<FocusOut>', self.on_focusoutP)
        self.password.pack(padx=10, pady=10, ipady=9)

        # Login button
        login = Button(self.main_frame, text="Login", height=2, width=20, bg="#96cb4b", fg="white", font=("Arial", 13, "bold"), command=self.login)
        login.pack(padx=20, pady=10)

        # Create Account button
        create_account = Button(self.main_frame, text="Create Account", height=2, width=20, bg="#96cb4b", fg="white", font=("Arial", 13, "bold"), command=self.show_create_account)
        create_account.pack(padx=20, pady=10)
        
    def log(self):
        self.create_account_window.destroy()
        self.show_login()
            

    def login(self):
        self.entered_username = self.username.get()
        self.entered_password = self.password.get()

        try:
            self.db_cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (self.entered_username, self.entered_password))
            result = self.db_cursor.fetchone()
            if result:
                messagebox.showinfo("Login Successful", "Welcome to the To-Do List App!")
                self.Amainwindow()  # Call your main window method
            else:
                messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        

    def show_create_account(self):
        # Clear the main frame
        self.create_account_window = tk.Toplevel()
        self.create_account_window.title("Create Account")
        self.create_account_window.geometry("900x600")
        self.create_account_window.config(bg="#518d45")

        # Create main frame for the create account window
        self.main_frame = Frame(self.create_account_window, bg="white", height=500, width=900)
        self.main_frame.pack_propagate(False)
        self.main_frame.pack(padx=50, pady=50)

        # Clear any existing widgets in the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.main_frame.config(bg="white")
        self.create_account_window.config(bg="#518d45")

        # Create title label
        title_label = Label(self.main_frame, text="Create Account", bg="white", fg="#518d45", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)

        # Create image label
        label = Label(self.main_frame, image=self.photo, bg="white")
        label.pack(padx=10, pady=10)

        # Username entry
        self.new_username = tk.Entry(self.main_frame, fg='#505050', font=("Arial", 12), width=40)
        self.new_username.insert(0, self.placeholder_username)
        self.new_username.bind('<FocusIn>', self.on_entry_click)
        self.new_username.bind('<FocusOut>', self.on_focusout)
        self.new_username.pack(padx=10, pady=10, ipady=9)

        # Password entry
        self.new_password = tk.Entry(self.main_frame, fg='#505050', font=("Arial", 12), show='*', width=40)
        self.new_password.insert(0, self.placeholder_password)
        self.new_password.bind('<FocusIn>', self.on_entry_clickP)
        self.new_password.bind('<FocusOut>', self.on_focusoutP)
        self.new_password.pack(padx=10, pady=10, ipady=9)

        # Create Account button
        create = Button(self.main_frame, text="Create Account", height=2, width=20, bg="#96cb4b", fg="white", font=("Arial", 13, "bold"), command=self.create_account)
        create.pack(padx=20, pady=10)

        # Back to Login button
        back_to_login = Button(self.main_frame, text="Back to Login", height=2, width=20, bg="#96cb4b", fg="white", font=("Arial", 13, "bold"), command=self.log)
        back_to_login.pack(padx=20, pady=10)
        self.login_window.destroy()


    def create_account(self):
        username = self.new_username.get()
        password = self.new_password.get()

        if username and password:  # Check that fields are not empty
            self.process_create_account(username, password)
        else:
            messagebox.showerror("Input Error", "Username and password cannot be empty.")

    def process_create_account(self, username, password):
        # Check if username and password are provided
        if not username or not password:
                messagebox.showerror("Input Error", "Username and password cannot be empty.")
                return

        try:
                # Check if the username already exists
                self.db_cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                if self.db_cursor.fetchone():
                        messagebox.showerror("Username Error", "Username already exists. Please choose a different one.")
                        return

                # Create filenames for JSON task and archive
                json_data = {"Personal": {}, "Academic": {}}
                safe_username = "".join(c if c.isalnum() else "_" for c in username)  # Sanitize the username

                # Default filename if username is not valid (should not occur due to previous checks)
                if not safe_username:
                        safe_username = "default_user"
                
                # Create task and archive JSON file paths
                json_task_filename = f"{safe_username}_jsontask.json"
                json_archive_filename = f"{safe_username}_jsonarchive.json"
                
                # Full paths for file writing
                json_task_path = os.path.join(self.json_folder, json_task_filename)
                json_archive_path = os.path.join(self.json_folder, json_archive_filename)

                # Write the JSON files
                with open(json_task_path, 'w') as json_task_file:
                        json.dump(json_data, json_task_file)

                with open(json_archive_path, 'w') as json_archive_file:
                        json.dump(json_data, json_archive_file)

                # Insert the new user into the database, including the JSON filenames
                self.db_cursor.execute(
                        "INSERT INTO users (username, password, json_task, json_archive) VALUES (%s, %s, %s, %s)",
                        (username, password, json_task_filename, json_archive_filename)
                )
                self.db_connection.commit()  # Commit the changes

                messagebox.showinfo("Account Created", "Your account has been successfully created!")
                self.create_account_window.destroy()
                self.show_login()  # Return to the login screen

        except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
        except Exception as e:
                messagebox.showerror("File Error", f"Could not create JSON file: {e}")


            
            
    def on_entry_click(self, event):
        entry = event.widget
        if entry.get() == self.placeholder_username:
            entry.delete(0, "end")  # delete all the text in the entry
            entry.config(fg="#000000")  # Darker text when typing

    def on_focusout(self, event):
        entry = event.widget
        if entry.get() == '':
            entry.insert(0, self.placeholder_username)
            entry.config(fg='#505050')  # Darker placeholder color

    def on_entry_clickP(self, event):
        entry = event.widget
        if entry.get() == self.placeholder_password:
            entry.delete(0, "end")  # delete all the text in the entry
            entry.config(fg="#000000")  # Darker text when typing

    def on_focusoutP(self, event):
        entry = event.widget
        if entry.get() == '':
            entry.insert(0, self.placeholder_password)
            entry.config(fg='#505050')  # Darker placeholder color
        
        
    def Amainwindow(self):
        self.login_window.destroy()
        self.load_tasks()
        self.mainwindow = tk.Toplevel(self.root)
        self.mainwindow.geometry("1430x800")
        # Create the main frame
        frontFrame = tk.Frame(self.mainwindow, bg="white")
        frontFrame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Configure grid for the main frame
        frontFrame.grid_columnconfigure(0, weight=1)  # For logo
        frontFrame.grid_columnconfigure(1, weight=3)  # For title
        frontFrame.grid_columnconfigure(2, weight=1)  # For bell and history icons
        frontFrame.grid_rowconfigure(0, weight=0)  # For title and logo
        frontFrame.grid_rowconfigure(1, weight=0)  # For search bar
        frontFrame.grid_rowconfigure(2, weight=1)  # For resultFrame (expandable)
        frontFrame.grid_rowconfigure(3, weight=0)  # For add button

        # Load and resize the logo image
        logo = Image.open("HCI project/logo.png")
        logo = logo.resize((190, 130), Image.LANCZOS)
        img = ImageTk.PhotoImage(logo)

        # Create and place the logo label
        log = tk.Label(frontFrame, image=img, bg="white")
        log.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        log.image = img

        # Title label for the app
        todotitle = tk.Label(frontFrame, text="To Do List Application", font=("Times", 50), bg="white", fg="#5B5DA8")
        todotitle.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")

        # Frame for bell and history icons
        bell_history_frame = tk.Frame(frontFrame, bg="white")
        bell_history_frame.grid(row=0, column=2, padx=10, pady=10, sticky="ne")

        # Load and place bell and history images
        bell = Image.open("HCI project/bell.png").resize((70, 60), Image.LANCZOS)
        bel = ImageTk.PhotoImage(bell)
        be = tk.Label(bell_history_frame, image=bel, bg="white")
        be.pack(side="left", padx=5)
        be.image = bel
        be.bind("<Button-1>", self.show_sorter)

        history_img = Image.open("HCI project/history.png").resize((70, 60), Image.LANCZOS)
        hist_img = ImageTk.PhotoImage(history_img)
        history_button = tk.Label(bell_history_frame, image=hist_img, bg="white")
        history_button.pack(side="left", padx=5)
        history_button.image = hist_img
        history_button.bind("<Button-1>", self.open_history_window)
        
         # Load and place the exit image
        exit_img = Image.open("HCI project/exit.png").resize((70, 60), Image.LANCZOS)
        ex_img = ImageTk.PhotoImage(exit_img)
        exit_button = tk.Label(bell_history_frame, image=ex_img, bg="white")
        exit_button.pack(side="left", padx=5)
        exit_button.image = ex_img
        exit_button.bind("<Button-1>", self.logout)  # You can bind to any function that closes the window

        # Create frame for search bar and icon
        searchFrame = tk.Frame(frontFrame, bg="white")
        searchFrame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        search = Image.open("HCI project/search.png").resize((40, 40), Image.LANCZOS)
        searc = ImageTk.PhotoImage(search)
        sear = tk.Label(searchFrame, image=searc, bg="white")
        sear.pack(side="left", padx=5)
        sear.image = searc

        self.searchbar_placeholder = "Search Task"
        self.searchBar = tk.Entry(searchFrame, width=50, font=("Arial", 20))
        self.searchBar.insert(0, self.searchbar_placeholder)
        self.searchBar.bind('<FocusIn>', self.on_entry_clickSearch)
        self.searchBar.bind('<FocusOut>', self.on_focusoutSearch)
        self.searchBar.pack(side="left", padx=5, ipady=10)

        # Create result frame
        self.resultFrame = tk.Frame(frontFrame, bg="grey", borderwidth=2, relief="solid")
        self.resultFrame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.resultFrame.grid_rowconfigure(0, weight=1)  # Make the inner frame expandable
        self.resultFrame.grid_columnconfigure(0, weight=1)

        # Scrollbar for Treeview
        scrollbar = tk.Scrollbar(self.resultFrame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create the Treeview widget with larger text
        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Helvetica", 12))  # Set font size
        style.configure("Custom.Treeview.Heading", font=("Helvetica", 17, "bold"))  # Set heading font size

        # Create the Treeview widget
        self.tree = ttk.Treeview(self.resultFrame, columns=("Task", "Priority", "Status", "Due Date"), show='headings', height=10)
        self.tree.heading("Task", text="Task")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Due Date", text="Due Date")  # Added Due Date column

        # Configure the columns' width and alignment
        self.tree.column("Task", width=400, anchor="center")
        self.tree.column("Priority", width=200, anchor="center")
        self.tree.column("Status", width=150, anchor="center")
        self.tree.column("Due Date", width=150, anchor="center")  # Added Due Date column width

        # Apply styles for the entire Treeview
        style.configure("Treeview", rowheight=40)  # Set row height
        style.configure("Treeview.Heading", font=("Arial", 16))  # Set heading font size
        
        style.configure("Custom.Treeview", font=("Helvetica", 12))  # Set font size for the entire Treeview
        
        # Set the style to the Treeview
        self.tree.configure(style="Custom.Treeview")

        # Pack the Treeview into the frame
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure the scrollbar
        scrollbar.config(command=self.tree.yview)
        self.tree.config(yscrollcommand=scrollbar.set)

        # Add Button
        add = Image.open("HCI project/add.png").resize((60, 60), Image.LANCZOS)
        ad = ImageTk.PhotoImage(add)
        add_button = tk.Button(frontFrame, image=ad, bg="white", borderwidth=0, command=self.open_task_window)
        add_button.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")
        add_button.image = ad

        # Insert some sample data
        self.add_listbox()
        self.tree.bind("<ButtonRelease-1>", self.display_selected_task)
        self.start_monitoring()    
        
    def logout(self,event):
        
        
        msg = messagebox.askyesno("Logout Confirmation", "Do you want to logout?")
        if msg:
            self.username = ""
            self.password = ""
            self.mainwindow.destroy()
            self.show_login()  

    def check_due_dates(self):
        """Check the due dates of tasks and alert if a task is overdue."""
        while True:
                if hasattr(self, 'tree'):  # Check if self.tree exists
                        current_time = datetime.now()
                        for category, task_list in self.data.items():
                                for task_name, task_info in task_list.items():
                                        due_date_str = task_info.get("Due Date")

                                        if due_date_str is None:
                                                print(f"No due date for task '{task_name}'.")
                                                continue

                                        try:
                                                due_date = datetime.strptime(due_date_str, "%m/%d/%y %I:%M %p")
                                        except ValueError as e:
                                                print(f"Error parsing date for task '{task_name}': {e}")
                                                continue

                                        # Check if the task is overdue
                                        if current_time >= due_date and task_info["Status"] == "Pending":
                                                task_info["Status"] = "Overdue"  # Mark task as overdue
                                                self.save_tasks()  # Save the updated task status
                                                messagebox.showinfo("Task Overdue", f"The task '{task_name}' is overdue!")

                        self.add_listbox()  # Update the listbox with any changes
                time.sleep(10)


             
    def save_tasks(self):
        """Save the updated tasks to the JSON file."""
        path = f"HCI project/json_files/{self.entered_username}_jsontask.json"
        
        with open(path, 'w') as file:
            json.dump(self.data, file, indent=4)
            
    def start_monitoring(self):
        """Start the monitoring process in a separate thread."""
        threading.Thread(target=self.check_due_dates, daemon=True).start()
    
        

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
      path = f"HCI project/json_files/{self.entered_username}_jsonarchive.json"
      if os.path.exists(path):
        with open(path, 'r') as file:
            history = json.load(file)
            
            # Iterate over each category and task
            for category, tasks in history.items():
                # Insert the category as a header
                self.history_listbox.insert(tk.END, f"{category}:")
                
                self.history_listbox.itemconfig(tk.END, {'fg': '#518d45'})  # Optional: Make category stand out

                for task_name, details in tasks.items():
                    # Format the task details with an 8-space indent
                    due_date = details.get("Due Date", "N/A")
                    
                    task_info = f"        {task_name} - Due Date: {due_date}"
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
                path = f"HCI project/json_files/{self.entered_username}_jsonarchive.json"
                with open(path, 'r') as file:
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
                path = f"HCI project/json_files/{self.entered_username}_jsonarchive.json"
                with open(path, 'w') as file:
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
        self.tree.tag_configure('high_priority', background='#EF5350', foreground='black', font=("Arial", 16))
        self.tree.tag_configure('medium_priority', background='#EF5350', foreground='black', font=("Arial", 16))
        self.tree.tag_configure('low_priority', background='#EF5350', foreground='black', font=("Arial", 16))
        self.tree.tag_configure('done', background='#43A047', foreground='black', font=("Arial", 16))  # Tag for done tasks

        try:
            path = f"HCI project/json_files/{self.entered_username}_jsontask.json"
            # Open the JSON file and load the data
            with open(path, 'r') as json_file:
                self.alltask = json.load(json_file)  # Load data into self.alltask
                print("Tasks loaded successfully:", self.alltask)
        except FileNotFoundError:
            print("The file 'task.json' was not found.")
            self.alltask = {"Personal": {}, "Academic": {}}  # Initialize to prevent errors
        except json.JSONDecodeError:
            print("Error decoding JSON from the file.")
            self.alltask = {"Personal": {}, "Academic": {}}  # Initialize to prevent errors
        except Exception as e:
            print("An error occurred:", str(e))
            self.alltask = {"Personal": {}, "Academic": {}}  # Initialize to prevent errors

        # Clear the Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        def get_priority_tag(priority):
            """Returns the appropriate tag based on priority."""
            if priority.lower() == "high":
                return 'high_priority'
            elif priority.lower() == "medium":
                return 'medium_priority'
            elif priority.lower() == "low":
                return 'low_priority'
            else:
                return ''  # No tag if priority is unknown

        # Check if 'Personal' category exists and loop through personal tasks
        if "Personal" in self.alltask:
            for task_key, task_info in self.alltask["Personal"].items():
                task_title = task_key
                priority = task_info.get("Priority", "N/A")  # Get priority, default to "N/A"
                status = task_info.get("Status", "Pending")      # Get status, default to "N/A"
                due_date = task_info.get("Due Date", "N/A")  # Get due date, default to "N/A"
                tag = get_priority_tag(priority)  # Get the priority tag

                # Add the done tag if status is "Done"
                if status.lower() == "done":
                    tag = 'done'  # Override tag to 'done' if the status is done

                print(f"Adding Personal Task: {task_title}, Priority: {priority}, Status: {status}, Due Date: {due_date}")  # Debug print
                # Insert the task into the Treeview with the appropriate tag
                self.tree.insert("", tk.END, values=(task_title, priority, status, due_date, "Personal"), tags=(tag,))

        # Check if 'Academic' category exists and loop through academic tasks
        if "Academic" in self.alltask:
            for task_key, task_info in self.alltask["Academic"].items():
                task_title = task_key
                priority = task_info.get("Priority", "N/A")  # Get priority, default to "N/A"
                status = task_info.get("Status", "Pending")      # Get status, default to "N/A"
                due_date = task_info.get("Due Date", "N/A")  # Get due date, default to "N/A"
                tag = get_priority_tag(priority)  # Get the priority tag

                # Add the done tag if status is "Done"
                if status.lower() == "done":
                    tag = 'done'  # Override tag to 'done' if the status is done

                print(f"Adding Academic Task: {task_title}, Priority: {priority}, Status: {status}, Due Date: {due_date}")  # Debug print
                # Insert the task into the Treeview with the appropriate tag
                self.tree.insert("", tk.END, values=(task_title, priority, status, due_date, "Academic"), tags=(tag,))

        # Print a message if no tasks are found
        if not self.tree.get_children():
            print("No tasks found to display.")
    time.sleep(1)






            
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
        self.category_combo = tk.StringVar(value="Academic")  # Default value

        # Create a frame to hold the radio buttons
        radio_frame = tk.Frame(self.task_chooser)
        radio_frame.pack(pady=10)

        # Create radio buttons for 'Academic' and 'Personal'
        academic_radio = tk.Radiobutton(radio_frame, text="Academic", variable=self.category_combo, value="Academic", font=("Arial", 12), command=self.on_category_selected)
        personal_radio = tk.Radiobutton(radio_frame, text="Personal", variable=self.category_combo, value="Personal", font=("Arial", 12), command=self.on_category_selected)

        # Pack the radio buttons horizontally
        academic_radio.pack(side=tk.LEFT, padx=10)
        personal_radio.pack(side=tk.LEFT, padx=10)
        
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
        

        
        
    def on_category_selected(self):
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
        self.subcategory_window.geometry("400x400")  # Increased height to accommodate radio buttons

        # Subject Label
        self.subject_label = tk.Label(self.subcategory_window, text="Subject:", font=('Arial', 12))
        self.subject_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')  # Align to the west
        
        # Subjects for ComboBox
        subjects = ["Mathematics", "Science", "History", "English", "Computer Science", "Art"]

        # Subject ComboBox
        self.subject_combobox = ttk.Combobox(self.subcategory_window, values=subjects, font=('Arial', 12), width=28)
        self.subject_combobox.grid(row=0, column=1, padx=10, pady=10)

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

        # Priority Label
        self.priority_label = tk.Label(self.subcategory_window, text="Priority:", font=('Arial', 12))
        self.priority_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        # Variable to hold priority selection
        self.priority_var = tk.StringVar(value="Medium")  # Default value

        # Radio Buttons for Priority
        self.high_priority = tk.Radiobutton(self.subcategory_window, text="High", variable=self.priority_var, value="High", font=('Arial', 12))
        self.high_priority.grid(row=3, column=1, padx=10, pady=5, sticky='w')

        self.medium_priority = tk.Radiobutton(self.subcategory_window, text="Medium", variable=self.priority_var, value="Medium", font=('Arial', 12))
        self.medium_priority.grid(row=4, column=1, padx=10, pady=5, sticky='w')

        self.low_priority = tk.Radiobutton(self.subcategory_window, text="Low", variable=self.priority_var, value="Low", font=('Arial', 12))
        self.low_priority.grid(row=5, column=1, padx=10, pady=5, sticky='w')

        # Submit Button
        self.submit_button = tk.Button(self.subcategory_window, text="Submit", command=self.submit_task, font=('Arial', 12), width=20)
        self.submit_button.grid(row=6, column=1, padx=10, pady=20, sticky='ew')  # Align with Due Date Button

        # Make the layout more spacious
        for i in range(7):
                self.subcategory_window.grid_rowconfigure(i, weight=1)
        for j in range(2):
                self.subcategory_window.grid_columnconfigure(j, weight=1)
    
    def open_personal_task_window(self):
        self.subcategory_window = tk.Toplevel(self.root)
        self.subcategory_window.title("Personal Task")

        # Set a larger size for the window
        self.subcategory_window.geometry("400x400")  # Increased height to accommodate radio buttons

        # Personal Task Selection (using an Entry)
        self.task_label = tk.Label(self.subcategory_window, text="Where:", font=('Arial', 12))
        self.task_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        # Where Entry
        self.where_entry = tk.Entry(self.subcategory_window, font=('Arial', 12), width=30)
        self.where_entry.grid(row=0, column=1, padx=10, pady=10)

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

        # Priority Label
        self.priority_label = tk.Label(self.subcategory_window, text="Priority:", font=('Arial', 12))
        self.priority_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        # Variable to hold priority selection
        self.priority_var = tk.StringVar(value="Medium")  # Default value

        # Radio Buttons for Priority
        self.high_priority = tk.Radiobutton(self.subcategory_window, text="High", variable=self.priority_var, value="High", font=('Arial', 12))
        self.high_priority.grid(row=3, column=1, padx=10, pady=5, sticky='w')

        self.medium_priority = tk.Radiobutton(self.subcategory_window, text="Medium", variable=self.priority_var, value="Medium", font=('Arial', 12))
        self.medium_priority.grid(row=4, column=1, padx=10, pady=5, sticky='w')

        self.low_priority = tk.Radiobutton(self.subcategory_window, text="Low", variable=self.priority_var, value="Low", font=('Arial', 12))
        self.low_priority.grid(row=5, column=1, padx=10, pady=5, sticky='w')

        # Submit Button
        self.submit_button = tk.Button(self.subcategory_window, text="Submit", command=self.submit_task, font=('Arial', 12), width=20)
        self.submit_button.grid(row=6, column=1, padx=10, pady=20, sticky='ew')  # Align with Due Date Button

        # Make the layout more spacious
        for i in range(7):
                self.subcategory_window.grid_rowconfigure(i, weight=1)
        for j in range(2):
                self.subcategory_window.grid_columnconfigure(j, weight=1)
            
            
    def on_entry_clickSearch(self, event):
        if self.searchBar.get() == self.searchbar_placeholder:
            self.searchBar.delete(0, "end")
    
    def on_focusoutSearch(self, event):
        if not self.searchBar.get():
            self.searchBar.insert(0, self.searchbar_placeholder)
            
    
        
    def submit_task(self):
        # Get the category and task prefix from the combo boxes
        sub = self.task_combo.get().strip()
        category = self.category_combo.get()

        # Get priority
        priority = self.priority_var.get()  # Get the selected priority from radio buttons

        # File name for storing tasks
        path = f"HCI project/json_files/{self.entered_username}_jsontask.json"

        # Load existing tasks or initialize an empty dictionary
        if os.path.exists(path):
                with open(path, 'r') as json_file:
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
                where = self.where_entry.get().strip()  # Get the entry from 'where' (combo box)
                description = self.description_entry.get("1.0", tk.END).strip()
                due_date = self.full_time  # Assume full_time is set when selecting the date

                # Create task info for personal task
                task_info = {
                        "where": where,
                        "description": description,
                        "Due Date": due_date,
                        "Priority": priority,  # Include priority
                        "Status": "Pending"
                }

                # Add the new personal task to the all_tasks dictionary
                all_tasks["Personal"][subname] = task_info

        elif category == "Academic":
                # Get academic task entry data
                subject = self.subject_combobox.get().strip()  # Use subject from the combo box
                description = self.description_entry.get("1.0", tk.END).strip()
                due_date = self.full_time  # Assume full_time is set when selecting the date

                # Create task info for academic task
                task_info = {
                        "subject": subject,
                        "description": description,
                        "Due Date": due_date,
                        "Priority": priority,
                        "Status": "Pending" # Include priority
                }

                # Add the new academic task to the all_tasks dictionary
                all_tasks["Academic"][subname] = task_info

        # Save the updated all_tasks dictionary to the JSON file
        with open(path, 'w') as json_file:
                json.dump(all_tasks, json_file, indent=4)

        # Print confirmation of the submitted task
        print(f"Task Submitted: {task_info} in {category} category under key: {subname}")
        self.subcategory_window.destroy()
        self.task_chooser.destroy()
        self.add_listbox()


        
    def display_selected_task(self, event):
        # Ensure something is selected
        selected_item = self.tree.selection()
        if not selected_item:
            return  # Exit if nothing is selected

        # Create a new Toplevel window to show task details
        self.details_window = tk.Toplevel()
        self.details_window.geometry("800x700")  # Ensure the window is large enough

        # Title label directly in the details_window
        title_label = tk.Label(self.details_window, text="Task Details", font=("Times", 30, "bold"), pady=20, fg="#518D45")
        title_label.pack()

        # Get the selected task details
        selected_task = self.tree.item(selected_item)

        # Extract values from the selected task (task title, priority, status, etc.)
        task_title, priority, status, due_date, category = selected_task['values']

        # Display Category Label
        category_label = tk.Label(self.details_window, text=f"Category: {category}", font=("Arial", 20), pady=10, fg="#518D45")
        category_label.pack()

        # Display Task Title
        task_label = tk.Label(self.details_window, text=f"Task: {task_title}", font=("Arial", 20), pady=10, fg="#518D45")
        task_label.pack()

        # Find the task details using the task title
        task_info = self.alltask.get(category, {}).get(task_title, {})

        if not task_info:
            return  # Exit if task not found

        # Display task details as labels
        for key, value in task_info.items():
            if key == "description":
                description_text = tk.Text(self.details_window, font=("Arial", 18), fg="#518D45", height=5, width=50)
                description_text.insert(tk.END, value)  # Insert the description into the Text widget
                description_text.pack(pady=10)
                description_text.config(state=tk.DISABLED)  # Make it read-only
            else:
                tk.Label(self.details_window, text=f"{key.capitalize()}: {value}", font=("Arial", 18), fg="#518D45").pack(pady=10)

        # Create a Text widget to display the task context if it exists
        if "context" in task_info:
            context_text = tk.Text(self.details_window, font=("Arial", 18), fg="#518D45", height=10, width=80)
            context_text.pack(padx=10, pady=10)

            # Insert task context into the Text widget
            context_text.insert(tk.END, task_info["context"])
            context_text.config(state=tk.DISABLED)  # Make it read-only

        # Create the "Mark as Done" button
        mark_done_frame = tk.Frame(self.details_window)
        mark_done_frame.pack(pady=10, anchor="center")  # Pack the frame and center it

        # Mark as Done button
        mark_done_button = tk.Button(mark_done_frame, text="Mark as Done", font=("Arial", 16), command=lambda: self.mark_task_as_done(category, task_title, selected_item), fg="#518D45")
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

# Function to mark a task as done
    def mark_task_as_done(self, category, task_title, selected_item):
     if category in self.alltask and task_title in self.alltask[category]:
        # Update the task's status to 'Done'
        self.alltask[category][task_title]['Status'] = 'Done'  # Ensure 'Status' matches your JSON structure
        print(f"Updated {task_title} status to Done")  # Debug print
        

        # Change the Treeview row's color to indicate it's done (green background)
        self.tree.item(selected_item, tags=('done',))  # Apply 'done' tag
        self.tree.tag_configure('done', background='#42b84a', foreground='black')  # Set color for 'done' tasks

        # Save the updated tasks to the JSON file
        self.save_tasks_to_json()  # Call save method
        print(f"Tasks saved to JSON: {self.alltask}")  # Debug print

        # Close the details window
        self.details_window.destroy()
     else:
        print("Task not found for updating.")  # Debug print for error handling
        

    def save_tasks_to_json(self):
        # Prepare the path for saving tasks to JSON file
        path = f"HCI project/json_files/{self.entered_username}_jsontask.json"  # Updated path

        # Save the current tasks to a JSON file
        with open(path, "w") as f:
            json.dump(self.alltask, f, indent=4)

        try:
            # Update the database with the new JSON file path in the json_task column
            self.db_cursor.execute(
                "UPDATE users SET json_task = %s WHERE username = %s",
                (path, self.entered_username)
            )
            self.db_connection.commit()  # Commit the changes
            print(f"Updated JSON path in database for user: {self.entered_username}")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

        self.add_listbox()  # Refresh the listbox or UI element as needed
        

# Function to delete a task
    def delete_task(self, category, task_title):
        # Remove the task from the internal data
        if category in self.alltask and task_title in self.alltask[category]:
            del self.alltask[category][task_title]

        # Update the Treeview to reflect the deletion
        selected_item = self.tree.selection()[0]
        self.tree.delete(selected_item)
        
        # Close the details window
        self.details_window.destroy()


    def delete_task(self, category, task_title):
        # Prepare the path for loading existing tasks from the JSON file
        path = f"HCI project/json_files/{self.entered_username}_jsontask.json"  # Updated path for user-specific JSON

        # Load existing tasks from the user's JSON file
        with open(path, 'r') as file:
            tasks = json.load(file)

        # Remove the task from the tasks dictionary
        if category in tasks and task_title in tasks[category]:
            task_info = tasks[category][task_title]  # Store task info before deletion
            del tasks[category][task_title]  # Delete the task

            # Write the updated tasks back to the user's JSON file
            with open(path, 'w') as file:
                json.dump(tasks, file, indent=4)

            # Archive the deleted task to archives.json
            self.archive_task(category, task_title, task_info)
            self.details_window.destroy()

            # Update the listbox
            self.add_listbox()


    def archive_task(self, category, task_title, task_info):
        # Prepare the path for the archives file
        archive_path = f'HCI project/json_files/{self.entered_username}_jsonarchive.json'  # You can also make this dynamic if needed

        # Load existing archives from archives.json
        try:
            with open(archive_path, 'r') as file:
                archives = json.load(file)
        except FileNotFoundError:
            archives = {}

        # Ensure the category exists in archives
        if category not in archives:
            archives[category] = {}
        archives[category][task_title] = task_info  # Add the task info to the archives

        # Write the updated archives back to archives.json
        with open(archive_path, 'w') as file:
            json.dump(archives, file, indent=4)

    def load_tasks(self):
        # Prepare the path for loading the user's tasks
        path = f"HCI project/json_files/{self.entered_username}_jsontask.json"  # Updated path for user-specific JSON

        # Load tasks from the user's JSON file
        try:
            with open(path, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {"Personal": {}, "Academic": {}}  # Initialize empty structure if file does not exist

            
    def show_sorter(self, event):
        self.load_tasks()
        sorter_window = tk.Toplevel()
        sorter_window.title("Task Sorter")
        sorter_window.geometry("600x600")  # Make the window bigger

        # Create a frame for the scrollbar and the content
        frame = tk.Frame(sorter_window)
        frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas to hold the content
        canvas = tk.Canvas(frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas to work with the scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create another frame to hold the content within the canvas
        content_frame = tk.Frame(canvas)

        # Create a window in the canvas to hold the content frame
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        # Update scrollregion after creating widgets
        def on_frame_configure(event):
                canvas.configure(scrollregion=canvas.bbox("all"))

        content_frame.bind("<Configure>", on_frame_configure)

        # Get today's date
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)

        # Initialize sorted task categories
        sorted_tasks = {
                "Overdue": {},
                "Due Today": {},
                "Due Tomorrow": {},
                "Next Week": {}
        }

        # Sorting tasks by their due dates
        for category, tasks in self.data.items():
                for task_name, task_details in tasks.items():
                        due_date_str = task_details.get("Due Date")
                        if due_date_str:
                                try:
                                        due_date = datetime.strptime(due_date_str, "%m/%d/%y %I:%M %p")
                                        due_date_only = due_date.date()

                                        if due_date_only < today:
                                                sorted_tasks["Overdue"].setdefault(category, {})[task_name] = task_details
                                        elif due_date_only == today:
                                                sorted_tasks["Due Today"].setdefault(category, {})[task_name] = task_details
                                        elif due_date_only == tomorrow:
                                                sorted_tasks["Due Tomorrow"].setdefault(category, {})[task_name] = task_details
                                        elif today < due_date_only <= (today + timedelta(days=7)):
                                                sorted_tasks["Next Week"].setdefault(category, {})[task_name] = task_details

                                except ValueError:
                                        print(f"Error parsing date: {due_date_str}")

        # Display sorted tasks with larger font and colored text
        font = ("Arial", 12)  # Change the font size to make the text bigger

        for category, tasks in sorted_tasks.items():
                tk.Label(content_frame, text=category, font=("Arial", 14, "bold"), fg="#518D45").pack(anchor="w")  # Category headers in larger bold font
                for task_category, task_details in tasks.items():
                        tk.Label(content_frame, text=f"Category: {task_category}", font=("Arial", 12,"bold"), fg="#518D45").pack(anchor="w", padx=10)
                        for task_name, task_info in task_details.items():
                                tk.Label(content_frame, text=f"Task: {task_name}", font=font, fg="#518D45").pack(anchor="w", padx=20)
                                due_date_label = f"Due Date: {task_info['Due Date']}"
                                tk.Label(content_frame, text=due_date_label, font=font, fg="#518D45").pack(anchor="w", padx=30)

        print(f"Sorted tasks: {sorted_tasks}")

       
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