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

    def test_1_upload_a_story(self):
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

        headers = { 'Authorization': 'Basic %s' % b64encode(bytes(loginInfo["username"] + ':' + token, "utf-8")).decode("ascii")}

        result = self.client.post('/api/stories', headers=headers, data=json.dumps(storyInfo), content_type='application/json')

        dataDict = json.loads(result.data)
        print (dataDict)
        self.assertEqual(result.status_code,200)

    def test_2_get_my_story(self):
        # Asume user exists
        loginInfo = {
            "username": "user",
            "password": "password"
        };
        info = {
            "username": "user"
        };
        result_login = \
            self.client.post('/api/users/login', data=json.dumps(loginInfo), content_type='application/json')

        token = json.loads(result_login.data)["Token"]

        headers = { 'Authorization': 'Basic %s' % b64encode(bytes(loginInfo["username"] + ':' + token, "utf-8")).decode("ascii")}

        result = self.client.get('/api/stories', headers=headers, data=json.dumps(info), content_type='application/json')

        dataDict = json.loads(result.data)
        print ("Historiass:\n",dataDict)
        self.assertEqual(result.status_code,200)
        self.assertTrue(dataDict) # is not Empty


    def test_3_get_my_friends_story(self):
        # Asume userFriends exists and is friends with user
        loginInfo = {
            "username": "userFriends",
            "password": "password"
        };
        info = {
            "username": "userFriends"
        };
        result_login = \
            self.client.post('/api/users/login', data=json.dumps(loginInfo), content_type='application/json')

        token = json.loads(result_login.data)["Token"]

        headers = { 'Authorization': 'Basic %s' % b64encode(bytes(loginInfo["username"] + ':' + token, "utf-8")).decode("ascii")}

        result = self.client.get('/api/stories', headers=headers, data=json.dumps(info), content_type='application/json')

        dataDict = json.loads(result.data)
        print ("Historias:\n",dataDict)
        self.assertEqual(result.status_code,200)
        self.assertTrue(dataDict) # is not Empty

    def test_4_update_my_story(self):
        # Asume user exists
        loginInfo = {
            "username": "user",
            "password": "password"
        };
        info = {
            "username": "user"
        };
        result_login = \
            self.client.post('/api/users/login', data=json.dumps(loginInfo), content_type='application/json')

        token = json.loads(result_login.data)["Token"]

        headers = { 'Authorization': 'Basic %s' % b64encode(bytes(loginInfo["username"] + ':' + token, "utf-8")).decode("ascii")}

        result = self.client.get('/api/stories', headers=headers, data=json.dumps(info), content_type='application/json')
        dataDict = json.loads(result.data)
        id = dataDict["_id"]
        # print ("\n\nHistoria ID: ",id)
        updatedInfo = {
            "username": "user",
            "id": id,
            "description": "Nueva descripcion"
        }

        result_update = self.client.put('/api/stories', headers=headers, data=json.dumps(updatedInfo), content_type='application/json')

        self.assertEqual(result_update.status_code,200)

        result = self.client.get('/api/stories', headers=headers, data=json.dumps(info), content_type='application/json')
        dataDict = json.loads(result.data)
        print (dataDict)
        description = dataDict["storyDetail"]["description"]
        self.assertEqual(result.status_code,200)
        self.assertEqual(description,"Nueva descripcion")

    def test_5_delete_my_story(self):
        # Asume user exists
        loginInfo = {
            "username": "user",
            "password": "password"
        };
        info = {
            "username": "user"
        };
        result_login = \
            self.client.post('/api/users/login', data=json.dumps(loginInfo), content_type='application/json')

        token = json.loads(result_login.data)["Token"]

        headers = { 'Authorization': 'Basic %s' % b64encode(bytes(loginInfo["username"] + ':' + token, "utf-8")).decode("ascii")}

        result = self.client.get('/api/stories', headers=headers, data=json.dumps(info), content_type='application/json')

        dataDict = json.loads(result.data)
        id = dataDict["_id"]
        print ("\n\nHistoria ID: ",id)
        self.assertEqual(result.status_code,200)
        self.assertTrue(dataDict) # is not Empty

        result = self.client.delete('/api/stories', headers=headers, data=json.dumps({"id":id}), content_type='application/json')

        self.assertEqual(result.status_code,200)