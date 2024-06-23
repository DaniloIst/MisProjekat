import tkinter as tk
from tkinter import ttk, messagebox
import sv_ttk
from firebase_admin import auth, db
from Ui.admin_frame import SecondFrame
from Ui.fitter_frame import FitterFrame
from Ui.audiolog_frame import AuditorFrame

class FirstFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        login_label = ttk.Label(self, text="Login", font=("Helvetica", 24))
        username_label = ttk.Label(self, text="Username", font=("Helvetica", 14))
        self.username_entry = ttk.Entry(self)
        self.password_entry = ttk.Entry(self, show="*")
        password_label = ttk.Label(self, text="Password", font=("Helvetica", 14))
        login_button = ttk.Button(self, text="Login", command=self.check_login)

        login_label.grid(row=0, column=0, columnspan=2, pady=20, padx=80)
        username_label.grid(row=1, column=0, pady=(40, 10), padx=(20, 20), sticky='e')
        self.username_entry.grid(row=2, column=0, columnspan=2, pady=(50, 0), padx=(40, 40), sticky='w')
        password_label.grid(row=3, column=0, pady=(20, 10), padx=(20, 20), sticky='e')
        self.password_entry.grid(row=4, column=0, columnspan=2, pady=(30, 10), padx=(40, 40), sticky='w')
        login_button.grid(row=5, column=0, columnspan=2, pady=20)

        sv_ttk.set_theme("dark")

    def check_login(self):
        email = self.username_entry.get()
        password = self.password_entry.get()
        user_id = self.login(email, password)

        if user_id is not None:
            role = self.checkRole(email)
            if role == "Admin":
                self.master.change(SecondFrame)
            elif role == "Fitter":
                self.master.change(FitterFrame)
            elif role == "Auditor":
                self.master.change(AuditorFrame)
            else:
                messagebox.showerror(title="Error", message="Role not found.")
        else:
            messagebox.showerror(title="Error", message="Invalid login.")

    def checkRole(self, email):
        ref = db.reference("/Users")
        users = ref.get()
        for user_id, user_data in users.items():
            if isinstance(user_data, dict) and user_data.get('email', '') == email:
                return user_data.get('role', '')

    def login(self, email: str, password: str):
        try:
            user = auth.get_user_by_email(email)
            return user.uid
        except Exception as e:
            print(f'Error verifying user: {e}')
            return None
