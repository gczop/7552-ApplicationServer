import os
import app
import unittest
import tempfile

class AppServerTestCase(unittest.TestCase):

    def setUp(self):
        # self.db_fd, Self.app.config['DATABASE'] = tempfile.mkstemp()

        # flaskr.app.testing = True
        # self.app = flaskr.app.test_client()

        # with Self.app.app_context():
        #     Self.init_db()
        return

    def tearDown(self):

        # os.close(self.db_fd)

        # os.unlink(flaskr.app.config['DATABASE'])
        return

if __name__ == '__main__':
    unittest.main()

quit()