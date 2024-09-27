import  tkinter as tk
from tkinter import Label, Frame, Entry, Button
from PIL import Image, ImageTk 


class TodoList:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("To do List App")
        self.root.geometry("900x500")
        self.placeholder_username = "Username"
        self.placeholder_password = "Password"
        
        front = Frame(self.root,bg="#518d45",height=500,width=550,bd=2,relief="groove")
        imgPath = r"C:\Users\micov\OneDrive\Desktop\HCI project\face.png"
        img = Image.open(imgPath)
        
        new_size = (120, 100)  # Specify the new size (width, height)
        img_resized = img.resize(new_size, Image.LANCZOS)
        
        photo = ImageTk.PhotoImage(img_resized)
        
        label = Label(front,image=photo,bg="#518d45")
        label.pack(padx=10,pady=10)
        label.image = photo
        
        self.username = tk.Entry(front, fg='#96cb4b',width=40)
        self.username.insert(0, self.placeholder_username)
        self.username.bind('<FocusIn>', self.on_entry_click)
        self.username.bind('<FocusOut>', self.on_focusout)
        self.username.pack(padx=10, pady=10,ipady=9)
        
        self.password = tk.Entry(front, fg='#96cb4b',width=40)
        self.password.insert(0, self.placeholder_password)
        self.password.bind('<FocusIn>', self.on_entry_clickP)
        self.password.bind('<FocusOut>', self.on_focusoutP)
        self.password.pack(padx=10, pady=10,ipady=9)
        
        
        
        
        login = Button(front,text="Login",height=2,width=20,bg="#96cb4b",fg="white",font=("Arial",13,"bold"))
        login.pack(padx=20,pady=20)
        
        
        
        
        
        
        
        front.pack_propagate(False)
        front.pack(padx=50,pady=50)
        
   
        
        

    def on_entry_click(self,event):
        if self.username.get() == self.placeholder_username:
            self.username.delete(0, "end")  # delete all the text in the entry
            self.username.config(fg="#96cb4b")

    def on_focusout(self,event):
        if self.username.get() == '':
            self.username.insert(0, self.placeholder_username)
            self.username.config(fg='#96cb4b')
            
    def on_entry_clickP(self,event):
        if self.password.get() == self.placeholder_password:
            self.password.delete(0, "end")  # delete all the text in the entry
            self.password.config(fg='#96cb4b')

    def on_focusoutP(self,event):
        if self.password.get() == '':
            self.password.insert(0, self.placeholder_password)
            self.password.config(fg='#96cb4b')     
               
    def run(self):
        self.root.mainloop()
        
        
todoList = TodoList()
todoList.run()