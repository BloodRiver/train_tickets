import hashlib
import csv
import os


# constants to use as list indexes for `add_train` and `edit_train`

NAME = 0
PSWD = 1
ADMN = 2

TRAIN_NUM = 0
NUM_COACH = 1
NUM_SEATS = 2
WEEK_DAYN = 3
TIME_ARRI = 4
TIME_DEPA = 5

WEEKDAYS = ("sunday", "monday", "tuesday", "wednesday", "friday",
            "saturday")


# Admin name is Sajeed and password is admin@123 though an admin account can
# be easily created from the users.csv


def create_database_files_if_non_existent() -> None:
    '''
    This function creates the database files if they do not exist in
    the same directory as this program. This helps initialize the
    database files and avoid errors.
    '''

    dirs = os.listdir('.')  # fetch a list of files and directories

    # database_files = {'filename.csv': 2-d tuple for csv file headers}

    database_files = {
        'trains.csv': (
            ('Train Number', 'Number of Coaches', 'Number of Seats',
             'Weekday', 'Train Arrival Time', 'Train Departure Time'
             ),
        ),
        'users.csv': (
            ('Username', 'Password', 'Admin'),
        ),
        'tickets.csv': (
            ('Username', "Train Number"),
        )
    }

    for filename in database_files:
        '''
        For each filename take from the keys of the dictionary
        `database_files` loop the following code:
        '''

        if filename not in dirs:

            '''
            If the filename does not exist in the list of files and
            directories, create a new file with `filename`
            (example: trains.csv) and initialize the files with
            corresponding headers as defined in the `database_files`
            dictionary
            '''

            data = database_files[filename]
            with open(filename, 'w') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerows(data)


def get_data_from_csv(filename: str) -> list:
    '''
    Reads `filename` and returns a 2-D list containing all headers and records
    from the given csv file.
    `filename` must include the .csv extension.
    '''
    try:

        # try to open the file given in `filename`

        csv_file = open(filename, "r")
    except FileNotFoundError:

        # if the file is not found, the data to be returned is "err"
        # indicating that the file has not been found without showing error
        # and without terminating the program.

        data = "err"
    else:
        csv_reader = csv.reader(csv_file)
        data = list()

        # read each row from the csv file and loop the following code
        for row in csv_reader:

            # if current row is not an empty string
            if len(row):

                # if row has greater than or equal to 2 columns
                if len(row) - 1 >= ADMN:

                    # if True or False values are found, change them from
                    # string to boolean.
                    if row[ADMN] == 'True':
                        row[ADMN] = True
                    elif row[ADMN] == "False":
                        row[ADMN] = False
                data.append(row)

    # return the fetched data or 'err'
    return data


def write_to_csv(filename: str, data: list) -> None:
    '''
    Opens the csv file with given `filename` and writes the `data`
    into it. If the file does not exist, it is automatically created.
    '''
    with open(filename, "w") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(data)


def login() -> tuple:
    '''
    The login interface. Checks whether or not username is in database.
    If username exists in database, checks to see if password matches.
    Checks whether or not the user is an admin.
    Finally, returns the `name`, `loggedIn` status and `admin` status
    '''
    loggedIn = False
    admin = False

    name = input("Enter name: ")
    pwd = input("Enter password: ")

    # hashing the password for comparison with the password already stored
    # in the database

    pwd_hash = hashlib.sha256(pwd.encode()).hexdigest()

    users = get_data_from_csv("users.csv")

    # by looping through each user, check to see if username
    # matches any existing user account

    for user in users:
        if name in user:

            # if the hashed password matches with corresponding
            # user's existing hashed password, log the user in

            if pwd_hash == user[PSWD]:
                loggedIn = True

                # According to the database, if the user is an admin,
                # give them admin previliges

                if user[ADMN]:
                    admin = True
                    print(f"Welcome admin {name}!")
                else:
                    print(f"Welcome {name}!")

                # Since matching username and password have been found,
                # there is no need to continue looping so breaking out of
                # the loop to save memory and processing speed.

                break
            else:

                # Else, if password does not match, show error message
                # without terminating the program.

                print("Incorrect password.")

                # If the requested user has been found in the database,
                # there is no need to continue looping and keep the
                #  program busy so breaking out of the for loop to
                #  save memory and processing speed

                break
    else:

        # a Pythonic shortcut to indicate that if the for loop has reached
        # the final loop without breaking in between, then the following code
        # will be executed. In this case, if a user is found in the database,
        # and the password matches, the for loop is broken. If the for loop
        # is not broken and reaches the end, we assume that the username
        # has not been found in the data base so we show error message without
        # terminating the program.

        print("Username does not exist in database.")

    # return a tuple containing the name, loggedIn status and admin status
    return (name, loggedIn, admin)


def int_input(message: str) -> int:
    '''
    Keeps prompting user for an input, displaying `message` until user enters
    an integer.
    '''
    while True:  # infinite loop
        try:

            # output the `message` given as a parameter in the function and
            # take a string input (preferably integer digits) from the user,
            # try to convert it to integer before storing it in `value`

            value = int(input(message))
        except ValueError:

            # if it's not possible to convert the string input to integer,
            # show error message and a blank line without terminating
            # the program and loop again.

            print("Invalid input. Please enter a whole number.")
            print()
        else:

            # if string input from the user has been successfully converted
            # into an integer, break out of the infinite loop.

            break

    # return the value entered by the user
    return value


def time_input(message: str) -> str:
    '''
    Prompts the user to input a time in 24-hour clock (HH:MM) format.
    Keeps looping until time is input in correct format.
    '''
    while True:
        myTime = input(message)

        # if user inputs -1 then return -1 to exit the function
        if myTime == "-1":
            return "-1"

        # if number of characters in `myTime` is exacly 5
        # example -> 04:03
        if len(myTime) == 5:

            # if the colon ":" character exists in `myTime`
            if ":" in myTime:
                try:

                    # try to convert the first 2 characters of `myTime` to
                    # integer. This integer value is the 'hour' part of the
                    # time in 24-hour clock format
                    hours = int(myTime[:2])
                except ValueError:

                    # if we failed to convert the first 2 characters of
                    # `myTime` to integer, show an error message without
                    # terminating the program and loop again
                    print("Invalid input. Hours must be in digits. Did you",
                          "enter something other than a number?")
                    print()
                else:
                    try:

                        # try to convert the last 2 characters of `myTime` to
                        # integer. This integer value is the 'minute' part of
                        # time time in 24-hour clock format
                        mins = int(myTime[3:])
                    except ValueError:

                        # if we failed to convert the last 2 characters of
                        # `myTime` to integer, show an error message without
                        # terminating the program and loop again
                        print("Invalid input. Minutes must be in digits.",
                              "Did you enter something other than a number?")
                        print()
                    else:

                        # if the integer value hours is between 0 and 23
                        # (inclusive)
                        if 0 <= hours <= 23:

                            # if the integer value mins is between 0 and 59
                            # (inclusive)
                            if 0 <= mins <= 59:

                                # return the string input by the user as it
                                # has passed all validation checks
                                return myTime
                            else:

                                # show error message without terminating the
                                # program and loop again
                                print("Invalid input. Minutes must be a 2",
                                      "digit number between 00 and 59")
                                print()
                        else:

                            # show error message without terminating the
                            # program and loop again.
                            print("Invalid input. Hours must be a 2 digit",
                                  "number between 00 and 23")
                            print()
            else:

                # show error message without terminating the program and loop
                # again
                print("Invalid input. Input time must have a colon (:)",
                      "between the hours and minutes (HH:MM")
                print()
        else:

            # show error message without terminating the program and loop again
            print("Invalid input. Try adding zeroes to your input.",
                  "Example: 04:03")
            print()


def time_in_seconds(time: str) -> int:
    '''
    Takes `time` in HH:MM format and returns it in seconds as an integer
    '''

    # convert the first 2 characters of the `time` to integer
    hours = int(time[:2])

    # convert the last 2 characters of the `time` to integer
    minutes = int(time[3:])

    # convert the time to seconds and return the integer value
    return ((hours * 3600) + (minutes * 60))


def show_menu(user: dict) -> int:
    '''
    Displays a menu to the user depending whether or not they are an admin
    '''

    # If user has admin previliges
    if user['admin'] is True:

        # initialize menu options
        menu_options = (
            "1. View train data",
            "2. Add train data",
            "3. Edit train data",
            "4. Delete train data",
            "5. View ticket bookings",
            "6. Logout"
        )
    else:

        # initialize menu options
        menu_options = (
            "1. View available trains",
            "2. Purchase tickets",
            "3. View ticket bookings",
            "4. Cancel booking",
            "5. Logout"
        )

    while True:  # infinite loop

        # keep showing the menu options and asking the user to choose an option

        # the below print statement alone does the work of looping through all
        # the menu options and printing (outputting) them each on a new line
        print('\n'.join(menu_options))

        choice = int_input("Please choose an option: ")

        # if the user has chosen the last option (Logout)
        if choice == len(menu_options):

            # break out of the loop
            break
        else:

            # return the integer value entered by the user
            # as the user's chosen option
            return choice

    # if -1 is returned, in the main menu, the program is terminated
    return -1


def view_train_data(user: dict) -> bool:
    '''
    Fetches records from trains.csv and displays it to the current user.

    This is a main menu function so if it returns False, it will indicate
    that the user has logged out.
    '''
    all_trains = get_data_from_csv("trains.csv")

    # if trains.csv file does not exist or if the file is empty or contains
    # only the header row
    if all_trains == "err" or len(all_trains) < 2:
        print("There are no trains available at the moment. Please try again",
              "later.")
    else:

        # print a horizontal line as a separator for beautified output
        print("_" * 187)

        # loop through each train data record
        for row in all_trains:

            # for each of the data parameters (example: number of seats,
            # number of coaches, arrival time, etc)
            for col in row:

                # The below print statement automatically puts spacing on both
                # sides of the string and puts the value of `col` in the center
                # The spaces are put in both sides to make sure the length of
                # the resultant string is always at least 30. A very useful
                # python shortcut: help(str.format)
                # Also, this print statement does not create a new line.
                print("|{:^30}".format(col), end="")

            # put a vertical bar | character and move to the next line
            print("|")

            # print a horizontal line as a separator for beautified output
            print("_" * 187)

    # return True to indicate that the user is still logged in.
    return True


def add_train_data(user: dict) -> bool:
    '''
    Add a new train data to the trains.csv database.
    Checks to make sure no duplicate entries are being made.
    Also checks to make sure time inputs are corrects.

    In any of the prompts, if the user inputs -1, the process is cancelled,
    new train is not added to the database and user returns to the main menu.

    This is a main menu function so if it returns False, it will indicate that
    the user has logged out.
    '''

    # show the user a list of trains existing in the database
    view_train_data(user)

    all_trains = get_data_from_csv('trains.csv')

    # this variable will be used to auto-increment the serial number of the
    # new train as it is saved in the database.
    num_trains = len(all_trains)
    print("New train number:", num_trains)

    # infinite loop to ensure user inputs correct number of coaches
    while True:
        coaches = int_input("How many coaches in the new train? "
                            "(type -1 to cancel): ")

        # if user enters -1, exit the function
        if coaches == -1:

            # returning True indicates that the user is still logged in
            return True

        # if user inputs 0 or a negative number
        elif coaches < 1:
            print("Invalid input. There must be at least 1 coach"
                  " in each train.")
        else:

            # break out of the infinite loop and proceed to the next steps
            break

    # infinite loop to ensure user inputs correct number of seats
    while True:
        seats_per_coach = int_input("How many seats in each coach? "
                                    "(type -1 to cancel): ")

        # if the user enters -1
        if seats_per_coach == -1:

            # returning True indicates that the user is still logged in
            return True

        # Each coach of the train must have at least 10 seats
        elif seats_per_coach < 10:
            print("Error. there must be at least 10 seats in the coach")
        else:

            # break out of the infinite loop and proceed to the next steps
            break

    # infinite loop to ensure the user inputs the correct weekday
    # (monday, tuesday, Wednesday, etc)
    while True:
        weekday = input("What day of the week is this train "
                        "available?: ")

        # make the first letter of the weekday capital
        # monday -> Monday
        weekday = weekday.capitalize()

        # if the user enters -1
        if weekday == "-1":

            # returning True indicates that the user is still logged in
            return True

        # WEEKDAYS has been initialized to contain names of weekdays
        # convert all characters of the weekday input by the user to check if
        # it exists in WEEKDAYS tuple. If it does not, show error without
        # terminating the program and loop again.
        elif weekday.lower() not in WEEKDAYS:
            print("Invalid input. Please enter a day between",
                  "Sunday to Saturday")
            print()
        else:

            # break out of the infinite loop to proceed with the next steps
            break

    # infinite loop to ensure that the user inputs correct time of arrival
    while True:
        arrival_time = time_input("Please enter time of arrival in"
                                  "  24-hour clock (HH:MM) format: ")

        # if the user inputs -1
        if arrival_time == "-1":

            # returning True indicates that the user is still logged in
            return True

        # loop through each train record
        for row in all_trains:

            # convert the weekday part of the record to lowercase letters
            # for comparison with the weekday entered by the user
            _weekday = row[WEEK_DAYN].lower()
            _time = row[TIME_ARRI]

            # if duplicate entry for arrival time on the same week day has been
            # entered by the user, show error without terminating the program
            # break out of the for loop to indicate that duplicate entry has
            # been found.
            # This is because more than one train can not arrive at the
            # station at the same time because we are assuming there is only
            # one track for the trains to travel
            if arrival_time == _time and weekday.lower() == _weekday:
                print(f"Error. Duplicate arrival time on {weekday}")
                print()

                # break out of the for loop and continue with the infinite loop
                # to get a proper arrival time input by the user
                break
        else:

            # this part of the code is executed if no duplicate entries for
            # arrival time on the same weekday has been found. The below
            # break statement breaks out of the infinite loop to proceed with
            # the next steps.
            break

    # infinite loop to ensure that the user inputs correct time of departure
    while True:
        departure_time = time_input("Please enter time of departure in"
                                    " 24-hour clock (HH:MM) format: ")

        # if the user inputs -1
        if departure_time == "-1":

            # returning True indicates that the user is still logged in
            return True

        # loop through each train record
        for row in all_trains:

            # convert the weekday part of the record to lowercase letters
            # for comparison with the weekday entered by the user
            _weekday = row[WEEK_DAYN].lower()
            _time = row[TIME_DEPA]

            # if duplicate entry for departure time on the same weekday has
            # been entered by the user, show error without terminating the
            # program break out of the for loop to indicate that duplicate
            # entry has been found.
            # This is because more than one train can not depart from the
            # station at the same time because we are assuming there is only
            # one track for the trains to travel
            if departure_time == _time and weekday.lower() == _weekday:
                print(f"Error. Duplicate departure time on {weekday}")
                print()

                # break out of the for loop and continue with the infinite loop
                # to get a proper departure time input by the user
                break
        else:
            # this part of the code is executed if no duplicate entries for
            # arrival time on the same weekday has been found.

            # Arrival time must not be later than the departure time because
            # a train can not depart without arriving first.
            if (time_in_seconds(arrival_time)
                    > time_in_seconds(departure_time)):
                print("Error. Departure time must not be earlier than",
                      "arrival time.")
                print()

            # departure time must not be the same as arrival time
            elif departure_time != arrival_time:

                # add a new record to the train data in the database
                all_trains.append(
                    [num_trains,
                        coaches,
                        seats_per_coach,
                        weekday,
                        arrival_time,
                        departure_time])

                # write the data to the database
                write_to_csv('trains.csv', all_trains)

                # The below break statement breaks out of the infinite loop to
                # proceed with the next steps.
                break
            else:
                print("Error. Departure time must not be the same as",
                      "arrival time.")
                print()

    # returning True indicates that the user is still logged in
    return True


def edit_train_data(user: dict) -> bool:
    '''
    Edit details of existing train data in the database.

    In any of the prompts, if the user inputs -1, the process is cancelled,
    new train data is not changed in the database and user returns to the
    main menu.

    This is a main menu function so if it returns False, it will indicate that
    the user has logged out.
    '''

    all_trains = get_data_from_csv('trains.csv')

    # display a list of existing trains
    view_train_data(user)

    while True:  # infinite loop
        choice = int_input("Which train do you wish to edit?"
                           " (type -1 to cancel editing): ")

        # if user enters -1
        if choice == -1:
            # break out of the infinite loop
            break

        # if user enters a value between 1 and number of existing trains
        # inclusive
        if 1 <= choice <= len(all_trains):
            # infinite loop to ensure user enters valid number of coaches
            while True:
                coaches = int_input("How many coaches? (type -1 to cancel"
                                    " editing): ")

                # if user enters -1
                if coaches == -1:

                    # returning True indicates that the user is still logged in
                    # Also, this breaks out of the function itself, hence
                    # cancelling the editing process
                    return True
                elif coaches < 1:
                    print("Error. There must be at least 1 coach.")
                else:

                    # breaking out of the infinite loop to proceed with the
                    # next steps
                    break

            # infinite loop to ensure user enters valid number of seats
            while True:
                num_seats = int_input("How many seats in the coach? (type -1"
                                      " to cancel editing): ")

                if num_seats == -1:

                    # returning True indicates that the user is still logged in
                    # Also, this breaks out of the function itself, hence
                    # cancelling the editing process
                    return True
                elif num_seats < 10:
                    print("Error. There must be at least 10 seats in each",
                          "coach.")
                else:

                    # breaking out of the infinite loop to proceed with the
                    # next steps
                    break

            # infinite loop to ensure user enters valid weekday
            while True:
                weekday = input("What day of the week is this train"
                                " available?: ")

                weekday = weekday.capitalize()

                if weekday == "-1":

                    # returning True indicates that the user is still logged in
                    # Also, this breaks out of the function itself, hence
                    # cancelling the editing process
                    return True
                elif weekday.lower() not in WEEKDAYS:
                    print("Invalid input. Please enter a day between",
                          "Sunday to Saturday")
                    print()
                else:

                    # breaking out of the infinite loop to proceed with the
                    # next steps
                    break

            # infinite loop to ensure user enters valid arrival time
            while True:
                arrival_time = time_input("Please enter time of arrival in"
                                          "  24-hour clock (HH:MM) format: ")

                if arrival_time == "-1":

                    # returning True indicates that the user is still logged in
                    # Also, this breaks out of the function itself, hence
                    # cancelling the editing process
                    return True

                # loop through all existing train data to check for duplicate
                # arrival time entries on the same weekday
                for row in all_trains:
                    _weekday = row[WEEK_DAYN].lower()
                    _time = row[TIME_ARRI]
                    if arrival_time == _time and weekday.lower() == _weekday:
                        print(f"Error. Duplicate arrival time on {weekday}")
                        print()

                        # if duplicate time has been found, break out of the
                        # for loop
                        break
                else:

                    # if the for loop has not been broken before it could reach
                    # the end,
                    # break out of the infinite loop to proceed with the next
                    # steps
                    break

            # infinite loop to ensure user enters valid departure time
            while True:
                departure_time = time_input("Please enter time of departure in"
                                            " 24-hour clock (HH:MM) format: ")

                if departure_time == "-1":

                    # returning True indicates that the user is still logged in
                    # Also, this breaks out of the function itself, hence
                    # cancelling the editing process
                    return True

                # loop through all existing train data to check for duplicate
                # departure time entries on the same weekday
                for row in all_trains:
                    _weekday = row[WEEK_DAYN].lower()
                    _time = row[TIME_DEPA]
                    if departure_time == _time and weekday.lower() == _weekday:
                        print(f"Error. Duplicate departure time on {weekday}")
                        print()

                        # if duplicate time has been found, break out of the
                        # for loop
                        break
                else:

                    # arrival time must not be later than departure time
                    if (time_in_seconds(arrival_time)
                            > time_in_seconds(departure_time)):
                        print("Error. Departure time must not be earlier than",
                              "arrival time.")
                        print()

                    # departure time must not be same as arrival time
                    elif departure_time != arrival_time:

                        # edit the existing data
                        all_trains[choice][NUM_COACH] = coaches
                        all_trains[choice][NUM_SEATS] = num_seats
                        all_trains[choice][WEEK_DAYN] = weekday
                        all_trains[choice][TIME_ARRI] = arrival_time
                        all_trains[choice][TIME_DEPA] = departure_time

                        # write edited data to database
                        write_to_csv('trains.csv', all_trains)

                        print("Editing complete.")

                        # returning True indicates that the user is still
                        # logged in
                        # Also, this breaks out of the function itself, hence
                        # completing the editing process
                        return True
                    else:
                        print("Error. Departure time must not be the same as",
                              "arrival time.")
                        print()

        else:
            view_train_data(user)
            print()
            print("Invalid choice. Please choose from the numbers shown.")

    # returning True indicates that the user is still logged in
    return True


def delete_train_data(user: dict) -> bool:
    '''
    Allows an admin to delete train data from the csv database
    '''

    all_trains = get_data_from_csv('trains.csv')
    num_trains = len(all_trains) - 1

    view_train_data(user)

    while True:  # infinite loop
        print()  # blank line for better readability

        choice = int_input("Which train do you wish to remove "
                           "from the database? "
                           "(type -1 to cancel): ")

        if choice == -1:
            # returning True indicates that the user is still logged in
            # This breaks out of the function itself, hence cancelling
            # the deletion process.
            return True

        # if user's choice is between 1 and number of trains (inclusive)
        if 1 <= choice <= num_trains:
            all_trains.pop(choice)  # remove train data from the given index

            # re-arrange the serial numbers in the database
            # Example:
            # 1
            # 2
            # 4
            # 5

            # becomes
            # 1
            # 2
            # 3
            # 4

            for x in range(1, len(all_trains)):
                all_trains[x][TRAIN_NUM] = x

            write_to_csv('trains.csv', all_trains)

            print("Selected train has been removed from the database.")
            # returning True indicates that the user is still logged in.
            # Also, this breaks out of the function, hence completing the
            # deletion process.
            return True
        else:
            view_train_data(user)
            print()
            print("Invalid input.",
                  "Please choose a number from the numbers shown.")


def purchase_tickets(user: dict) -> bool:
    '''
    Creates an entry in tickets.csv with username `name` and train number
    chosen by user
    '''

    all_trains = get_data_from_csv("trains.csv")
    while True:  # infinite loop keeps looping until user enters -1
        view_train_data(user)  # display a list of existing trains
        while True:
            choice = int_input("Which train do you wish to book?: ")

            if choice == -1:

                # breaking out of the loop, the function and returning to the
                # main menu. Also, returning True indicates that the user is
                # still logged in
                return True
            elif 1 <= choice <= len(all_trains):
                break
            else:
                view_train_data(user)
                print("Invalid choice. Please choose from the numbers shown.")

        print("You have chosen:")
        print(f"Train number: {choice} that arrives on",
              f"{all_trains[choice][WEEK_DAYN]} at",
              f"{all_trains[choice][TIME_ARRI]}", "and leaves at",
              f"{all_trains[choice][TIME_DEPA]}")

        confirm = input("Are you sure you wish to purchase this ticket?"
                        " (y/n): ")
        confirm = confirm.lower()

        # if the user has confirmed their purchase
        if confirm == "y" or confirm == "yes":

            # if tickets.csv exists in the directory containing this program
            if 'tickets.csv' in os.listdir("."):

                # append the new booking data to the database
                data = [[user['name'], choice]]
                tickets = open("tickets.csv", "a")
            else:

                # since the database file does not exist, we will create
                # the database, initialize it with the headers and at the same
                # time we will add the new train ticket booking data to the
                # database file (.csv)
                data = [
                    ["Username", "Train Number"],
                    [user['name'], choice]
                ]
                tickets = open("tickets.csv", "w")

            writer = csv.writer(tickets)
            writer.writerows(data)

            tickets.close()  # save changes and close the database file

            # break out of the infinite loop and go to the outer infinite
            # loop to let the user decide whether they wish to buy more tickets
            # or exit.
            break

    return True


def get_ticket_data(name: str = '') -> list:
    '''
    Fetch all ticket data from database.

    By default the parameter `name` is an empty string. If no name is passed,
    then this function returns ticket data for all users.
    '''

    all_tickets = get_data_from_csv('tickets.csv')
    all_trains = get_data_from_csv('trains.csv')
    user_tickets = [['Username', 'Train Number', 'Weekday',
                     'Train Arrival Time', 'Train Departure Time']]

    # for each record in all ticket booking data
    for row in all_tickets[1:]:
        current_row = row.copy()

        # for each record in all trains existing in database
        for train in all_trains[1:]:

            # if train data has matched a record from the ticket bookings
            if train[0] == current_row[1]:

                # copy the train data and store it in a variable
                current_train = train.copy()

                # remove the first three columns (train number,
                # number of coaches and number of seats)
                current_train.pop(0)
                current_train.pop(0)
                current_train.pop(0)

                # Append the remaining train data to the current user's data
                current_row.extend(current_train)

                # if no name has been passed in the `name` parameter,
                # all ticket booking data long with corresponding train data
                # is appended to the `user_tickets` variable
                # however, if a name has been passed, only ticket booking
                # data for the specified user name is appended.
                if name == '' or current_row[0] == name:
                    user_tickets.append(current_row)

    # finally return the data that has been fetched and filtered
    return user_tickets


def view_ticket_bookings(user: dict) -> bool:
    '''
    Displays a list of tickets purchased.
    If the `user` is an admin, they are shown all the ticket bookings.
    If the `user` is a customer, they are only shown their own ticket bookings
    '''

    if user['admin']:

        # if user is an admin, fetch all ticket data from the database
        all_tickets = get_ticket_data()
    else:

        # if user is a customer, fetch only ticket data for the customer's
        # username
        all_tickets = get_ticket_data(user['name'])

    # if ticket booking data are found in the database
    # length of all_tickets will be greater than 1(excluding the headers)
    if len(all_tickets) > 1:

        # a horizontal line used to separate outputs
        print("_" * 187)

        # updating the headers to show serial numbers
        # this numbering will be useful when a user wishes to cancel
        # their booking
        headers = ["No."] + all_tickets[0]

        # using python short cuts to loop through each header, put them
        # next to each other with vertical bars | as separators and then moving
        # on to the next line

        # expected output
        # |    No.    |    Username    |   and so on for all the headers
        print((len(headers) * "|{:^30}").format(*headers), end="|\n")

        # a horizontal line used to separate outputs
        print("_" * 187)

        # the enumerate function returns a 2D list that are unpacked
        # to the two variables x and eachTicket
        # the first part of the 2D list contains numbers from 0 to length
        # of the list passed in enumerate.

        # example
        # x = 0, eachTicket = 'ticket data 0'
        # x = 1, eachTicket = 'ticket data 1'
        # therefore, the value of x corresponds to the index number of the
        # eachTicket in the current loop
        for x, eachTicket in enumerate(all_tickets[1:]):

            # using python shortcuts to format the output so that train data
            # columns separated by vertical bars | are output
            # Example output:
            # |    No.    |     Username    |    Train Data    |
            # |     1.    |     Sajeed      |    ..........    |
            print(("|{:^30}".format(x + 1)
                   + (((len(eachTicket)) * "|{:^30}").format(*eachTicket))),
                  end='|\n')  # the end="|\n" means output a | and then move to
            # next line

            # a horizontal line used to separate outputs
            print("_" * 187)
    else:
        print("No purchased tickets.")

    # returning True indicates that the user is still logged in
    return True


def cancel_booking(user: dict) -> bool:
    '''
    Remove entry from tickets.csv
    '''
    view_ticket_bookings(user)
    all_tickets = get_data_from_csv('tickets.csv')
    current_user_tickets = get_ticket_data(user['name'])

    if len(all_tickets):

        while True:  # infinite loop

            cancel_choice = int_input("Which ticket booking do you wish to"
                                      " cancel? (type -1 to exit): ")

            if cancel_choice == -1:
                return True
            elif 1 <= cancel_choice <= len(current_user_tickets):
                cancel_choice -= 1
                all_tickets.pop(
                    all_tickets.index(
                        current_user_tickets[cancel_choice][:2]
                    ))
                write_to_csv('tickets.csv', all_tickets)
                print("Your train ticket booking has been cancelled.")

                # break out of the infinite loop to proceed with the next steps
                break
            else:
                print("Invalid choice. Please choose a number from the",
                      "numbers shown.")
    else:
        print("You have not purchased any tickets.")

    # returning True indicates that the user is still logged in
    return True


def logout(name: str) -> bool:
    '''
    Nothing special. Simply logs user out and closes the program
    '''

    # returning False indicates that the user is no longer logged in
    return False


def main() -> None:
    '''
    The main procedure that links all the above functions to make this whole
    program work
    '''
    loggedIn = False

    # infinite loop to show pre-main menu. Allows user to login, register or
    # exit
    while loggedIn is False:
        print("1. Login\n2. Register\n3. Exit")
        choice = int_input("Choose an option: ")

        if choice == 1:  # login
            name, loggedIn, admin = login()
            user = {'name': name, 'admin': admin}

            # if user has successfully logged in, variable loggedIn becomes
            # True and hence the program breaks out of this infinite loop and
            # enters the next infinite loop down below
        elif choice == 2:  # register
            name = input("Please enter your name: ")
            password = input("Enter a password: ")
            confirm = input("Enter the same password again: ")

            if confirm != password:
                print("Passwords do not match. Please try again.")
            else:

                # hash the password to securely store in the database
                password = hashlib.sha256(password.encode()).hexdigest()

                # username, password, admin status
                data = [
                    [name, password, False]
                ]

                with open("users.csv", "a") as users:
                    writer = csv.writer(users)
                    writer.writerows(data)
        elif choice == 3:
            # break out of the infinite loop with loggedIn = False
            # therefore the program does not enter the next infinite loop
            # for the main menu
            break
        else:
            print("Invalid choice.")

    # storing all the functions that will be called according to the user's
    # choice in tuples. Using a system like this, redundancy can be avoided.
    # Instead of using:
    # if choice < 1 or choice > 6:
    #    # print("Invalid choice")
    # elif choice == 1:
    #    # do something
    # elif choice == 2:
    #    # do something
    # and so on
    # I can simply call the function in the corresponding index as input by
    # the user

    admin_functions = (
        view_train_data,
        add_train_data,
        edit_train_data,
        delete_train_data,
        view_ticket_bookings,
        logout
    )

    functions = (
        view_train_data,
        purchase_tickets,
        view_ticket_bookings,
        cancel_booking,
        logout
    )

    while loggedIn:

        # the show_menu function repeatedly asks the user to choose an option
        # by entering an integer and returns that integer here.
        choice = show_menu(user)

        if choice == -1:

            # if the user enters -1 then the user is logged out, this infinite
            # loop is broken and the program is terminated.
            loggedIn = False
        else:
            if admin is True:

                # if the user is an admin or customer and the choice is
                # between 1 and the number of elements in admin_function
                # tuple, call the function from the tuple according to
                # the choice of the user.
                # Example:
                # If user is admin and inputs 1
                # From `admin_functions` tuple, choice - 1 (1-1 = 0)
                # the function in index 0 of `admin_functions` tuple
                # view_train_data is called with variable`user` passed in
                # as parameter. This is True for all choices made by the user
                # Similarly, the same thing is done for customers as well
                # Therefore, redundancy of if/elif/else blocks is avoided
                if 1 <= choice <= len(admin_functions):
                    loggedIn = admin_functions[choice - 1](user)
            else:
                if 1 <= choice <= len(functions):
                    loggedIn = functions[choice - 1](user)

    print("Program closed. Thank you for using my application.")


if __name__ == "__main__":

    # while executing the program, if this python script is the main
    # module, call the following functions.
    # otherwise, if this python file is imported in another python file
    # example: import train_tickets.py, then the following functions will
    # not be called unless called explicitly in the main module
    # where this module has been imported

    # To avoid FileNotFoundError, initialize database files if they don't
    # exist in the current working directory
    create_database_files_if_non_existent()

    # Enter the main function of this program
    main()
