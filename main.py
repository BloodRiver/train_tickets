import database as mydb
import tkinter as tk

TITLE = "Train Ticket Booking System by Sajeed Ahmed Galib Arnob"


class Window(tk.Tk):
    screens = dict()

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

    def add_screen(self, screen_name, screen):
        self.screens.update({screen_name: screen})

    def show_screen(self, screen):
        if screen in self.screens:
            currentScreen = self.screens[screen](self)
            return currentScreen
        else:
            print("This screen has not been added to screens dictionary.",
                  "Add this screen using self.add_screen(screen_name)")


class MainScreen:
    def __init__(self, window):

        self.window = window

        # creating the widgets
        self.header = tk.Label(window, text="Train Ticket Booking System",
                               font="Arial 26 bold")

        self.login_header = tk.Label(window, text="Login",
                                     font="Arial 14 bold")

        self.login_frame = tk.Frame(window)
        self.email_label = tk.Label(self.login_frame, text="Email: ",
                                    font="Arial 12")
        self.email_entry = tk.Entry(self.login_frame)

        self.password_label = tk.Label(self.login_frame, text="Password: ",
                                       font="Arial 12")
        self.password_entry = tk.Entry(self.login_frame, show="*")

        self.login_button = tk.Button(self.login_frame, text="Login",
                                      command=self.login)

        self.register_link = tk.Label(
            window,
            text="Don't have an account? Click here to register.",
            font="Arial 12 underline",
            cursor="hand2")

        # placing the widgets

        self.header.pack(anchor=tk.CENTER)
        self.login_header.pack(anchor=tk.CENTER)
        self.login_frame.pack(anchor=tk.CENTER)

        self.email_label.grid(row=0, column=0)
        self.password_label.grid(row=1, column=0)

        self.email_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)

        self.login_button.grid(row=2, columnspan=2)

        self.register_link.pack(anchor=tk.CENTER)

        # event bindings
        self.register_link.bind("<Button-1>", lambda e: self.register(e))

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        print(f"email: {email}\npassword: {password}")

    def register(self, event):
        for child in self.window.winfo_children():
            child.pack_forget()

        self.window.show_screen('register')


class RegisterScreen:
    def __init__(self, window):
        # creating the widgets
        self.header = tk.Label(window, text="Train Ticket Booking System",
                               font="Arial 26 bold")

        self.login_header = tk.Label(window, text="Register",
                                     font="Arial 14 bold")

        self.register_frame = tk.Frame(window)

        self.fields = (
            {'name': 'First Name', 'type': "text"},
            {'name': 'Last Name', 'type': "text"},
            {'name': 'Email', 'type': 'email'},
            {'name': 'New Password', 'type': 'password'},
            {'name': 'Confirm Password', 'type': 'password'}
        )

        # placing the widgets

        self.header.pack(anchor=tk.CENTER)
        self.login_header.pack(anchor=tk.CENTER)
        self.register_frame.pack(anchor=tk.CENTER)

        row = 0
        for eachField in self.fields:
            new_label = tk.Label(
                self.register_frame,
                text=eachField['name'] + ": ",
                font="Arial 12"
                )
            new_label.grid(row=row, column=0)

            new_entry = tk.Entry(
                self.register_frame,
                show="*" if eachField['type'] == 'password' else ''
            )

            new_entry.grid(row=row, column=1)

            eachField.update({'widget': new_entry})

            row += 1

        self.test_button = tk.Button(window, text='Test', command=self.test)
        self.test_button.pack(anchor=tk.CENTER)

    def test(self):
        for eachField in self.fields:
            print(f"{eachField['name']}: {eachField['widget'].get()}")


mydb.create_db_if_not_exists()

root = Window()
root.title(TITLE)
root.geometry("640x480")

# Adding screens
root.add_screen('main', MainScreen)
root.add_screen('register', RegisterScreen)

root.show_screen('main')
root.mainloop()
