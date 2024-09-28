import tkinter as tk
from tkinter import ttk

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("400x300")

        # Create a label to prompt the user to choose a task category
        self.label = tk.Label(self.root, text="Choose Task Category", font=("Arial", 14))
        self.label.pack(pady=10)

        # Create a Combobox for task categories
        self.category_combo = ttk.Combobox(self.root, values=["Academic", "Personal"], font=("Arial", 12))
        self.category_combo.pack(pady=10)
        self.category_combo.bind("<<ComboboxSelected>>", self.on_category_selected)

        # Create a Combobox for tasks (Initially empty, will populate based on category selection)
        self.task_combo = ttk.Combobox(self.root, font=("Arial", 12))
        self.task_combo.pack(pady=10)

        # Add buttons for actions
        self.add_task_button = tk.Button(self.root, text="Add Task", font=("Arial", 12), command=self.add_task)
        self.add_task_button.pack(pady=10)

        self.exit_button = tk.Button(self.root, text="Exit", font=("Arial", 12), command=self.root.quit)
        self.exit_button.pack(pady=10)

    def on_category_selected(self, event):
        # Get the selected category
        category = self.category_combo.get()

        # Define academic and personal tasks
        academic_tasks = ["Submit Assignment", "Prepare for Exam", "Attend Class", "Group Project Meeting"]
        personal_tasks = ["Grocery Shopping", "Pay Bills", "Clean the House", "Cook Dinner"]

        # Populate the task combo based on selected category
        if category == "Academic":
            self.task_combo['values'] = academic_tasks
        elif category == "Personal":
            self.task_combo['values'] = personal_tasks

        # Set the first task as default in the task combo box
        self.task_combo.current(0)

    def add_task(self):
        # Get the selected task from the task combo box
        selected_task = self.task_combo.get()
        if selected_task:
            print(f"Task '{selected_task}' added to the list!")
        else:
            print("No task selected!")

# Initialize the Tkinter app
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
