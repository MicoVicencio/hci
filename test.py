import tkinter as tk
from tkinter import ttk

# Function to convert each line in the text box to a combo box item
def convert_to_combo():
    # Split the text by lines
    items = text_box.get("1.0", tk.END).strip().split("\n")
    combo_box['values'] = items  # Set items in the combo box
    text_box.delete("1.0", tk.END)  # Optional: Clear the text box after conversion

# Set up the main window
root = tk.Tk()
root.title("Text to Combo Box")

# Multi-line text box
text_box = tk.Text(root, width=30, height=5)
text_box.pack(pady=10)

# Convert button
convert_button = tk.Button(root, text="Convert to Combo Box", command=convert_to_combo)
convert_button.pack(pady=5)

# Combo box
combo_box = ttk.Combobox(root, width=30)
combo_box.pack(pady=10)

# Run the application
root.mainloop()
