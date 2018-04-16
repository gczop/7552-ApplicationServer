#Set Test_Env Var to true
import os
os.environ["TEST_ENV"] = "true"
from app import application as app
import unittest
import json



class AppServerTestCase(unittest.TestCase):

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True


    def test_home_status_code(self):
        result = self.app.get('/')

        # Assert the server is running correctly
        self.assertEqual(result.status_code, 200)


    def test_correct_signup_post(self):
        signupInfo = {
            "username": "user",
            "password": "password"
        };
        result = self.app.post('/api/users/signup', data=json.dumps(signupInfo), content_type='application/json')

        print (result)

        # Assert a correct sign up
        self.assertEqual(result.status_code, 200)


    def test_signup_post_without_pass_or_fbtoken(self):
        signupInfo = { "username": "user2" };
        result = self.app.post('/api/users/signup', data=json.dumps(signupInfo), content_type='application/json')

        # Assert an error from the server
        # TODO ver que error es el que deberia tirar
        self.assertNotEqual(result.status_code, 200)

    def test_signup_and_login(self):
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
        # self.assertEqual(result_login.status_code, 200)


if __name__ == '__main__':
    unittest.main()
