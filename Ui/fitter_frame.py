import tkinter as tk
from tkinter import ttk, messagebox
import sv_ttk
from firebase_admin import db
from tkcalendar import Calendar
from datetime import datetime

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
        self.calendar = Calendar(self, selectmode='day', year=datetime.today().year, month=datetime.today().month, day=datetime.today().day)

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

        if self.add_client_to_db(address, date, name, lastname):
            messagebox.showinfo(title="Success", message="Client was successfully added.")
            self.master.change(FitterFrame)
        else:
            messagebox.showerror(title="Error", message="Client was not added.")

    def add_client_to_db(self, address, date, name, lastname):
        try:
            client_data = {
                "Date": str(date),
                "name": name,
                "lastname": lastname,
                "Address": address
            }
            db.reference("/Klijenti").push(client_data)
            return True

        except Exception as e:
            print(f'Error while adding client: {e}')
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
        self.calendar = Calendar(self, selectmode='day', year=datetime.today().year, month=datetime.today().month, day=datetime.today().day)

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

        if self.add_appointment_to_db(doctor, date, time, name, lastname):
            messagebox.showinfo(title="Success", message="Appointment was successfully added.")
            self.master.change(FitterFrame)
        else:
            messagebox.showerror(title="Error", message="Appointment was not added.")

    def add_appointment_to_db(self, doctor, date, time, name, lastname):
        try:
            appointment_data = {
                "Datum": str(date),
                "Audiolog": doctor,
                "Ime Pacijenta": name,
                "Prezime Pacijenta": lastname,
                "Time": str(time)
            }

            db.reference("/Termini").push(appointment_data)
            return True

        except Exception as e:
            print(f'Error while making the appointment: {e}')
            return None
