from app import application as app
import unittest
import json
from base64 import b64encode


class ProfileTestCase(unittest.TestCase):

    def setUp(self):
        # creates a test client
        self.client = app.test_client()
        # propagate the exceptions to the test client
        self.client.testing = True


    def test_1_put_user_info(self):
        # with self.client:
        signupInfo = {
            "username": "userProfile",
            "password": "password"
        };
        #result_signup = \
        self.client.post('/api/users/signup', data=json.dumps(signupInfo), content_type='application/json')

        loginInfo = {
            "username": "userProfile",
            "password": "password"
        };
        result_login = \
        self.client.post('/api/users/login', data=json.dumps(loginInfo), content_type='application/json')
        token = json.loads(result_login.data)["Token"]
        profileInfo = {
            "username": "userProfile",
            "personalInformation": {
                "firstname": "User",
                "lastname": "Profile",
                "age": "15"
                }
        }
        headers = {
            'Authorization': 'Basic %s' % b64encode(bytes(signupInfo["username"] + ':' + token, "utf-8")).decode("ascii"),
            'username': 'userProfile'
        }

        result = self.client.put('/api/profile', headers=headers ,data=json.dumps(profileInfo), content_type='application/json')

        dataDict = json.loads(result.data)
        print(dataDict)

        print (result)

        # Assert a correct update of the profile
        self.assertEqual(result.status_code, 200)

    def test_2_get_user_info(self):
        profileInfo = {
            "username": "userProfile"
        }
        headers = {
            'Authorization': 'Basic ' + b64encode(b'userProfile:eTKhUrPGek').decode('utf-8'),
            'username': 'userProfile'
        }

        result = self.client.get('/api/profile', headers=headers ,data=json.dumps(profileInfo), content_type='application/json')

        self.assertEqual(result.status_code, 200)
        dataDict = json.loads(result.data)
        # print(dataDict)
        self.assertEqual(dataDict["age"], "15")

    def test_3_update_user_info(self):
        loginInfo = {
            "username": "userProfile",
            "password": "password"
        };
        result_login = \
        self.client.post('/api/users/login', data=json.dumps(loginInfo), content_type='application/json')
        token = json.loads(result_login.data)["Token"]
        user = {
            "username": "userProfile"
        }
        profileNewInfo = {
            "username": "userProfile",
            "personalInformation": {
                "firstname": "User",
                "lastname": "Profile",
                "age": "25"
            }
        }
        # headers = {'Authorization': 'Basic ' + b64encode(b'userProfile:'+bytes(token)+b').decode('utf-8')}

        headers = { 
            'Authorization': 'Basic %s' % b64encode(bytes(user["username"] + ':' + token, "utf-8")).decode("ascii"),
            'username': 'userProfile'
        }
        result = self.client.put('/api/profile', headers=headers ,data=json.dumps(profileNewInfo), content_type='application/json')
        # Assert a correct update of the profile
        self.assertEqual(result.status_code, 200)

        result = self.client.get('/api/profile', headers=headers ,data=json.dumps(user), content_type='application/json')
        dataDict = json.loads(result.data)
        # Assert correct new info
        self.assertEqual(dataDict["age"], "25")

    def test_4_put_complete_user_info(self):
        # with self.client:
        signupInfo = {
            "username": "userProfile2",
            "password": "password"
        };
        #result_signup = \
        self.client.post('/api/users/signup', data=json.dumps(signupInfo), content_type='application/json')

        loginInfo = {
            "username": "userProfile2",
            "password": "password"
        };
        #result_login = \
        self.client.post('/api/users/login', data=json.dumps(loginInfo), content_type='application/json')
        profileInfo = {
            "username": "userProfile2",
            "personalInformation": {
                "firstname": "User",
                "lastname": "Profile",
                "age": "15",
                "gender": "Male",
                "birthday": "21/05"
            }
        }
        headers = {
            'Authorization': 'Basic ' + b64encode(b'userProfile:eTKhUrPGek').decode('utf-8'),
            'username': 'userProfile2'
        }

        result = self.client.put('/api/profile', headers=headers ,data=json.dumps(profileInfo), content_type='application/json')
        # Assert a correct update of the profile
        self.assertEqual(result.status_code, 200)

        result = self.client.get('/api/profile', headers=headers ,data=json.dumps(signupInfo), content_type='application/json')
        dataDict = json.loads(result.data)
        # Assert correct new info
        self.assertEqual(dataDict["birthday"], "21/05")

if __name__ == '__main__':
    unittest.main()
