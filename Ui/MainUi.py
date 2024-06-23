import tkinter as tk
from Ui.login_frame import FirstFrame


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        window_width = 600
        window_height = 540

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2

        self.title("Login Forum")
        self.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        self.frame = FirstFrame(self)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.frame.pack()

    def change(self, frame):
        self.frame.pack_forget()
        self.frame = frame(self)
        self.frame.pack()
