import os
from app import application as app
import unittest
import tempfile

from werkzeug.contrib.fixers import ProxyFix

class AppServerTestCase(unittest.TestCase):

    app.wsgi_app = ProxyFix(app.wsgi_app)

    def setUp(self):
        # self.db_fd, app.config['StoriesAppServer'] = tempfile.mkstemp()
        #
        # # flaskr.app.testing = True
        # # self.app = flaskr.app.test_client()
        #
        # # creates a test client
        self.app = app.test_client()
        # # propagate the exceptions to the test client
        # self.app.testing = True
        return


    def test_home_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/')

        print (result.data)

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)


    def test_signup_post(self):
        # sends HTTP POST request to the application
        # on the specified path
        print("Reqs to sign up")
        loginInfo = {
            "user": "user",
            "password": "password",
            "fbToken": "fbToken"
        };
        result = self.app.post('/api/users/signup',data=dict(
        user="username",
        password="password"
        ))

        print (result)

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def tearDown(self):

        # os.close(self.db_fd)
        #
        # os.unlink(app.config['StoriesAppServer'])
        return

if __name__ == '__main__':
    unittest.main()