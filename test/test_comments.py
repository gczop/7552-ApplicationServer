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

    def test_1_upload_a_comment(self):
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
            "story-id": storyId
        };
        commentInfo = {
            "comment": "Ese meme si se puede ver"
        };
        result = self.client.put('/api/comments', headers=headers, data=json.dumps(commentInfo), content_type='application/json')

        dataDict = json.loads(result.data)
        # print (dataDict)
        self.assertEqual(result.status_code,200)

    def test_2_get_a_comment(self):
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
            "story-id": storyId
        };
        commentInfo = {
            "comment": "Ese meme si se puede ver"
        };
        result = self.client.put('/api/comments', headers=headers, data=json.dumps(commentInfo), content_type='application/json')

        dataDict = json.loads(result.data)
        # print (dataDict)
        self.assertEqual(result.status_code,200)

        headers = {
            'Authorization': 'Basic %s' % b64encode(bytes(loginInfo["username"] + ':' + token, "utf-8")).decode("ascii"),
            "story-id": storyId
        };

        result = self.client.get('/api/comments', headers=headers, data=json.dumps(commentInfo), content_type='application/json')
        dataDict = json.loads(result.data)
        # print (dataDict)
        comment = dataDict["comments"][0]["message"]
        # print (comment)
        self.assertEqual(result.status_code,200)
        self.assertEqual(comment,"Ese meme si se puede ver")

    def test_3_get_two_comments(self):
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
            "story-id": storyId
        };
        commentInfo = {
            "comment": "Ese meme si se puede ver"
        };
        result = self.client.put('/api/comments', headers=headers, data=json.dumps(commentInfo), content_type='application/json')

        commentInfo = {
            "comment": "Buzzfeed es muy normie"
        };
        result = self.client.put('/api/comments', headers=headers, data=json.dumps(commentInfo), content_type='application/json')

        dataDict = json.loads(result.data)
        # print (dataDict)
        self.assertEqual(result.status_code,200)

        headers = {
            'Authorization': 'Basic %s' % b64encode(bytes(loginInfo["username"] + ':' + token, "utf-8")).decode("ascii"),
            "story-id": storyId
        };

        result = self.client.get('/api/comments', headers=headers, data=json.dumps(commentInfo), content_type='application/json')
        dataDict = json.loads(result.data)
        # print (dataDict)
        comment1 = dataDict["comments"][0]["message"]
        comment2 = dataDict["comments"][1]["message"]
        # print (comment)
        self.assertEqual(result.status_code,200)
        self.assertEqual(comment1,"Buzzfeed es muy normie")
        self.assertEqual(comment2,"Ese meme si se puede ver")

    def test_4_delete_comment(self):
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
            "story-id": storyId
        };
        commentInfo = {
            "comment": "Ese meme si se puede ver"
        };
        result = self.client.put('/api/comments', headers=headers, data=json.dumps(commentInfo), content_type='application/json')

        dataDict = json.loads(result.data)
        print (dataDict)
        id = dataDict["id"]
        self.assertEqual(result.status_code,200)

        headers = {
            'Authorization': 'Basic %s' % b64encode(bytes(loginInfo["username"] + ':' + token, "utf-8")).decode("ascii"),
            "story-id": storyId,
            "comment-id": id
        };

        result = self.client.delete('/api/comments', headers=headers, data=json.dumps(commentInfo), content_type='application/json')
        dataDict = json.loads(result.data)

        headers = {
            'Authorization': 'Basic %s' % b64encode(bytes(loginInfo["username"] + ':' + token, "utf-8")).decode("ascii"),
            "story-id": storyId
        };

        result = self.client.get('/api/comments', headers=headers, data=json.dumps(commentInfo), content_type='application/json')
        dataDict = json.loads(result.data)
        comments = dataDict["comments"]
        print (comments)
        self.assertEqual(result.status_code,200)
        self.assertFalse(comments)