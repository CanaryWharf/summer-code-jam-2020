import json
from unittest.mock import patch
from django.test import TestCase, Client
from chat.models import User


class ChatLobbyTest(TestCase):

    @patch('chat.views.go_to_chat_room')
    def test_invalid_names(self, data):
        User.objects.create_user('fake', password='test')

        client = Client()
        client.login(username='fake', password='test')

        tests = [
            ('', 400, None),
            ('hello!', 200, {"valid": False, "message": "Invalid chat room name. Names must be alphanumeric."}),
            ('fartoolonganame'*10, 400, None)
        ]

        for (invalid_name, expected_status_code, content) in tests:
            res = client.post('/api/chat/gotoroom/', json.dumps({
                'roomName': invalid_name,
                'private': False,
                'users': []
            }), content_type='application/json')

            self.assertEqual(res.status_code, expected_status_code)
            if content:
                self.assertEqual(
                    json.loads(res.content.decode()),
                    content,
                )

    @patch('chat.views.go_to_chat_room')
    def test_valid_names(self, data):
        User.objects.create_user('fake', password='test')

        client = Client()
        client.login(username='fake', password='test')

        tests = [
            ('myroom', 200, {"valid": True, "message": "Ok"}),
            ('myRoom', 200, {"valid": True, "message": "Ok"}),
            ('123', 200, {"valid": True, "message": "Ok"}),
            ('HowRU111', 200, {"valid": True, "message": "Ok"})
        ]

        for (valid_name, expected_status_code, content) in tests:
            res = client.post('/api/chat/gotoroom/', json.dumps({
                'roomName': valid_name,
                'private': False,
                'users': []
            }), content_type='application/json')

            self.assertEqual(res.status_code, expected_status_code)
            if content:
                self.assertEqual(
                    json.loads(res.content.decode()),
                    content,
                )

    @patch('chat.views.go_to_chat_room')
    def test_private_room(self, data):
        User.objects.create_user('valid1', password='test')
        User.objects.create_user('valid2', password='test')
        User.objects.create_user('invalid1', password='test')

        client = Client()

        # Check a user can create a private room
        client.login(username='valid1', password='test')

        res = client.post('/api/chat/gotoroom/', json.dumps({
                'roomName': 'privateroom',
                'private': True,
                'users': ['valid2']
            }), content_type='application/json')
        
        self.assertEqual(res.status_code, 200)

        client.logout()

        # Check a user cannot create a private room without at least one other member
        client.login(username='valid1', password='test')

        res = client.post('/api/chat/gotoroom/', json.dumps({
                'roomName': 'privateroom2',
                'private': True,
                'users': []
            }), content_type='application/json')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            json.loads(res.content.decode()),
            dict(
                valid=False,
                message='You need at least one other permitted user.'
            )
        )

        client.logout()

        # Check a permitted user can enter, regardless of the extra params included
        client.login(username='valid2', password='test')

        res = client.post('/api/chat/gotoroom/', json.dumps({
                'roomName': 'privateroom',
                'private': True,
                'users': ['valid1']
            }), content_type='application/json')

        self.assertEqual(res.status_code, 200)

        res = client.post('/api/chat/gotoroom/', json.dumps({
                'roomName': 'privateroom',
                'private': False,
                'users': []
            }), content_type='application/json')

        self.assertEqual(res.status_code, 200)

        client.logout()

        # Check a user who is not permitted cannot enter, regardless of aprams
        client.login(username='invalid1', password='test')

        res = client.post('/api/chat/gotoroom/', json.dumps({
                'roomName': 'privateroom',
                'private': True,
                'users': ['valid1']
            }), content_type='application/json')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            json.loads(res.content.decode()),
            dict(
                valid=False,
                message='This room is private and you are not on the permitted users list.'
            )
        )
