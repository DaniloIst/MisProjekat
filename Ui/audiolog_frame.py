import tkinter as tk
from tkinter import ttk, messagebox
import sv_ttk
from firebase_admin import db
from tkcalendar import Calendar
from datetime import datetime

class AuditorFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        master.title("Auditor Forum")
        master.geometry("800x440")

        button_width = 20

        appointments_button = ttk.Button(
            self, text="Show all appointments", style='TButton', width=button_width,
            command=lambda: self.show_apoitments_window())
        clients_button = ttk.Button(
            self, text="Show all clients", style='TButton', width=button_width,
            command=lambda: self.show_clients_window(master))
        logout_button = ttk.Button(
            self, text="Log out", style='TButton', width=button_width,
            command=lambda: master.destroy())

        appointments_button.grid(row=1, column=0, pady=40)
        clients_button.grid(row=2, column=0, pady=40)
        logout_button.grid(row=3, column=0, pady=40)

        self.grid_columnconfigure(0, weight=1)

        sv_ttk.set_theme("dark")

    def show_apoitments_window(self):
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

            cal = Calendar(window, selectmode='day', year=datetime.today().year, month=datetime.today().month, day=datetime.today().day)
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

    def show_clients_window(self, master):
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
