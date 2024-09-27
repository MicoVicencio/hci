import tkinter as tk

def add_dict_to_listbox(dictionary):
    # Clear the listbox before adding items
    listbox.delete(0, tk.END)

    # Add dictionary items to the listbox
    for key, value in dictionary.items():
        listbox.insert(tk.END, f"{key}: {value}")

# Sample dictionary
sample_dict = {
    "Task 1": "Description of task 1",
    "Task 2": "Description of task 2",
    "Task 3": "Description of task 3",
}

# Create the main window
root = tk.Tk()

# Create the Listbox widget
listbox = tk.Listbox(root, width=50, height=10)
listbox.pack(pady=10)

# Button to add dictionary items to the Listbox
add_button = tk.Button(root, text="Add Dictionary to Listbox", command=lambda: add_dict_to_listbox(sample_dict))
add_button.pack(pady=5)

# Run the main loop
root.mainloop()
