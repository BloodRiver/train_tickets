import os
import sqlite3 as sql

import settings

'''
TRAIN_CHOICES = (
    ("BUL", "Bullet Train"),
)
'''

"""
CREATE TABLE IF NOT EXISTS `user` (
    -- Data Access
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,

    -- User Info
    `first_name` varchar(200) NOT NULL,
    `last_name`  varchar(200) NOT NULL,
    `username`   varchar(100) NOT NULL,
    `email`      varchar(100) NOT NULL,
    `password`   varchar(200) NOT NULL,

    -- Permission
    `is_admin`   BOOLEAN NOT NULL DEFAULT 0
);
""",
"""
CREATE TABLE IF NOT EXISTS `trains` (
    -- Data Access
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Train Info
    `train_type`,
    `coaches`        INTEGER NOT NULL,
    `seats`          INTEGER NOT NULL,
    `rows`           INTEGER NOT NULL,
    `columns`        INTEGER NOT NULL,
    `weekday`        varchar(30) NOT NULL,
    `arrival_time`   varchar(5) NOT NULL,
    `departure_time` varchar(5) NOT NULL
);
""",
"""
CREATE TABLE IF NOT EXISTS `tickets` (
    -- Data Access
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,

    -- User ID
    `user_id`  INTEGER NOT NULL,
    `train_id` INTEGER NOT NULL
);
"""

DO_NOTHING = 0
PROTECT = 1
CASCADE = 2
SET_DEFAULT = 3
SET_NULL = 4


def create_db_if_not_exists():
    db = sql.connect(os.path.join(settings.BASE_DIR, "db2.sqlite3"))
    cursor = db.cursor()

    queries = [
        """
        CREATE TABLE IF NOT EXISTS `user` (
            -- Data Access
            `id` INTEGER PRIMARY KEY AUTOINCREMENT,

            -- User Info
            `first_name` varchar(200) NOT NULL,
            `last_name`  varchar(200) NOT NULL,
            `username`   varchar(100) NOT NULL,
            `email`      varchar(100) NOT NULL,
            `password`   varchar(200) NOT NULL,

            -- Permission
            `is_admin`   BOOLEAN NOT NULL DEFAULT 0
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS `trains` (
            -- Data Access
            `id` INTEGER PRIMARY KEY AUTOINCREMENT,

            -- Train Info
            `train_type`,
            `coaches`        INTEGER NOT NULL,
            `seats`          INTEGER NOT NULL,
            `rows`           INTEGER NOT NULL,
            `columns`        INTEGER NOT NULL,
            `weekday`        varchar(30) NOT NULL,
            `arrival_time`   varchar(5) NOT NULL,
            `departure_time` varchar(5) NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS `tickets` (
            -- Data Access
            `id` INTEGER PRIMARY KEY AUTOINCREMENT,

            -- User ID
            `user_id`  INTEGER NOT NULL,
            `train_id` INTEGER NOT NULL
        );
        """
    ]

    for eachQuery in queries:
        cursor.execute(eachQuery)

    db.commit()
    cursor.close()
    db.close()


class Field(object):
    pass


class CharField(Field):
    value = None

    def __init__(self, max_length: int, null: bool = False,
                 blank: bool = False, *args, **kwargs):
        pass


class IntegerField(Field):
    pass


class BooleanField(Field):
    pass


class EmailField(Field):
    pass


class PasswordField(Field):
    pass


class TimeField(Field):
    pass


class ForeignKey(IntegerField):
    pass


class TableManager(object):
    pass


class Table(object):
    objects = TableManager()

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def sql_query(self, query: str) -> list:
        db = sql.connect(os.path.join(settings.BASE_DIR, 'db2.sqlite3'))
        cursor = db.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        db.commit()
        cursor.close()
        db.close()

        return results

    def get_all(self, lower_limit: int = 0, upper_limit: int = 20) -> list:

        query = (f"SELECT * FROM `{self.__class__.__name__.lower()}` "
                 + f"LIMIT {lower_limit}, {upper_limit}")
        results = self.sql_query(query)
        objects = list()
        data = dict()
        print(dir(self))
        '''for eachResult in results:
            for k, v in zip(self.__dict__.keys(), eachResult):
                print(f"k: {k}, v: {v}")
                data.update({k: v})

            objects.append(self.__class__(**data))

        return objects'''

    def get(self, lower_limit: int = 0, upper_limit: int = 20, *args,
            **kwargs) -> list:

        query = "SELECT *"

        query += f" FROM {self.__class__.__name__.lower()} "
        data = list()

        for k, v in kwargs.items():
            data.append(f"{k} = '{v}'")
        query += "WHERE " + " AND ".join(data)
        query += " LIMIT 1"
        results = self.sql_query(query)

        return results

    def save(self):
        table_name = self.__class__.__name__.lower()
        id = self.__getattribute__('id')
        result = self.sql_query(f"SELECT `id` FROM `{table_name}`"
                                + f"WHERE `id` = {id}")

        data = list()
        for k, v in self.__dict__.items():
            data.append(f"{k} = '{str(v)}'")
        if result:
            query = f"UPDATE {table_name} SET " + ", ".join(data)
        else:
            fields = list(self.__dict__.keys())
            values = list()

            for value in self.__dict__.values():
                values.append(f"'{str(value)}'")

            query = (f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES "
                     + f"({', '.join(values)})"
                     )

        self.sql_query(query)

        return self


class User(Table):
    first_name = CharField(max_length=200)
    last_name = CharField(max_length=200)
    username = CharField(max_length=200)
    email = EmailField()
    password = PasswordField()
    is_admin = BooleanField()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Train(Table):
    TRAIN_TYPES = (
        ('BUL', "Bullet Train"),
    )
    WEEKDAY_CHOICES = (
        ('SUN', "Sunday"),
        ('MON', "Monday"),
        ('TUE', "Tuesday"),
        ('WED', "Wednesday"),
        ('THU', "Thursday"),
        ('FRI', "Friday"),
        ('SAT', "Saturday")
    )
    train_type = CharField(max_length=3)
    coaches = IntegerField()
    seats = IntegerField()
    rows = IntegerField()
    columns = IntegerField()
    weekday = CharField(max_length=3)
    arrival_time = TimeField(auto_now=False)
    departure_time = TimeField(auto_now=False)

    def __str__(self) -> str:
        return dict(self.TRAIN_TYPES)[self.train_type]


class Ticket(Table):
    user_id = ForeignKey(User, on_delete=PROTECT)
    train_id = ForeignKey(Train)

    def __str__(self) -> str:
        return f"Ticket No. {self.id}"


if __name__ == "__main__":
    create_db_if_not_exists()
    print("Database initialized.")
