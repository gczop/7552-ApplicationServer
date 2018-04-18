from app import application as app
import unittest
import json

class UserTestCase(unittest.TestCase):

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True


    def test_1_correct_signup_post(self):
        signupInfo = {
            "username": "user",
            "password": "password"
        };
        result = self.app.post('/api/users/signup', data=json.dumps(signupInfo), content_type='application/json')

        print (result)

        # Assert a correct sign up
        self.assertEqual(result.status_code, 200)


    def test_2_signup_post_without_pass_or_fbtoken(self):
        signupInfo = { "username": "user2" };
        result = self.app.post('/api/users/signup', data=json.dumps(signupInfo), content_type='application/json')

        # Assert an error from the server
        # TODO ver que error es el que deberia tirar
        self.assertNotEqual(result.status_code, 200)

    def test_3_signup_and_login(self):
        signupInfo = {
            "username": "user2",
            "password": "password2"
        };
        loginInfo = {
            "username": "user2",
            "password": "password2"
        };
        result_signup = self.app.post('/api/users/signup', data=json.dumps(signupInfo), content_type='application/json')
        self.assertEqual(result_signup.status_code, 200)
        result_login = self.app.post('/api/users/login', data=json.dumps(loginInfo), content_type='application/json')
        self.assertEqual(result_login.status_code, 200)

    def test_4_login_nonexistant_user(self):
        loginInfo = {
            "username": "fakeuser",
            "password": "password"
        };
        result_login = self.app.post('/api/users/login', data=json.dumps(loginInfo), content_type='application/json')
        self.assertNotEqual(result_login.status_code, 200)

    def test_5_login_an_already_registered_user(self):
        loginInfo = {
            "username": "user",
            "password": "password"
        };
        result_login = self.app.post('/api/users/login', data=json.dumps(loginInfo), content_type='application/json')
        self.assertEqual(result_login.status_code, 200)

    def test_6_wrong_pass_login(self):
        loginInfo = {
            "username": "user",
            "password": "wrong_password"
        };
        result_login = self.app.post('/api/users/login', data=json.dumps(loginInfo), content_type='application/json')
        self.assertNotEqual(result_login.status_code, 200)

    def test_7_signup_and_login_with_fbtoken(self):
        signupInfo = {
            "username": "user3",
            "fbToken": "987654321"
        };
        loginInfo = {
            "username": "user3",
            "fbToken": "987654321"
        };
        result_signup = self.app.post('/api/users/signup', data=json.dumps(signupInfo), content_type='application/json')
        self.assertEqual(result_signup.status_code, 200)
        result_login = self.app.post('/api/users/login', data=json.dumps(loginInfo), content_type='application/json')
        self.assertEqual(result_login.status_code, 200)

        dataDict = json.loads(result_login.data)
        print(dataDict["Token"])


if __name__ == '__main__':
    unittest.main()
