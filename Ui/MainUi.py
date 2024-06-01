import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox
import sv_ttk
from firebase_admin import credentials, auth, db
from tkcalendar import Calendar


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
        username_label.grid(row=1, column=0, pady=(40, 10), padx=(0, 20), sticky='e')
        self.username_entry.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky='w')
        password_label.grid(row=3, column=0, pady=(20, 10), padx=(0, 20), sticky='e')
        self.password_entry.grid(row=4, column=0, columnspan=2, pady=10, padx=10, sticky='w')
        login_button.grid(row=5, column=0, columnspan=2, pady=20)

        sv_ttk.set_theme("dark")

    def check_login(self):
        email = self.username_entry.get()
        password = self.password_entry.get()
        user_id = login(email, password)
        if user_id is not None:
            role = checkRole(email)
            if role == "Admin":
                self.master.change(SecondFrame)
            elif role == "Fitter":
                self.master.change(FitterFrame)
            else:
                messagebox.showerror(title="Error", message="Role not found.")
        else:
            messagebox.showerror(title="Error", message="Invalid login.")


def checkRole(email):
    ref = db.reference("/Users")
    users = ref.get()
    for user_id, user_data in users.items():
        if isinstance(user_data, dict) and user_data.get('email', '') == email:
            return user_data.get('role', '')

class SecondFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        master.title("Admin Forum")
        master.geometry("800x440")

        button_width = 20

        show_users_button = ttk.Button(
            self, text="Show all users", style='TButton', width=button_width, command=show_users_window)
        register_button = ttk.Button(
            self, text="Register a new user", style='TButton', width=button_width,
            command=lambda: self.master.change(RegisterFrame))
        logout_button = ttk.Button(
            self, text="Log out", style='TButton', width=button_width,
            command=lambda: master.destroy())

        show_users_button.grid(row=0, column=0, pady=40)
        register_button.grid(row=1, column=0, pady=40)
        logout_button.grid(row=2, column=0, pady=40)

        self.grid_columnconfigure(0, weight=1)

        sv_ttk.set_theme("dark")

def show_users_window():
    window = tk.Toplevel()
    window.title("User List")
    window.geometry('1920x1080')

    columns = ('name',"lastname", 'Username', 'Email', 'Title', 'Role', 'clinic')
    tree = ttk.Treeview(window, columns=columns, show='headings')

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER)

    tree.pack(fill=tk.BOTH, expand=True)

    scroll_y = ttk.Scrollbar(window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

    scroll_x = ttk.Scrollbar(window, orient=tk.HORIZONTAL, command=tree.xview)
    tree.configure(xscrollcommand=scroll_x.set)
    scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

    ref = db.reference("/Users")
    users = ref.get()
    for user_id, user_data in users.items():
        tree.insert('', tk.END, values=(
            user_data.get('name', ''),
            user_data.get('lastname', ''),
            user_data.get('username', ''),
            user_data.get('email', ''),
            user_data.get('title', ''),
            user_data.get('role', ''),
            user_data.get('additional_field', '')
        ))

    sv_ttk.set_theme("dark")

def login(email: str, password: str):
    user_id = verify_user(email, password)
    return user_id

#a da ovo kao ne radi a msm radi gleda da li email postoji ali petar je rekao da ne mora sifru gledati i nece sifru gledati a ona nece znati da li radi bez sifre
def verify_user(email: str, password: str):
    try:
        user = auth.get_user_by_email(email)
        return user.uid
    except Exception as e:
        print(f'Error verifying user: {e}')
        return None

class RegisterFrame(tk.Frame):
    register_button = None
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        register_label = ttk.Label(self, text="Register", font=("Helvetica", 24))
        name_label = ttk.Label(self, text="First name", font=("Helvetica", 14))
        lastname_label = ttk.Label(self, text="Last name", font=("Helvetica", 14))
        username_label = ttk.Label(self, text="Username", font=("Helvetica", 14))
        email_label = ttk.Label(self, text="Email", font=("Helvetica", 14))
        password_label = ttk.Label(self, text="Password", font=("Helvetica", 14))
        confirm_password_label = ttk.Label(self, text="Confirm Password", font=("Helvetica", 14))
        title_label = ttk.Label(self, text="Title", font=("Helvetica", 14))

        self.name_entry = ttk.Entry(self)
        self.last_entry = ttk.Entry(self)
        self.username_entry = ttk.Entry(self)
        self.email_entry = ttk.Entry(self)
        self.password_entry = ttk.Entry(self, show="*")
        self.confirm_password_entry = ttk.Entry(self, show="*")
        self.title_entry = ttk.Entry(self)

        self.role = tk.StringVar(value="Role 1")

        role_label = ttk.Label(self, text="Role", font=("Helvetica", 14))
        role_checkbox1 = ttk.Checkbutton(self, text="Fitter", variable=self.role, onvalue="Fitter",command=self.toggle_textfield)
        role_checkbox2 = ttk.Checkbutton(self, text="Audiolog", variable=self.role, onvalue="Audiolog", command=self.toggle_textfield)

        self.additional_field_label = ttk.Label(self, text="Clinic", font=("Helvetica", 14))
        options = ["Clinic 1", "Clinic 2", "Clinic 3", "Clinic 4"]
        self.additional_field = ttk.Combobox(self, values=options)

        RegisterFrame.register_button = ttk.Button(self, text="Register", command=self.register_user)

        register_label.grid(row=0, column=0, columnspan=2, pady=20)
        name_label.grid(row=1, column=0, pady=10, padx=10, sticky='e')
        self.name_entry.grid(row=1, column=1, pady=10, sticky='w')
        lastname_label.grid(row=2, column=0, pady=10, padx=10, sticky='e')
        self.last_entry.grid(row=2, column=1, pady=10, sticky='w')
        username_label.grid(row=3, column=0, pady=10, padx=10, sticky='e')
        self.username_entry.grid(row=3, column=1, pady=10, sticky='w')
        email_label.grid(row=4, column=0, pady=10, padx=10, sticky='e')
        self.email_entry.grid(row=4, column=1, pady=10, sticky='w')
        password_label.grid(row=5, column=0, pady=10, padx=10, sticky='e')
        self.password_entry.grid(row=5, column=1, pady=10, sticky='w')
        confirm_password_label.grid(row=6, column=0, pady=10, padx=10, sticky='e')
        self.confirm_password_entry.grid(row=6, column=1, pady=10, sticky='w')
        title_label.grid(row=7, column=0, pady=10, padx=10, sticky='e')
        self.title_entry.grid(row=7, column=1, pady=10, sticky='w')
        role_label.grid(row=8, column=0, pady=10, padx=10, sticky='e')
        role_checkbox1.grid(row=8, column=1, pady=10, sticky='w')
        role_checkbox2.grid(row=8, column=2, pady=10, sticky='w')
        RegisterFrame.register_button.grid(row=9, column=0, columnspan=2, pady=20)

        sv_ttk.set_theme("dark")

        self.grid_rowconfigure(8, minsize=40)

    def toggle_textfield(self):
        if self.role.get() == "Audiolog":
            self.register_button.grid(row=10, column=0, columnspan=2, pady=20)
            self.additional_field_label.grid(row=9, column=0, pady=10, padx=10, sticky='e')
            self.additional_field.grid(row=9, column=1, pady=10, sticky='w')
        else:
            self.register_button.grid(row=9, column=0, columnspan=2, pady=20)
            self.additional_field_label.grid_remove()
            self.additional_field.grid_remove()
    def register_user(self):
        name = self.name_entry.get()
        lastname = self.last_entry.get()
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        title = self.title_entry.get()
        role = self.role.get()
        additional_field = self.additional_field_entry.get() if role == "Audiolog" else None

        if password != confirm_password:
            messagebox.showerror(title="Error", message="Passwords do not match.")
            return

        if register_user(email, password, title, role, username, additional_field,name,lastname) is not None:
            messagebox.showinfo(title="Success", message="User was successfully added.")
            self.master.change(SecondFrame)
        else:
            messagebox.showerror(title="Error", message="User was not added.")

def register_user(email: str, password: str, title: str, role: str, username: str, additional_field: str, name: str,lastname: str):
    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=username
        )

        user_data = {
            'username': username,
            'email': email,
            'name': name,
            'lastname': lastname,
            'title': title,
            'role': role,
            'additional_field': additional_field
        }

        db.reference(f"/Users/{user.uid}").set(user_data)

        return user.uid

    except Exception as e:
        print(f'Error creating new user: {e}')
        return None


class FitterFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        master.title("Fitter Forum")
        master.geometry("800x440")

        button_width = 20

        register_button = ttk.Button(
            self, text="Make an appointment", style='TButton', width=button_width,
            command=lambda: self.master.change(TerminFrame))
        logout_button = ttk.Button(
            self, text="Log out", style='TButton', width=button_width,
            command=lambda: master.destroy())

        register_button.grid(row=1, column=0, pady=40)
        logout_button.grid(row=2, column=0, pady=40)

        self.grid_columnconfigure(0, weight=1)

        sv_ttk.set_theme("dark")


class TerminFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        termin_label = ttk.Label(self, text="Appointment", font=("Helvetica", 24))
        name_label = ttk.Label(self, text="First name ", font=("Helvetica", 14))
        lastname_label = ttk.Label(self, text="Last name", font=("Helvetica", 14))
        name_of_doctor_label = ttk.Label(self, text="Auditor ", font=("Helvetica", 14))

        self.name_entry = ttk.Entry(self)
        self.last_entry = ttk.Entry(self)
        self.name_of_doctor_entry = ttk.Entry(self)
        self.calendar = Calendar(self, selectmode='day', year=datetime.today().year, month=datetime.today().month,
                                 day=datetime.today().day)

        TerminFrame.termin_button = ttk.Button(self, text="Add an appointment", command=self.dodaj_termin)

        termin_label.grid(row=0, column=0, columnspan=2, pady=20)
        name_label.grid(row=1, column=0, pady=10, padx=10, sticky='e')
        self.name_entry.grid(row=1, column=1, pady=10, sticky='w')
        lastname_label.grid(row=2, column=0, pady=10, padx=10, sticky='e')
        self.last_entry.grid(row=2, column=1, pady=10, sticky='w')
        name_of_doctor_label.grid(row=3, column=0, pady=10, padx=10, sticky='e')
        self.name_of_doctor_entry.grid(row=3, column=1, pady=10, sticky='w')
        self.calendar.grid(row=4, column=0, columnspan=2, pady=20)
        TerminFrame.termin_button.grid(row=5, column=0, columnspan=2, pady=20)

        sv_ttk.set_theme("dark")

        self.grid_rowconfigure(8, minsize=40)

    def dodaj_termin(self):
        name = self.name_entry.get()
        lastname = self.last_entry.get()
        doctor = self.name_of_doctor_entry.get()
        date = self.calendar.selection_get()

        if dodaj_termin(doctor, date, name, lastname):
            messagebox.showinfo(title="Success", message="Appointment was successfully added.")
            self.master.change(FitterFrame)
        else:
            messagebox.showerror(title="Error", message="Appointment was not added.")


def dodaj_termin(doctor, date, name, lastname):
    try:
        termin_data = {
            "Datum": str(date),
            "Audiolog": doctor,
            "Ime Pacijenta": name,
            "Prezime Pacijenta": lastname
        }

        db.reference("/Termini").push(termin_data)
        return True

    except Exception as e:
        print(f'Error while making the appointment : {e}')
        return None

class AuditorFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        master.title("Fitter Forum")
        master.geometry("800x440")

        button_width = 20

        register_button = ttk.Button(
            self, text="Make an appointment", style='TButton', width=button_width,
            command=lambda: self.master.change(TerminFrame))
        logout_button = ttk.Button(
            self, text="Log out", style='TButton', width=button_width,
            command=lambda: master.destroy())

        register_button.grid(row=1, column=0, pady=40)
        logout_button.grid(row=2, column=0, pady=40)

        self.grid_columnconfigure(0, weight=1)

        sv_ttk.set_theme("dark")


#pristup kalendaru // fiter
#Doda termin(pregleda) Ime prez klijenta i vreme i koji audiolog
#Ako postoji klijent u bazi onda ponudi se ponudi da se koristi taj klijent

#Audiolog moze da vidi listu klijenata
#kada klikne na klijenta bira slusni aparat i kad odabere slusni aparat  i bira jedan od templateova za slanje mejla