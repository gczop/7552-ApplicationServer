#Set Test_Env Var to true
import os
os.environ["TEST_ENV"] = "true"
from app import application as app
import unittest
from test import test_users , test_server , test_profile

loader = unittest.TestLoader()
suite  = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(test_server))
suite.addTests(loader.loadTestsFromModule(test_users))
suite.addTests(loader.loadTestsFromModule(test_profile))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)