from app import application as app
import unittest

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

if __name__ == '__main__':
    unittest.main()