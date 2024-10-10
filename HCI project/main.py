import tkinter as tk
from tkinter import Label, Frame, Entry, Button, messagebox
from PIL import Image, ImageTk
from todo import App  # Import your todo app

class TodoList:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("To Do List App")
        self.root.geometry("900x600")

        # Placeholder texts
        self.placeholder_username = "Username"
        self.placeholder_password = "Password"

        # Hardcoded valid credentials for login
        self.valid_username = "admin"
        self.valid_password = "password123"

        # Load image
        imgPath = r"C:\Users\micov\OneDrive\Desktop\HCI project\face.png"
        img = Image.open(imgPath)
        new_size = (120, 100)  # Specify the new size (width, height)
        img_resized = img.resize(new_size, Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(img_resized)

        # Create main frame
        self.main_frame = Frame(self.root, bg="#518d45", height=500, width=900)
        self.main_frame.pack_propagate(False)
        self.main_frame.pack(padx=50, pady=50)

        # Show login by default
        self.show_login()

        self.root.mainloop()

    def show_login(self):
        # Clear the main frame
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

    def login(self):
        entered_username = self.username.get()
        entered_password = self.password.get()

        # Check if the entered username and password are correct
        if entered_username == self.valid_username and entered_password == self.valid_password:
            messagebox.showinfo("Login Successful", "Welcome to the To-Do List App!")
            self.root.destroy()  # Close the login window
            todo_root = tk.Tk()  # Create a new window for the To-Do List App
            App(todo_root, entered_username, entered_password)  # Pass credentials to the To-Do App
            todo_root.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")

    def show_create_account(self):
        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Create title label
        title_label = Label(self.main_frame, text="Create Account", bg="#518d45", fg="white", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)

        # Create image label
        label = Label(self.main_frame, image=self.photo, bg="#518d45")
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
        create = Button(self.main_frame, text="Create Account", height=2, width=20, bg="#96cb4b", fg="white", font=("Arial", 13, "bold"))
        create.pack(padx=20, pady=10)

        # Back to Login button
        back_to_login = Button(self.main_frame, text="Back to Login", height=2, width=20, bg="#96cb4b", fg="white", font=("Arial", 13, "bold"), command=self.show_login)
        back_to_login.pack(padx=20, pady=10)

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


todoList = TodoList()
