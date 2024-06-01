import tkinter
from tkinter import ttk, messagebox
import main

import sv_ttk

def draw():
    global username_entry, password_entry
    window = tkinter.Tk()
    window.title("Login form")
    window.geometry('600x440')
    window.configure()
    window.resizable(False, False)

    frame = tkinter.Frame()


    frame.pack()


    sv_ttk.set_theme("dark")

    window.mainloop()
