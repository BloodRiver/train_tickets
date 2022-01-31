import os
import sqlite3 as sql
from pprint import pprint
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

DATABASE = os.path.join(settings.BASE_DIR, 'db2.sqlite3')


def create_db_if_not_exists(db_name: str = DATABASE):
    db = sql.connect(os.path.join(settings.BASE_DIR, db_name))
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


def sql_query(query: str, db_name: str = DATABASE) -> list:
    db = sql.connect(os.path.join(settings.BASE_DIR, db_name))
    cursor = db.cursor()

    try:
        cursor.execute(query)
    except sql.Warning:
        results = "err"

    else:
        results = cursor.fetchall()
        db.commit()
        cursor.close()
        db.close()

    return results


if __name__ == "__main__":
    create_db_if_not_exists('test_db.sqlite3')
    print("Database initialized.")
    print()

    while True:
        query = input("Enter your query (-1 to exit): ")

        if query == "-1":
            break
        else:
            pprint(sql_query(query))

    print("Program closed.")
