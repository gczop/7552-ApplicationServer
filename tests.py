from app import application as app
import unittest
import json


class AppServerTestCase(unittest.TestCase):

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True
        return


    def test_home_status_code(self):
        result = self.app.get('/')

        # Assert the server is running correctly
        self.assertEqual(result.status_code, 200)


    def test_correct_signup_post(self):
        loginInfo = {
            "user": "user",
            "password": "password",
            "fbToken": "fbToken"
        };
        result = self.app.post('/api/users/signup', data=json.dumps(loginInfo), content_type='application/json')

        print (result)

        # Assert a correct sign up
        self.assertEqual(result.status_code, 200)


    def test_signup_post_without_pass_or_fbtoken(self):
        loginInfo = { "user": "user" };
        result = self.app.post('/api/users/signup', data=json.dumps(loginInfo), content_type='application/json')

        # Assert an error from the server
        self.assertNotEqual(result.status_code, 200)



if __name__ == '__main__':
    unittest.main()
