import firebase_admin
from firebase_admin import credentials, auth, db
from Ui.MainUi import MainApp
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk


def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("resources/ServiceKey.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://mispython-ef4f5-default-rtdb.europe-west1.firebasedatabase.app/'
        })

        return cred


if __name__ == '__main__':
    cred = initialize_firebase()
    app = MainApp()
    app.mainloop()
