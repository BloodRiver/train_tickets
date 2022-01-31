# from sqlalchemy import all_
import database as mydb
import tkinter as tk
import tkinter.messagebox as msgbox
import hashlib


class Window(tk.Tk):
    '''
    The root window
    '''
    screens = dict()  # contains names of all the screens

    def __init__(self, *args, **kwargs):
        '''
        '''
        tk.Tk.__init__(self, *args, **kwargs)

    def add_screen(self, screen_name, screen):
        self.screens.update({screen_name: screen})

    def show_screen(self, screen):
        if screen in self.screens:
            for child in self.winfo_children():
                child.destroy()
            currentScreen = self.screens[screen](self)
            return currentScreen
        else:
            print("This screen has not been added to screens dictionary.",
                  "Add this screen using self.add_screen(screen_name)")


class Screen:
    def __init__(self, window, *args, **kwargs):
        self.window = window

        self.pack_headers()

        self.get_data()
        self.show_widgets()

    def pack_headers(self):
        self.header = tk.Label(self.window, text="Train Ticket Booking System",
                               font="Arial 26 bold")

        self.header.pack(anchor=tk.CENTER)

    def get_data(self):
        pass

    def show_widgets(self):
        pass


class MainScreen(Screen):
    def show_widgets(self):
        global user
        user = dict()
        self.login_header = tk.Label(self.window, text="Login",
                                     font="Arial 14 bold")

        self.login_frame = tk.Frame(self.window)
        self.email_label = tk.Label(self.login_frame, text="Email: ",
                                    font="Arial 12")
        self.email_entry = tk.Entry(self.login_frame)

        self.password_label = tk.Label(self.login_frame, text="Password: ",
                                       font="Arial 12")
        self.password_entry = tk.Entry(self.login_frame, show="*")

        self.login_button = tk.Button(self.login_frame, text="Login",
                                      command=self.login)

        self.register_link = tk.Label(
            self.window,
            text="Don't have an account? Click here to register.",
            font="Arial 12 underline",
            cursor="hand2")

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
        global user
        email = self.email_entry.get()
        password = self.password_entry.get()

        query = f"""
            SELECT * FROM user WHERE email='{email}'
        """

        user_details = mydb.sql_query(query)

        if user_details:
            db_password = user_details[0][5]
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            if hashed_password == db_password:
                msgbox.showinfo(TITLE, "Login Successful.")
                user = {
                    'id': user_details[0][0],
                    'first_name': user_details[0][1],
                    'last_name': user_details[0][2],
                    'username': user_details[0][3],
                    'email': user_details[0][4],
                    'is_admin': user_details[0][6]
                }
                self.window.show_screen('menu')
            else:
                msgbox.showerror(TITLE, "Incorrect Password.")
        else:
            msgbox.showerror(TITLE, 'Account does not exist')

    def register(self, event):
        self.window.show_screen('register')


class RegisterScreen(Screen):
    def show_widgets(self):
        self.register_header = tk.Label(self.window, text="Register",
                                        font="Arial 14 bold")

        self.register_frame = tk.Frame(self.window)

        self.fields = (
            {'name': 'first_name', 'type': "text"},
            {'name': 'last_name', 'type': "text"},
            {'name': 'email', 'type': 'email'},
            {'name': 'new_password', 'type': 'password'},
            {'name': 'confirm_password', 'type': 'password'}
        )
        self.register_header.pack(anchor=tk.CENTER)
        self.register_frame.pack(anchor=tk.CENTER)

        row = 0
        for eachField in self.fields:
            new_label = tk.Label(
                self.register_frame,
                text=(eachField['name'].replace("_", " ").title() + ": "),
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

        self.buttonFrame = tk.Frame(self.window)
        self.buttonFrame.pack(anchor=tk.CENTER)
        self.register_button = tk.Button(self.buttonFrame, text='Register',
                                         command=self.register)
        self.back_button = tk.Button(self.buttonFrame, text='Go Back',
                                     command=self.back)

        self.register_button.pack(anchor=tk.CENTER, side=tk.LEFT)
        self.back_button.pack(anchor=tk.CENTER, side=tk.LEFT)

    def register(self):
        password = self.fields[3]['widget'].get()
        password = hashlib.sha256(password.encode()).hexdigest()
        field_data = dict()
        for eachField in self.fields[:3]:
            field_data.update({eachField['name']: eachField['widget'].get()})

        field_data.update(
            {
                'password': password,
                'username': (field_data['first_name'][:3]
                             + field_data['last_name'][:3])
            }
        )

        query = f"""
            INSERT INTO user (
                {', '.join(list(field_data.keys()))}
            )
            VALUES
            (
                {', '.join(list(f"'{x}'" for x in field_data.values()))}
            )
        """

        mydb.sql_query(query)
        msgbox.showinfo(TITLE, "Registration Successful!")
        self.window.show_screen('main')

    def back(self):
        self.window.show_screen('main')


class MenuScreen(Screen):
    def show_widgets(self):
        global user
        self.user_name = tk.Label(
            self.window,
            text=f"Name: {user['username']}",
            font="Arial 12"
        )

        self.user_name.pack(anchor=tk.E)

        self.menu_options = (
            {
                'label': 'View Train Data',
                'funct': self.view_train_data,
                'admin': True
            },

            {
                'label': 'View Ticket Bookings',
                'funct': self.view_ticket_bookings,  # done
                'admin': True
            },

            {
                'label': 'Purchase Tickets',
                'funct': self.purchase_tickets,
                'admin': False
            },

            {
                'label': 'Logout',
                'funct': self.logout,
                'admin': None
            }
        )

        self.menu_frame = tk.Frame(self.window)
        self.menu_frame.pack(anchor=tk.CENTER, expand=True, fill=tk.BOTH)

        for eachOption in self.menu_options:
            if eachOption['admin'] in (None, user['is_admin']):
                new_label = tk.Label(
                    self.menu_frame,
                    font='Arial 12',
                    text=eachOption['label'],
                    cursor="hand2"
                )

                new_label.bind("<Motion>",
                               lambda event: self.mouse_hover(event))
                new_label.bind("<Leave>", lambda event: self.mouse_exit(event))

                new_label.bind("<Button-1>", eachOption['funct'])
                new_label.pack(side=tk.TOP, anchor=tk.CENTER, fill=tk.X)

    def logout(self, event):
        msgbox.showinfo(TITLE, "Thank you for using my app. See you again!")
        self.window.show_screen('main')

    def view_train_data(self, event):
        self.window.show_screen('traindata')

    def view_ticket_bookings(self, event):
        self.window.show_screen('ticketbooking')

    def purchase_tickets(self, event):
        return self.view_train_data(event)

    def mouse_hover(self, event):
        event.widget.config(bg='lightblue')

    def mouse_exit(self, event):
        event.widget.config(bg=self.menu_frame['bg'])


'''
Separate admin and customer Screens
'''


class TrainDataScreen(Screen):
    def get_data(self):
        self.headers = mydb.sql_query("SELECT name FROM pragma_table_info"
                                      + "('trains')")
        self.data = list(mydb.sql_query("SELECT * FROM trains"))

        for x in range(len(self.data)):
            self.data[x] = list(self.data[x])
            for y in range(len(self.data[x])):
                self.data[x][y] = str(self.data[x][y])
            self.data[x] = tuple(self.data[x])
        self.col_count = mydb.sql_query("SELECT COUNT(name) FROM "
                                        + "pragma_table_info('trains')")[0][0]

    '''def show_widgets(self):
        global user
        self.user_name = tk.Label(
            self.window,
            text=f"Name: {user['username']}",
            font="Arial 12"
        )

        self.user_name.pack(anchor=tk.E)

        self.button_frame_right = tk.Frame(self.window)
        self.button_frame_right.pack(anchor=tk.E, fill=tk.X,
                                     expand=True)

        self.back_button = tk.Button(
            self.button_frame_right,
            text="Go Back",
            command=self.back
            )
        self.back_button.pack(side=tk.RIGHT)

        self.update_button = tk.Button(
            self.button_frame_right,
            text='Update in Database',
            command=self.update
        )
        self.update_button.pack(side=tk.RIGHT)
        self.button_frame_left = tk.Frame(self.window)
        self.button_frame_left.pack(anchor=tk.W, fill=tk.X,
                                    expand=True)

        self.add_button = tk.Button(
            self.button_frame_left,
            text='Add',
            command=self.add
        )
        self.add_button.pack(side=tk.LEFT, anchor=tk.W)

        self.add_entry = tk.Entry(self.button_frame_left)
        self.add_entry.insert(0, '0')
        self.add_entry.pack(side=tk.LEFT, anchor=tk.W)

        self.rows_label = tk.Label(
            self.button_frame_left,
            text=' rows',
            font='Arial 12'
        )
        self.rows_label.pack(side=tk.LEFT, anchor=tk.W)

        self.data_frame = tk.Frame(self.window)
        self.data_frame.pack(anchor=tk.NW, expand=True, fill=tk.BOTH)

        for col, eachHeader in enumerate(self.headers):
            eachHeader = " ".join(eachHeader[0].split("_")).title()
            new_label = tk.Label(
                self.data_frame,
                text=eachHeader,
                font="Arial 12"
                )

            new_label.grid(row=0, column=col)

        for row_num, row_data in enumerate(self.data):
            for col_num, col_data in enumerate(row_data):
                new_entry = tk.Entry(self.data_frame)
                new_entry.insert(0, col_data)
                new_entry.grid(row=row_num + 1, column=col_num)

        for data in self.data:
            if sum(list(len(x) for x in data)) < 9:
                self.data.remove(data)'''

    def back(self):
        self.window.show_screen('menu')

    '''def add(self):
        num = int(self.add_entry.get())

        for x in range(len(self.data) + 1, len(self.data) + num + 1):
            self.data.append(tuple(
                [str(x)] + list('' for _ in range(self.col_count - 1))
            ))

        for child in self.window.winfo_children():
            child.destroy()

        super().pack_headers()
        self.show_widgets()

    def update(self):

        entries = list(filter((lambda x: x if type(x) == tk.Entry else None),
                              self.data_frame.winfo_children()))

        entry_data = list(x.get() for x in entries)

        entry_data_2d = list()

        for x in range(0, len(entry_data) + 1, 9):
            data = entry_data[x: x + 9]
            if len(data) == 9:
                if sum(list(len(y) for y in data[1:])) > 7:
                    entry_data_2d.append(tuple(data))

        for old_data, new_data in zip(entry_data_2d, self.data):
            print("old_data:", old_data)
            print("new_data:", new_data)
            print("-" * 80)
        #     # if new_data != old_data:
        #     # update trains set ... = ... where id = ...
        print("-------------------------entry data-----------------------")
        for row in entry_data_2d:
            print(row)

        print(20 * "-" + "new data" + (20 * "-"))
        for new_data in entry_data_2d[len(self.data) - 1:]:
            print(new_data)
            # insert into trains (cols) values (values)

        # msgbox.showinfo(TITLE, "Database updated!")'''


class TicketBookingScreen(Screen):
    def show_widgets(self):
        headers = (
                ('id',),
                ('username',),
                ('train_type',),
                ('weekday',),
                ('arrival_time',),
                ('departure_time',)
            )

        self.data = mydb.sql_query("""
            SELECT
                `tickets`.`id`,
                `user`.`username`,
                `trains`.`train_type`,
                `trains`.`weekday`,
                `trains`.`arrival_time`,
                `trains`.`departure_time`
            FROM
                `tickets`,
                `user`,
                `trains`
            WHERE
                `user`.`id` = `tickets`.`user_id`
            AND
                `trains`.`id` = `tickets`.`train_id`;
        """)

        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack(anchor=tk.E, fill=tk.X, expand=True)

        self.back_button = tk.Button(
            self.button_frame,
            text="Go Back",
            command=self.back
            )
        self.back_button.pack(side=tk.RIGHT)

        self.data_frame = tk.Frame(self.window)
        self.data_frame.pack(anchor=tk.NW, expand=True, fill=tk.BOTH)

        for col, eachHeader in enumerate(headers):
            eachHeader = " ".join(eachHeader[0].split("_")).title()
            new_label = tk.Label(
                self.data_frame,
                text=eachHeader,
                font="Arial 12"
                )

            new_label.grid(row=0, column=col)

        for row_num, row_data in enumerate(self.data):
            for col_num, col_data in enumerate(row_data):
                new_label = tk.Label(
                    self.data_frame,
                    text=col_data,
                    font='Arial 12'
                )
                new_label.grid(row=row_num + 1, column=col_num)
            new_button = tk.Button(
                self.data_frame,
                text='Trip Complete',
                command=lambda num=row_num: self.delete(num=num)
            )
            new_button.grid(row=row_num + 1, column=col_num + 1)

    def back(self):
        self.window.show_screen('menu')

    def delete(self, num):
        global TITLE
        del_id = self.data[num][0]
        print(self.data[num])
        print("id:", del_id)

        if msgbox.askyesno(
                TITLE,
                "Are you sure you wish to delete:\n"
                + f"{'|'.join(list(str(x) for x in self.data[num]))}"
                ):
            query = f"""
                DELETE FROM tickets
                WHERE id = {del_id};
            """

            mydb.sql_query(query)

            msgbox.showinfo(TITLE, "Trip marked as complete!")
            self.window.show_screen('ticketbooking')


if __name__ == "__main__":
    mydb.create_db_if_not_exists()

    TITLE = "Train Ticket Booking System by Sajeed Ahmed Galib Arnob"
    user = dict()

    root = Window()
    root.title(TITLE)
    root.geometry("1000x720")

    '''Automatically add all screens'''
    all_screens = dict(
        tuple(
            filter(
                (lambda x: x if (
                    x[0].endswith("Screen") and len(x[0]) > len("Screen")
                    ) else None), locals().items()
            )
        )
    )

    for k, v in all_screens.items():
        root.add_screen(k, v)

    # enter main loop
    root.show_screen('MainScreen')
    root.mainloop()
