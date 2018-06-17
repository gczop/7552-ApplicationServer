from app import application as app
import unittest
import json
from base64 import b64encode


class FriendsTestCase(unittest.TestCase):

    def setUp(self):
        # creates a test client
        self.client = app.test_client()
        # propagate the exceptions to the test client
        self.client.testing = True


    def test_1_get_empty_friends(self):
        signupInfo = {
            "username": "userFriends",
            "password": "password"
        };
        #result_signup = \
        self.client.post('/api/users/signup', data=json.dumps(signupInfo), content_type='application/json')

        loginInfo = {
            "username": "userFriends",
            "password": "password"
        };
        result_login = \
            self.client.post('/api/users/login', data=json.dumps(loginInfo), content_type='application/json')

        token = json.loads(result_login.data)["Token"]

        headers = { 
            'Authorization': 'Basic %s' % b64encode(bytes(signupInfo["username"] + ':' + token, "utf-8")).decode("ascii"),
            'username': 'userFriends'
        }

        result = self.client.get('/api/friends', headers=headers ,data=json.dumps(loginInfo), content_type='application/json')

        # Assert a correct get of friends
        self.assertEqual(result.status_code, 200)

    def test_2_add_friend(self):
        # Asume userFriends exists
        loginInfo = {
            "username": "userFriends",
            "password": "password"
        };
        result_login = \
            self.client.post('/api/users/login', data=json.dumps(loginInfo), content_type='application/json')

        info = {
            "username": "userFriends",
            "friend": "user"
        };

        token = json.loads(result_login.data)["Token"]

        headers = { 
            'Authorization': 'Basic %s' % b64encode(bytes(info["username"] + ':' + token, "utf-8")).decode("ascii"),
            'username': 'userFriends',
            "friend": "user"
        }

        result = self.client.post('/api/friends', headers=headers ,data=json.dumps(info), content_type='application/json')

        # Assert a correct get of friends
        self.assertEqual(result.status_code, 200)

    def test_3_get_my_new_friend(self):
        # Asume userFriends exists
        info = {
            "username": "userFriends",
            "password": "password"
        };
        result_login = \
            self.client.post('/api/users/login', data=json.dumps(info), content_type='application/json')

        token = json.loads(result_login.data)["Token"]

        headers = { 
            'Authorization': 'Basic %s' % b64encode(bytes(info["username"] + ':' + token, "utf-8")).decode("ascii"),
            'username': 'userFriends'
        }

        result = self.client.get('/api/friends', headers=headers ,data=json.dumps(info), content_type='application/json')

        dataDict = json.loads(result.data)
        print (dataDict)
        # Assert a correct get of friends
        self.assertEqual(result.status_code, 200)
        # Assert new friend is in the list
        self.assertTrue("user" in dataDict["friends"])

    def test_4_remove_my_new_friend(self):
        # Asume userFriends exists
        info = {
            "username": "userFriends",
            "password": "password"
        };

        friendToDelete = {
            "username": "userFriends",
            "friend": "user"
        }

        result_login = \
            self.client.post('/api/users/login', data=json.dumps(info), content_type='application/json')


        token = json.loads(result_login.data)["Token"]

        headers = { 
            'Authorization': 'Basic %s' % b64encode(bytes(info["username"] + ':' + token, "utf-8")).decode("ascii"),
            'username': 'userFriends',
            "friend": "user"
        }

        result = self.client.get('/api/friends', headers=headers ,data=json.dumps(info), content_type='application/json')

        dataDict = json.loads(result.data)
        print (dataDict)

        result = self.client.delete('/api/friends', headers=headers ,data=json.dumps(friendToDelete), content_type='application/json')

        result = self.client.get('/api/friends', headers=headers ,data=json.dumps(info), content_type='application/json')

        dataDict = json.loads(result.data)
        print (dataDict)
        # Assert a correct get of friends
        self.assertEqual(result.status_code, 200)
        # Assert new friend is in the list
        self.assertFalse("user" in dataDict["friends"])

    def test_5_add_a_friend_and_check_his_list(self):
        # Asume userFriends exists
        loginInfo = {
            "username": "userFriends",
            "password": "password"
        };
        result_login = \
            self.client.post('/api/users/login', data=json.dumps(loginInfo), content_type='application/json')

        info = {
            "username": "userFriends",
            "friend": "user"
        };

        token = json.loads(result_login.data)["Token"]

        headers = { 
            'Authorization': 'Basic %s' % b64encode(bytes(info["username"] + ':' + token, "utf-8")).decode("ascii"),
            'username': 'userFriends',
            "friend": "user"
        }

        self.client.post('/api/friends', headers=headers ,data=json.dumps(info), content_type='application/json')

        result = self.client.get('/api/friends/'+ info["friend"] , headers=headers ,data=json.dumps(info), content_type='application/json')

        dataDict = json.loads(result.data)
        print (dataDict)
        # Assert a correct get of friends
        self.assertEqual(result.status_code, 200)
        # Assert I'm in the list
        self.assertTrue("userFriends" in dataDict["friends"])
