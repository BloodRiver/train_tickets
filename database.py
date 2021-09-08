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


def sql_query(query: str) -> list:
    db = sql.connect(os.path.join(settings.BASE_DIR, 'db2.sqlite3'))
    cursor = db.cursor()
    cursor.execute(query)

    results = cursor.fetchall()
    db.commit()
    cursor.close()
    db.close()

    return results


if __name__ == "__main__":
    create_db_if_not_exists()
    print("Database initialized.")

    print(sql_query("SELECT * FROM `user`"))
