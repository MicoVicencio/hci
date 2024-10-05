import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Create the main window
root = tk.Tk()
root.title("To-Do List with Treeview")
root.geometry("900x400")

# Function to add tasks with priority-based color
def add_task():
    task = task_entry.get()
    priority = priority_combobox.get()
    
    if task and priority:
        if priority == "High":
            tag = 'high_priority'
        elif priority == "Medium":
            tag = 'medium_priority'
        else:
            tag = 'low_priority'
        
        tree.insert('', 'end', values=(task, priority, 'Pending'), tags=(tag,))
        task_entry.delete(0, tk.END)

# Function to mark task as completed
def mark_as_done():
    selected_item = tree.selection()
    if selected_item:
        tree.item(selected_item, values=(tree.item(selected_item, 'values')[0],
                                         tree.item(selected_item, 'values')[1],
                                         'Completed'))

# Function to remove a task
def remove_task():
    selected_item = tree.selection()
    if selected_item:
        tree.delete(selected_item)

# Function to show selected task details
def show_selected_task():
    selected_item = tree.selection()  # Get selected item
    if selected_item:
        task_details = tree.item(selected_item, 'values')  # Get task details
        messagebox.showinfo("Task Details", f"Task: {task_details[0]}\nPriority: {task_details[1]}\nStatus: {task_details[2]}")
    else:
        messagebox.showwarning("Selection Error", "No task selected!")

# Task input section
task_label = tk.Label(root, text="Task")
task_label.pack(pady=5)

task_entry = tk.Entry(root)
task_entry.pack(pady=5)

priority_label = tk.Label(root, text="Priority")
priority_label.pack(pady=5)

priority_combobox = ttk.Combobox(root, values=["High", "Medium", "Low"], state="readonly")
priority_combobox.pack(pady=5)
priority_combobox.current(1)  # Default to "Medium"

# Treeview to display tasks
tree = ttk.Treeview(root, columns=("Task", "Priority", "Status"), show='headings', height=10)
tree.heading("Task", text="Task")
tree.heading("Priority", text="Priority")
tree.heading("Status", text="Status")
tree.pack(pady=10, fill="x")

# Add tags for different priorities
tree.tag_configure('high_priority', background='red', foreground='white')
tree.tag_configure('medium_priority', background='yellow', foreground='black')
tree.tag_configure('low_priority', background='green', foreground='white')
 
# Buttons
add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.pack(pady=5)

done_button = tk.Button(root, text="Mark as Done", command=mark_as_done)
done_button.pack(pady=5)

remove_button = tk.Button(root, text="Remove Task", command=remove_task)
remove_button.pack(pady=5)

# Button to show selected task details
show_button = tk.Button(root, text="Show Selected Task", command=show_selected_task)
show_button.pack(pady=5)

# Run the application
root.mainloop()
