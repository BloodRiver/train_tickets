import hashlib
import csv
import os

NAME = 0
PSWD = 1
ADMN = 2

TRAIN_NUM = 0
NUM_COACH = 1
NUM_SEATS = 2
WEEK_DAYN = 3
TIME_ARRI = 4
TIME_DEPA = 5


# Admin name is Sajeed and password is admin@123


def create_database_files_if_non_existent() -> None:
    '''
    As the name of the function suggests, this function creates the database
    files if they do not exist in the same directory as this program.
    '''

    dirs = os.listdir('.')

    # database_files = {'filename.csv': 2-d list of length 1 for csv file
    #                                                            headers}

    database_files = {
        'trains.csv': [
            ['Train Number', 'Number of Coaches', 'Number of Seats',
             'Weekday', 'Train Arrival Time', 'Train Departure Time'
             ]
        ],
        'users.csv': [
            ['Username', 'Password', 'Admin']
        ],
    }

    for filename in database_files:
        if filename not in dirs:
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
        csv_file = open(filename, "r")
    except FileNotFoundError:
        data = "err"
    else:
        csv_reader = csv.reader(csv_file)
        # initializing list 'data' with the headers from the csv file
        data = list()

        for row in csv_reader:
            if len(row):
                if row[ADMN] == 'True':
                    row[ADMN] = True
                elif row[ADMN] == "False":
                    row[ADMN] = False
                data.append(row)

    return data


def write_to_csv(filename: str, data: list) -> None:
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

    pwd_hash = hashlib.sha256(pwd.encode()).hexdigest()

    users = get_data_from_csv("users.csv")

    for user in users:
        if name in user:
            if pwd_hash == user[PSWD]:
                loggedIn = True
                if user[ADMN]:
                    admin = True
                print("Welcome admin!")
                break
            else:
                print("Incorrect password.")
    else:
        print("Username does not exist in database.")

    return (name, loggedIn, admin)


def int_input(message: str) -> int:
    '''
    Keeps prompting user for an input, displaying `message` until user enters
    an integer.
    '''
    while True:
        try:
            value = int(input(message))
        except ValueError:
            print("Invalid input. Please enter a whole number.")
            print()
        else:
            break

    return value


def time_input(message: str) -> str:
    '''
    Prompts the user to input a time in 24-hour clock (HH:MM) format.
    Keeps looping until time is input in correct format.
    '''
    while True:
        myTime = input(message)

        if myTime == "-1":
            return True

        if len(myTime) == 5:
            if ":" in myTime:
                try:
                    hours = int(myTime[:2])
                except ValueError:
                    print("Invalid input. Hours must be in digits. Did you",
                          "enter something other than a number?")
                    print()
                else:
                    try:
                        mins = int(myTime[3:])
                    except ValueError:
                        print("Invalid input. Minutes must be in digits.",
                              "Did you enter something other than a number?")
                        print()
                    else:
                        if 0 <= hours <= 23:
                            if 0 <= mins <= 59:
                                return myTime
                            else:
                                print("Invalid input. Minutes must be a 2",
                                      "digit number between 00 and 59")
                                print()
                        else:
                            print("Invalid input. Hours must be a 2 digit",
                                  "number between 00 and 23")
                            print()
            else:
                print("Invalid input. Input time must have a colon (:)",
                      "between the hours and minutes (HH:MM")
                print()
        else:
            print("Invalid input. Try adding zeroes to your input.",
                  "Example: 04:03")
            print()


def time_in_seconds(time: str) -> int:
    '''
    Takes `time` in HH:MM format and returns it in seconds as an integer
    '''
    hours = int(time[:2])
    minutes = int(time[3:])

    return ((hours * 3600) + (minutes * 60))


def show_menu(admin: bool) -> int:
    '''
    Displays a menu to the user depending whether or not they are an admin
    '''
    if admin is True:
        menu_options = [
            "1. View train data",
            "2. Add train data",
            "3. Edit train data",
            "4. Delete train data",
            "5. Logout"
        ]
    else:
        menu_options = [
            "1. View available trains",
            "2. Purchase tickets",
            "3. Cancel booking",
            "4. Logout"
        ]

    while True:
        print('\n'.join(menu_options))
        choice = int_input("Please choose an option: ")
        if choice == len(menu_options):
            break
        else:
            return choice

    return -1


def view_train_data(name: str) -> bool:
    '''
    Fetches records from trains.csv and displays it to the current user.
    '''
    all_trains = get_data_from_csv("trains.csv")

    if all_trains == "err" or len(all_trains) < 2:
        print("There are no trains available at the moment. Please try again",
              "later.")
    else:
        print("_" * 187)
        for row in all_trains:
            for col in row:
                print("|{:^30}".format(col), end="")
            print("|")
            print("_" * 187)
    return True


def add_train_data(name: str) -> bool:
    '''
    Add a new train data to the trains.csv database.
    Checks to make sure no duplicate entries are being made.
    Also checks to make sure time inputs are corrects.
    '''
    WEEKDAYS = ["sunday", "monday", "tuesday", "wednesday", "friday",
                "saturday"]

    view_train_data(name)
    all_trains = get_data_from_csv('trains.csv')
    num_trains = len(all_trains)
    print("New train number:", num_trains)

    coaches = int_input("How many coaches in the new train? "
                        "(type -1 to cancel): ")

    if coaches == -1:
        return True
    else:
        seats_per_coach = int_input("How many seats in each coach? "
                                    "(type -1 to cancel): ")

        if seats_per_coach == -1:
            return True

        else:
            while True:
                weekday = input("What day of the week is this train "
                                "available?: ")

                weekday = weekday.capitalize()

                if weekday.lower() not in WEEKDAYS:
                    print("Invalid input. Please enter a day between",
                          "Sunday to Saturday")
                    print()
                elif weekday == "-1":
                    break
                else:
                    break

            if weekday == "-1":
                return True

            while True:
                arrival_time = time_input("Please enter time of arrival in"
                                          "  24-hour clock (HH:MM) format: ")

                if arrival_time == "-1":
                    return True

                for row in all_trains:
                    _weekday = row[WEEK_DAYN].lower()
                    _time = row[TIME_ARRI]
                    if arrival_time == _time and weekday.lower() == _weekday:
                        print(f"Error. Duplicate arrival time on {weekday}")
                        print()
                        break
                else:
                    break

            while True:
                departure_time = time_input("Please enter time of departure in"
                                            " 24-hour clock (HH:MM) format: ")

                if departure_time == "-1":
                    return True

                for row in all_trains:
                    _weekday = row[WEEK_DAYN].lower()
                    _time = row[TIME_DEPA]
                    if departure_time == _time and weekday.lower() == _weekday:
                        print(f"Error. Duplicate departure time on {weekday}")
                        print()
                        break
                else:
                    if (time_in_seconds(arrival_time)
                            > time_in_seconds(departure_time)):
                        print("Error. Departure time must not be earlier than",
                              "arrival time.")
                        print()
                    elif departure_time != arrival_time:
                        all_trains.append(
                            [num_trains,
                             coaches,
                             seats_per_coach,
                             weekday,
                             arrival_time,
                             departure_time])
                        write_to_csv('trains.csv', all_trains)
                        break
                    else:
                        print("Error. Departure time must not be the same as",
                              "arrival time.")
                        print()

    return True


def testFunc(name: str) -> None:
    print("It works!")


def main() -> None:

    while True:
        print("1. Login\n2. Register\n3. Exit")
        choice = int_input("Choose an option: ")

        if choice == 1:
            name, loggedIn, admin = login()
        elif choice == 2:
            pass
        elif choice == 3:
            break
        else:
            print("Invalid choice.")

    admin_functions = [
        view_train_data,
        testFunc
    ]

    functions = [
        view_train_data,
        testFunc
    ]

    while loggedIn:
        choice = show_menu(admin)

        if choice == -1:
            loggedIn = False
        else:
            if admin is True:
                loggedIn = admin_functions[choice - 1](name)
            else:
                loggedIn = functions[choice - 1](name)

    print("Program closed. Thank you for using my app.")


if __name__ == "__main__":
    create_database_files_if_non_existent()
    # main()
    # show_menu(False) is working
    # view_train_data("Sajeed") is working
    # get_data_from_csv(filename) is working
    # write_to_csv(filename) is working

    add_train_data("Sajeed")

    # print(time_in_seconds("05:05"))  is working
    # print(time_in_seconds("05:04"))
