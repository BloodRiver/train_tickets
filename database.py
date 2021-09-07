import sqlite3 as sql
# import os
import settings

'''
TRAIN_CHOICES = (
    ("BUL", "Bullet Train"),
)
'''


def create_db_if_not_exists():
    db = sql.connect(settings.DATABASE)
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


class Table(object):
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def sql_query(self, query: str) -> list:
        db = sql.connect(settings.DATABASE)
        cursor = db.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        db.close()

        return results

    def get_all(self, lower_limit: int = 0, upper_limit: int = 20) -> list:

        query = (f"SELECT * FROM `{self.__class__.__name__.lower()}` "
                 + "LIMIT {lower_limit}, {upper_limit}")
        return self.sql_query(query)

    def get_filtered(self, lower_limit: int = 0, upper_limit: int = 20, *args,
                     **kwargs) -> list:

        query = "SELECT *"

        query += f" FROM {self.__class__.__name__.lower()} "
        data = list()

        for k, v in kwargs.items():
            data.append(f"{k} = '{v}'")
        query += "WHERE " + ", ".join(data)
        # results = self.sql_query(query)

        return query


class User(Table):
    id = -1
    first_name = ''
    last_name = ''
    username = ''
    email = ''
    password = ''
    is_admin = False

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


if __name__ == "__main__":
    create_db_if_not_exists()
    print("Database initialized.")
