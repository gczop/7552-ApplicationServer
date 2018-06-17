from app import application as app
import unittest
import json
from base64 import b64encode


class InvitationsTestCase(unittest.TestCase):

    def setUp(self):
        # creates a test client
        self.client = app.test_client()
        # propagate the exceptions to the test client
        self.client.testing = True

    def test_1_get_no_invitations(self):
        # Asume userFriends exists
        loginInfo = {
            "username": "userFriends",
            "password": "password"
        };
        info = {
            "username": "userFriends"
        }
        result_login = \
            self.client.post('/api/users/login', data=json.dumps(loginInfo), content_type='application/json')

        token1 = json.loads(result_login.data)["Token"]

        headers1 = { 
            'Authorization': 'Basic %s' % b64encode(bytes(info["username"] + ':' + token1, "utf-8")).decode("ascii"),
            "username": "userFriends"
        }

        result = self.client.get('/api/invitations', headers=headers1 ,data=json.dumps(info), content_type='application/json')
        # Assert a correct get of friends
        print (result.data)
        self.assertEqual(result.status_code, 200)

    def test_2_get_invitation(self):
        # Asume userFriends exists
        loginInfo = {
            "username": "userFriends",
            "password": "password"
        };
        result_login = \
            self.client.post('/api/users/login', data=json.dumps(loginInfo), content_type='application/json')

        loginInfo2 = {
            "username": "user",
            "password": "password"
        };
        result_login2 = \
            self.client.post('/api/users/login', data=json.dumps(loginInfo2), content_type='application/json')


        info = {
            "username": "userFriends",
            "friend": "user"
        };

        friendInfo = { "username": "user"}

        token1 = json.loads(result_login.data)["Token"]
        token2 = json.loads(result_login2.data)["Token"]

        headers1 = {
            'Authorization': 'Basic %s' % b64encode(bytes(info["username"] + ':' + token1, "utf-8")).decode("ascii"),
            "username": "userFriends",
            "friend": "user"
        }
        headers2 = {
            'Authorization': 'Basic %s' % b64encode(bytes(info["friend"] + ':' + token2, "utf-8")).decode("ascii"),
            "username": "user"
        }

        result = self.client.post('/api/invitations', headers=headers1 ,data=json.dumps(info), content_type='application/json')
        # Assert a correct post of the invitation
        dataDict = json.loads(result.data)
        print (dataDict, "\n\n\n")
        self.assertEqual(result.status_code, 200)

        get_result = self.client.get('/api/invitations', headers=headers2 ,data=json.dumps(friendInfo), content_type='application/json')
        # Assert a correct get of invitations
        dataDict = json.loads(get_result.data)
        print (dataDict, "\n\n\n")
        self.assertEqual(get_result.status_code, 200)
        self.assertTrue("userFriends" in dataDict['invitations'])

    def test_3_accept_invitation(self):
        # Asume userFriends exists
        loginInfo = {
            "username": "userFriends",
            "password": "password"
        };
        result_login = \
            self.client.post('/api/users/login', data=json.dumps(loginInfo), content_type='application/json')

        loginInfo2 = {
            "username": "user",
            "password": "password"
        };
        result_login2 = \
            self.client.post('/api/users/login', data=json.dumps(loginInfo2), content_type='application/json')


        info = {
            "username": "userFriends",
            "friend": "user"
        };

        friendInfo = { "username": "user"}

        token1 = json.loads(result_login.data)["Token"]
        token2 = json.loads(result_login2.data)["Token"]

        headers1 = {
            'Authorization': 'Basic %s' % b64encode(bytes(info["username"] + ':' + token1, "utf-8")).decode("ascii"),
            "username": "userFriends",
            "friend": "user"
        }
        headers2 = {
            'Authorization': 'Basic %s' % b64encode(bytes(info["friend"] + ':' + token2, "utf-8")).decode("ascii"),
            "username": "user"
        }

        result = self.client.post('/api/invitations', headers=headers1 ,data=json.dumps(info), content_type='application/json')
        # Assert a correct get of friends
        self.assertEqual(result.status_code, 200)

        get_result = self.client.get('/api/invitations', headers=headers2 ,data=json.dumps(friendInfo), content_type='application/json')
        # Assert a correct get of invitations
        dataDict = json.loads(get_result.data)
        self.assertEqual(get_result.status_code, 200)
        self.assertTrue("userFriends" in dataDict['invitations'])

        accept_info = {
            "friend": "userFriends",
            "username": "user"
        };

        #Accept Invitation
        put_result = self.client.put('/api/invitations', headers=headers2 ,data=json.dumps(accept_info), content_type='application/json')
        self.assertEqual(get_result.status_code, 200)

        result = self.client.get('/api/friends', headers=headers1 ,data=json.dumps(info), content_type='application/json')

        dataDict = json.loads(result.data)
        print (dataDict)
        # Assert a correct get of friends
        self.assertEqual(result.status_code, 200)
        # Assert new friend is in the list
        self.assertTrue("user" in dataDict["friends"])

    def test_4_get_2invitations(self):
        # Asume userFriends exists
        loginInfo = {
            "username": "userFriends",
            "password": "password"
        };
        result_login = \
            self.client.post('/api/users/login', data=json.dumps(loginInfo), content_type='application/json')

        loginInfo2 = {
            "username": "user",
            "password": "password"
        };
        result_login2 = \
            self.client.post('/api/users/login', data=json.dumps(loginInfo2), content_type='application/json')

        loginInfo3 = {
            "username": "user2",
            "password": "password2"
        };
        result_login3 = \
            self.client.post('/api/users/login', data=json.dumps(loginInfo3), content_type='application/json')

        info = {
            "username": "userFriends",
            "friend": "user"
        };
        info2 = {
            "username": "user2",
            "friend": "user"
        };

        friendInfo = { "username": "user"}

        token1 = json.loads(result_login.data)["Token"]
        token2 = json.loads(result_login2.data)["Token"]
        token3 = json.loads(result_login3.data)["Token"]

        headers1 = {
            'Authorization': 'Basic %s' % b64encode(bytes(info["username"] + ':' + token1, "utf-8")).decode("ascii"),
            "username": "userFriends",
            "friend": "user"
        }
        headers2 = {
            'Authorization': 'Basic %s' % b64encode(bytes(info["friend"] + ':' + token2, "utf-8")).decode("ascii"),
            "username": "user"
        }
        headers3 = {
            'Authorization': 'Basic %s' % b64encode(bytes(info2["username"] + ':' + token3, "utf-8")).decode("ascii"),
            "username": "user2",
            "friend": "user"
        }

        result = self.client.post('/api/invitations', headers=headers1 ,data=json.dumps(info), content_type='application/json')
        # Assert a correct post of the invitation
        dataDict = json.loads(result.data)
        print (dataDict, "\n\n\n")
        self.assertEqual(result.status_code, 200)

        result = self.client.post('/api/invitations', headers=headers3 ,data=json.dumps(info2), content_type='application/json')
        # Assert a correct post of the invitation
        dataDict = json.loads(result.data)
        print (dataDict, "\n\n\n")
        self.assertEqual(result.status_code, 200)

        get_result = self.client.get('/api/invitations', headers=headers2 ,data=json.dumps(friendInfo), content_type='application/json')
        # Assert a correct get of invitations
        dataDict = json.loads(get_result.data)
        print (dataDict, "\n\n\n")
        self.assertEqual(get_result.status_code, 200)
        self.assertTrue("userFriends" in dataDict['invitations'])