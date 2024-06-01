import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox
import sv_ttk
from firebase_admin import credentials, auth, db
from tkcalendar import Calendar
import tkinter as tk
from tktimepicker import AnalogPicker, AnalogThemes, constants


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
        username_label.grid(row=1, column=0, pady=(40,10), padx=(20, 20), sticky='e')
        self.username_entry.grid(row=2, column=0, columnspan=2, pady=(50, 0), padx=(40, 40), sticky='w')
        password_label.grid(row=3, column=0, pady=(20, 10), padx=(20, 20), sticky='e')
        self.password_entry.grid(row=4, column=0, columnspan=2, pady=(30, 10), padx=(40, 40), sticky='w')
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
            elif role == "Auditor":
                self.master.change(AuditorFrame)
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

        self.role = tk.StringVar(value="Role")

        role_label = ttk.Label(self, text="Role", font=("Helvetica", 14))
        role_checkbox1 = ttk.Checkbutton(self, text="Fitter", variable=self.role, onvalue="Fitter",command=self.toggle_textfield)
        role_checkbox2 = ttk.Checkbutton(self, text="Audiolog", variable=self.role, onvalue="Audiolog", command=self.toggle_textfield)

        self.additional_field_label = ttk.Label(self, text="Clinic", font=("Helvetica", 14))
        options = ["Clinic 1", "Clinic 2", "Clinic 3", "Clinic 4"]
        self.additional_field = ttk.Combobox(self, values=options)

        RegisterFrame.register_button = ttk.Button(self, text="Register", command=self.register_user)

        register_label.grid(row=0, column=0, columnspan=2,pady = 30,padx=(50,40))
        name_label.grid(row=1, column=0, pady=10, padx=(20,5), sticky='e')
        self.name_entry.grid(row=1, column=1, pady=10, sticky='w')
        lastname_label.grid(row=2, column=0, pady=10, padx=(20,5), sticky='e')
        self.last_entry.grid(row=2, column=1, pady=10, sticky='w')
        username_label.grid(row=3, column=0, pady=10, padx=(20,5), sticky='e')
        self.username_entry.grid(row=3, column=1, pady=10, sticky='w')
        email_label.grid(row=4, column=0, pady=10, padx=(20,5), sticky='e')
        self.email_entry.grid(row=4, column=1, pady=10, sticky='w')
        password_label.grid(row=5, column=0, pady=10, padx=(20,5), sticky='e')
        self.password_entry.grid(row=5, column=1, pady=10, sticky='w')
        confirm_password_label.grid(row=6, column=0, pady=10, padx=(20,5), sticky='e')
        self.confirm_password_entry.grid(row=6, column=1, pady=10, sticky='w')
        title_label.grid(row=7, column=0, pady=10, padx=(20,5), sticky='e')
        self.title_entry.grid(row=7, column=1, pady=10, sticky='w')
        role_label.grid(row=8, column=0, pady=10, padx=(20,5), sticky='e')
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
        additional_field = self.role.get() if role == "Audiolog" else None

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

        appointment_button = ttk.Button(
            self, text="Make an appointment", style='TButton', width=button_width,
            command=lambda: self.master.change(TerminFrame))
        patient_button = ttk.Button(
            self, text="Enter a client", style='TButton', width=button_width,
            command=lambda: self.master.change(PatientsFrame))
        logout_button = ttk.Button(
            self, text="Log out", style='TButton', width=button_width,
            command=lambda: master.destroy())

        appointment_button.grid(row=1, column=0, pady=40)
        patient_button.grid(row=2, column=0, pady=40)
        logout_button.grid(row=3, column=0, pady=40)

        self.grid_columnconfigure(0, weight=1)

        sv_ttk.set_theme("dark")


class PatientsFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        termin_label = ttk.Label(self, text="Client", font=("Helvetica", 24))
        name_label = ttk.Label(self, text="First name ", font=("Helvetica", 14))
        lastname_label = ttk.Label(self, text="Last name", font=("Helvetica", 14))
        address_label = ttk.Label(self, text="Adress ", font=("Helvetica", 14))
        date_of_birth_label = ttk.Label(self, text="Date of birth ", font=("Helvetica", 14))

        self.name_entry = ttk.Entry(self)
        self.last_entry = ttk.Entry(self)
        self.address_entry = ttk.Entry(self)
        self.calendar = Calendar(self, selectmode='day', year=datetime.today().year, month=datetime.today().month,day=datetime.today().day)

        self.termin_button = ttk.Button(self, text="Add a client", command=self.dodaj_klijenta)

        termin_label.grid(row=0, column=0, columnspan=2, pady=20)
        name_label.grid(row=1, column=0, pady=10, padx=10, sticky='e')
        self.name_entry.grid(row=1, column=1, pady=10, sticky='w')
        lastname_label.grid(row=2, column=0, pady=10, padx=10, sticky='e')
        self.last_entry.grid(row=2, column=1, pady=10, sticky='w')
        address_label.grid(row=3, column=0, pady=10, padx=10, sticky='e')
        self.address_entry.grid(row=3, column=1, pady=10, sticky='w')
        date_of_birth_label.grid(row=4, column=1, pady=10, sticky='w')
        self.calendar.grid(row=5, column=1, columnspan=2, pady=20)

        self.termin_button.grid(row=6, column=0, columnspan=2, pady=20)

        sv_ttk.set_theme("dark")

    def dodaj_klijenta(self):
        name = self.name_entry.get()
        lastname = self.last_entry.get()
        address = self.address_entry.get()
        date = self.calendar.selection_get()

        if dodaj_klijenta(address, date, name, lastname):
            messagebox.showinfo(title="Success", message="Client was successfully added.")
            self.master.change(FitterFrame)
        else:
            messagebox.showerror(title="Error", message="Client was not added.")

def dodaj_klijenta(address,date, name, lastname):
        try:
            termin_data = {
                "Date": str(date),
                "name": name,
                "lastname": lastname,
                "Address": address
            }
            db.reference("/Klijenti").push(termin_data)
            return True

        except Exception as e:
            print(f'Error while making the appointment : {e}')
            return None


class TerminFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        termin_label = ttk.Label(self, text="Appointment", font=("Helvetica", 24))
        name_label = ttk.Label(self, text="First name ", font=("Helvetica", 14))
        lastname_label = ttk.Label(self, text="Last name", font=("Helvetica", 14))
        name_of_doctor_label = ttk.Label(self, text="Audiolog ", font=("Helvetica", 14))

        self.name_entry = ttk.Entry(self)
        self.last_entry = ttk.Entry(self)
        self.name_of_doctor_entry = ttk.Entry(self)
        self.calendar = Calendar(self, selectmode='day', year=datetime.today().year, month=datetime.today().month,day=datetime.today().day)

        hours = [f"{i:02d}" for i in range(1, 13)]
        minutes = ["00", "15", "30", "45"]
        periods = ["AM", "PM"]

        self.hour_combobox = ttk.Combobox(self, values=hours, width=3)
        self.minute_combobox = ttk.Combobox(self, values=minutes, width=3)
        self.period_combobox = ttk.Combobox(self, values=periods, width=3)

        self.hour_combobox.set(hours[0])
        self.minute_combobox.set(minutes[0])
        self.period_combobox.set(periods[0])

        TerminFrame.termin_button = ttk.Button(self, text="Add an appointment", command=self.dodaj_termin)

        termin_label.grid(row=0, column=0, columnspan=2, pady=20)
        name_label.grid(row=1, column=0, pady=10, padx=10, sticky='e')
        self.name_entry.grid(row=1, column=1, pady=10, sticky='w')
        lastname_label.grid(row=2, column=0, pady=10, padx=10, sticky='e')
        self.last_entry.grid(row=2, column=1, pady=10, sticky='w')
        name_of_doctor_label.grid(row=3, column=0, pady=10, padx=10, sticky='e')
        self.name_of_doctor_entry.grid(row=3, column=1, pady=10, sticky='w')
        self.calendar.grid(row=4, column=0, columnspan=2, pady=20)

        time_label = ttk.Label(self, text="Time:")
        time_label.grid(row=5, column=0, pady=10, padx=10, sticky='e')

        self.hour_combobox.grid(row=5, column=1, sticky='w')
        self.minute_combobox.grid(row=5, column=1, padx=(40, 0), sticky='w')
        self.period_combobox.grid(row=5, column=1, padx=(80, 0), sticky='w')

        TerminFrame.termin_button.grid(row=6, column=0, columnspan=2, pady=20)

        sv_ttk.set_theme("dark")


    def dodaj_termin(self):
        name = self.name_entry.get()
        lastname = self.last_entry.get()
        doctor = self.name_of_doctor_entry.get()
        date = self.calendar.selection_get()
        time = f"{self.hour_combobox.get()}:{self.minute_combobox.get()} {self.period_combobox.get()}"

        if dodaj_termin(doctor, date, time, name, lastname):
            messagebox.showinfo(title="Success", message="Appointment was successfully added.")
            self.master.change(FitterFrame)
        else:
            messagebox.showerror(title="Error", message="Appointment was not added.")

def dodaj_termin(doctor, date,time, name, lastname):
    try:
        termin_data = {
            "Datum": str(date),
            "Audiolog": doctor,
            "Ime Pacijenta": name,
            "Prezime Pacijenta": lastname,
            "Time": str(time)
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

        appointments_button = ttk.Button(
            self, text="Show all appointments", style='TButton', width=button_width,
            command=lambda: show_apoitments_window())
        clients_button = ttk.Button(
            self, text="Show all clients", style='TButton', width=button_width,
            command=lambda: show_clients_window(master))
        logout_button = ttk.Button(
            self, text="Log out", style='TButton', width=button_width,
            command=lambda: master.destroy())

        appointments_button.grid(row=1, column=0, pady=40)
        clients_button.grid(row=2, column=0, pady=40)
        logout_button.grid(row=3, column=0, pady=40)

        self.grid_columnconfigure(0, weight=1)

        sv_ttk.set_theme("dark")

def show_apoitments_window():
    window = tk.Toplevel()
    window.title("Appointments List")
    window.geometry('800x600')

    columns = ('First Name', 'Last Name', 'Time', 'Audiolog')
    tree = ttk.Treeview(window, columns=columns, show='headings')
    ref = db.reference("/Termini")
    patients = ref.get()
    if isinstance(patients, dict):
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

        calendar_frame = ttk.Frame(window)
        calendar_frame.pack(pady=10)


        cal = Calendar(window, selectmode='day', year=datetime.today().year, month=datetime.today().month,day=datetime.today().day)
        cal.pack()


        for patient_id, patient_data in patients.items():
            tree.insert('', tk.END, values=(
                patient_data.get('Ime Pacijenta', ''),
                patient_data.get('Prezime Pacijenta', ''),
                patient_data.get('Time', ''),
                patient_data.get('Audiolog', '')
            ))

        sv_ttk.set_theme("dark")
    else:
        messagebox.showerror("Error", "Failed to retrieve data from the database.")


def show_clients_window(master):
    def show_patient_details(event):
        item = tree.selection()[0]
        patient_details = tree.item(item, "values")

        def on_select_dropdown(event):
            selected_option = dropdown_var.get()
            print("Selected Option:", selected_option)

        def on_select_template(event):
            selected_template = template_var.get()
            textbox.delete("1.0", tk.END)
            textbox.insert(tk.END, templates[selected_template])

        popup_window = tk.Toplevel(window)
        popup_window.title("Patient Details")
        popup_window.geometry('400x350')

        for i, detail in enumerate(patient_details):
            ttk.Label(popup_window, text=columns[i]).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            ttk.Label(popup_window, text=detail).grid(row=i, column=1, padx=10, pady=5, sticky="w")

        dropdown_label = ttk.Label(popup_window, text="Select an option:")
        dropdown_label.grid(row=i + 1, column=0, padx=10, pady=5, sticky="w")

        dropdown_options = ["Slusni aparat 1", "Slusni aparat 2", "Slusni aparat 3"]
        dropdown_var = tk.StringVar(popup_window)
        dropdown_var.set(dropdown_options[0])
        dropdown_menu = ttk.Combobox(popup_window, textvariable=dropdown_var, values=dropdown_options)
        dropdown_menu.grid(row=i + 1, column=1, padx=10, pady=5, sticky="w")
        dropdown_menu.bind("<<ComboboxSelected>>", on_select_dropdown)

        template_label = ttk.Label(popup_window, text="Select a template:")
        template_label.grid(row=i + 2, column=0, padx=10, pady=5, sticky="w")

        template_options = ["Template 1", "Template 2", "Template 3"]
        templates = {
            "Template 1": "Tmp1.",
            "Template 2": "Tmp2.",
            "Template 3": "Tmp3."
        }
        template_var = tk.StringVar(popup_window)
        template_var.set(template_options[0])
        template_menu = ttk.Combobox(popup_window, textvariable=template_var, values=template_options)
        template_menu.grid(row=i + 2, column=1, padx=10, pady=5, sticky="w")
        template_menu.bind("<<ComboboxSelected>>", on_select_template)

        textbox = tk.Text(popup_window, height=5, width=40)
        textbox.grid(row=i + 3, column=0, columnspan=2, padx=10, pady=5)
        textbox.insert(tk.END, templates[template_options[0]])

        button = ttk.Button(popup_window, text="Confirm", command=lambda: messagebox.showinfo("Success", "Email sent."))
        button.grid(row=i + 4, column=0, columnspan=2, pady=10)

    window = tk.Toplevel(master)
    window.title("Clients List")
    window.geometry('800x600')

    columns = ('First Name', 'Last Name', 'Address', 'Date-of-Birth')
    tree = ttk.Treeview(window, columns=columns, show='headings')
    ref = db.reference("/Klijenti")
    patients = ref.get()
    if isinstance(patients, dict):
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

        for patient_id, patient_data in patients.items():
            tree.insert('', tk.END, values=(
                patient_data.get('name', ''),
                patient_data.get('lastname', ''),
                patient_data.get('Address', ''),
                patient_data.get('Date', '')
            ))

        tree.bind("<Double-1>", show_patient_details)

        sv_ttk.set_theme("dark")
    else:
        messagebox.showerror("Error", "Failed to retrieve data from the database.")


#pristup kalendaru // fiter
#Doda termin(pregleda) Ime prez klijenta i vreme i koji audiolog
#Todo Ako postoji klijent u bazi onda ponudi se ponudi da se koristi taj klijent

#Audiolog moze da vidi listu klijenata
#kada klikne na klijenta bira slusni aparat i kad odabere slusni aparat  i bira jedan od templateova za slanje mejla

#ToDo mene je malko mrzelo u momentu ali slobodno rasporedite klase u odvojene fajlove