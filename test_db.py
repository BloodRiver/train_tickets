import unittest
import database as db
import os
# from pprint import pprint

# write tests for fetching data from database. Test against SQL injection.
# write tests for inserting data to database. Test against SQL injection.
# write tests for updating data in database. Test against SQL injection.
# write tests for deleting data from database. Test against SQL injection.
TEST_DB = 'test_db.sqlite3'


class DatabaseQueryTest(unittest.TestCase):
    def setUp(self):
        db.create_db_if_not_exists(TEST_DB)
        queries = [
            """
            INSERT INTO user (
                first_name,
                last_name,
                username,
                email,
                password
            )
            VALUES (
                'Sajeed',
                'Ahmed',
                'BloodRiver',
                'email',
                'password'
            );
            """,
            """
            INSERT INTO trains (
                train_type,
                coaches,
                seats,
                rows,
                columns,
                weekday,
                arrival_time,
                departure_time
            )
            VALUES (
                'BUL',
                6,
                50,
                10,
                5,
                'Monday',
                '12:30',
                '13:30'
            );
            """,
            """
            INSERT INTO tickets (
                user_id,
                train_id
            )
            VALUES (
                1,
                1
            );
            """
        ]

        for query in queries:
            db.sql_query(query, TEST_DB)

    def test_queries(self):
        expected_fetch_user_result = [
            (1, 'Sajeed', 'Ahmed', 'BloodRiver', 'email', 'password', 0)
        ]

        fetch_user_query = "SELECT * FROM user WHERE id = 1"
        fetch_user_result = db.sql_query(fetch_user_query, TEST_DB)

        insert_ticket_query = """
        INSERT INTO tickets (
            user_id,
            train_id
        )
        VALUES (
            2,
            2
        );
        """

        db.sql_query(insert_ticket_query, TEST_DB)

        expected_fetch_ticket_result = [
            (2, 2, 2)
        ]

        fetch_ticket_query = "SELECT * FROM tickets WHERE id = 2"
        fetch_ticket_results = db.sql_query(fetch_ticket_query,
                                            TEST_DB)

        update_ticket_query = """
        UPDATE tickets SET user_id = 1, train_id = 1 WHERE id = 2;
        """

        db.sql_query(update_ticket_query, TEST_DB)

        fetch_updated_ticket_query = "SELECT * FROM tickets WHERE id = 2"
        fetch_updated_ticket_results = db.sql_query(
                                        fetch_updated_ticket_query,
                                        TEST_DB)
        expected_updated_ticket_result = [
            (2, 1, 1)
        ]

        self.assertEqual(fetch_user_result, expected_fetch_user_result)
        self.assertEqual(fetch_ticket_results, expected_fetch_ticket_result)
        self.assertEqual(fetch_updated_ticket_results,
                         expected_updated_ticket_result)

        delete_ticket_query = "DELETE FROM tickets WHERE id = 1"
        expected_delete_ticket_result = []

        db.sql_query(delete_ticket_query, TEST_DB)

        fetch_deleted_ticket_query = "SELECT * FROM tickets WHERE id = 1"
        fetch_deleted_ticket_result = db.sql_query(fetch_deleted_ticket_query,
                                                   TEST_DB)

        self.assertEqual(expected_delete_ticket_result,
                         fetch_deleted_ticket_result)


class SqlInjectionTest(unittest.TestCase):
    def setUp(self):
        db.create_db_if_not_exists(TEST_DB)
        queries = [
            """
            INSERT INTO user (
                first_name,
                last_name,
                username,
                email,
                password
            )
            VALUES (
                'Sajeed',
                'Ahmed',
                'BloodRiver',
                'email',
                'password'
            );
            """,
            """
            INSERT INTO trains (
                train_type,
                coaches,
                seats,
                rows,
                columns,
                weekday,
                arrival_time,
                departure_time
            )
            VALUES (
                'BUL',
                6,
                50,
                10,
                5,
                'Monday',
                '12:30',
                '13:30'
            );
            """,
            """
            INSERT INTO tickets (
                user_id,
                train_id
            )
            VALUES (
                1,
                1
            );
            """
        ]

        for query in queries:
            db.sql_query(query, TEST_DB)

    def test_new_user(self):
        first_name = "Sabit"
        last_name = "Abdullah"
        username = "SabAbd"
        email = "email@gmail.com"
        password = ("password'); INSERT INTO user (first_name, last_name,"
                    + " username, email, password) VALUES"
                    + " ('you have', 'been hacked', 'dumbass', "
                    + "'stupid@idiot.com', 'hacker');")

        query = f"""
            INSERT INTO user (
                first_name,
                last_name,
                username,
                email,
                password
            )
            VALUES (
                '{first_name}',
                '{last_name}',
                '{username}',
                '{email}',
                '{password}'
            );
        """

        self.assertEqual(db.sql_query(query, TEST_DB), 'err')


if __name__ == "__main__":
    unittest.main()
    os.remove(os.path.join(os.path.abspath('.'), TEST_DB))
