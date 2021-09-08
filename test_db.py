import unittest
import database as db


class UserTest(unittest.TestCase):
    def test_get_all(self):
        all_users = db.User().get_all()

        '''for eachUser in all_users:
            print(f"ID: {eachUser.id}")
            print(f"First Name: {eachUser.first_name}")
            print(f"Last Name: {eachUser.last_name}")
            print(f"Username: {eachUser.username}")
            print(f"Email: {eachUser.email}")
            print(f"Password: {eachUser.password}")
            print(f"Admin: {eachUser.is_admin}")
            print(80 * "-")'''

    def get_test(self):
        new_user = db.User()

        print(new_user.get(username="BloodRiver",
                                    email="email"))


if __name__ == "__main__":
    unittest.main()
