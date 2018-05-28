from app import application as app
import unittest
import json
from base64 import b64encode


class StoriesTestCase(unittest.TestCase):

    def setUp(self):
        # creates a test client
        self.client = app.test_client()
        # propagate the exceptions to the test client
        self.client.testing = True

    def test_1_upload_a_reaction(self):
        # Asume user exists
        loginInfo = {
            "username": "user",
            "password": "password"
        };
        result_login = \
            self.client.post('/api/users/login', data=json.dumps(loginInfo), content_type='application/json')

        storyInfo = {
            "username": "user",
            "url": "https://img.buzzfeed.com/buzzfeed-static/static/2016-11/9/10/asset/buzzfeed-prod-fastlane03/sub-buzz-6237-1478707084-5.jpg?downsize=715:*&output-format=auto&output-quality=auto",
            "state": "Public",
            "description": "Esto es una historia"
        };

        token = json.loads(result_login.data)["Token"]

        headers = {
            'Authorization': 'Basic %s' % b64encode(bytes(loginInfo["username"] + ':' + token, "utf-8")).decode("ascii"),
            "username": "user"
        }

        result = self.client.post('/api/stories', headers=headers, data=json.dumps(storyInfo), content_type='application/json')

        dataDict = json.loads(result.data)
        # print (dataDict)
        self.assertEqual(result.status_code,200)

        storyId = dataDict["storyId"];

        headers = {
            'Authorization': 'Basic %s' % b64encode(bytes(loginInfo["username"] + ':' + token, "utf-8")).decode("ascii"),
            "username": "user",
            "story-id": storyId,
            "reaction": "me gusta"
        };
        result = self.client.put('/api/reactions', headers=headers, content_type='application/json')

        dataDict = json.loads(result.data)
        print (dataDict)
        self.assertEqual(result.status_code,200)

    def test_2_get_reactions(self):
        # Asume user exists
        loginInfo = {
            "username": "user",
            "password": "password"
        };
        result_login = \
            self.client.post('/api/users/login', data=json.dumps(loginInfo), content_type='application/json')

        storyInfo = {
            "username": "user",
            "url": "https://img.buzzfeed.com/buzzfeed-static/static/2016-11/9/10/asset/buzzfeed-prod-fastlane03/sub-buzz-6237-1478707084-5.jpg?downsize=715:*&output-format=auto&output-quality=auto",
            "state": "Public",
            "description": "Esto es una historia"
        };

        token = json.loads(result_login.data)["Token"]

        headers = {
            'Authorization': 'Basic %s' % b64encode(bytes(loginInfo["username"] + ':' + token, "utf-8")).decode("ascii"),
            "username": "user"
        }

        result = self.client.post('/api/stories', headers=headers, data=json.dumps(storyInfo), content_type='application/json')

        dataDict = json.loads(result.data)
        # print (dataDict)
        self.assertEqual(result.status_code,200)

        storyId = dataDict["storyId"];

        headers = {
            'Authorization': 'Basic %s' % b64encode(bytes(loginInfo["username"] + ':' + token, "utf-8")).decode("ascii"),
            "username": "user",
            "story-id": storyId,
            "reaction": "me gusta"
        };
        result = self.client.put('/api/reactions', headers=headers, content_type='application/json')

        headers = {
            'Authorization': 'Basic %s' % b64encode(bytes(loginInfo["username"] + ':' + token, "utf-8")).decode("ascii"),
            "username": "user2",
            "story-id": storyId,
            "reaction": "me aburre"
        };
        result = self.client.put('/api/reactions', headers=headers, content_type='application/json')

        headers = {
            'Authorization': 'Basic %s' % b64encode(bytes(loginInfo["username"] + ':' + token, "utf-8")).decode("ascii"),
            "story-id": storyId
        };
        result = self.client.get('/api/reactions', headers=headers, content_type='application/json')

        dataDict = json.loads(result.data)
        print (dataDict)

        self.assertEqual(result.status_code,200)
        self.assertEqual(dataDict,[{'reacter': 'user', 'reaction': 'me gusta'}, {'reacter': 'user2', 'reaction': 'me aburre'}])


    def test_3_delete_reaction(self):
        # Asume user exists
        loginInfo = {
            "username": "user",
            "password": "password"
        };
        result_login = \
            self.client.post('/api/users/login', data=json.dumps(loginInfo), content_type='application/json')

        storyInfo = {
            "username": "user",
            "url": "https://img.buzzfeed.com/buzzfeed-static/static/2016-11/9/10/asset/buzzfeed-prod-fastlane03/sub-buzz-6237-1478707084-5.jpg?downsize=715:*&output-format=auto&output-quality=auto",
            "state": "Public",
            "description": "Esto es una historia"
        };

        token = json.loads(result_login.data)["Token"]

        headers = {
            'Authorization': 'Basic %s' % b64encode(bytes(loginInfo["username"] + ':' + token, "utf-8")).decode("ascii"),
            "username": "user"
        }

        result = self.client.post('/api/stories', headers=headers, data=json.dumps(storyInfo), content_type='application/json')

        dataDict = json.loads(result.data)
        # print (dataDict)
        self.assertEqual(result.status_code,200)

        storyId = dataDict["storyId"];

        headers = {
            'Authorization': 'Basic %s' % b64encode(bytes(loginInfo["username"] + ':' + token, "utf-8")).decode("ascii"),
            "username": "user",
            "story-id": storyId,
            "reaction": "me gusta"
        };
        result = self.client.put('/api/reactions', headers=headers, content_type='application/json')

        headers = {
            'Authorization': 'Basic %s' % b64encode(bytes(loginInfo["username"] + ':' + token, "utf-8")).decode("ascii"),
            "username": "user",
            "story-id": storyId
        };
        result = self.client.delete('/api/reactions', headers=headers, content_type='application/json')

        headers = {
            'Authorization': 'Basic %s' % b64encode(bytes(loginInfo["username"] + ':' + token, "utf-8")).decode("ascii"),
            "story-id": storyId
        };
        result = self.client.get('/api/reactions', headers=headers, content_type='application/json')

        dataDict = json.loads(result.data)
        print (dataDict)

        self.assertEqual(result.status_code,200)
        self.assertEqual(dataDict,[])
