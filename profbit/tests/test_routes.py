import os
import unittest
from os.path import dirname as parent

from profbit.app import app


class RouteTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_keybase(self):
        resp = self.app.get('/keybase.txt')
        self.assertEqual(resp.status_code, 200)
        path = os.path.join(parent(parent(__file__)), 'static', 'keybase.txt')
        with open(path, 'rb') as f:
            self.assertEqual(resp.data, f.read())

    def test_index(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_donate(self):
        resp = self.app.get('/donate/')
        self.assertEqual(resp.status_code, 200)

    def test_stats(self):
        resp = self.app.get('/stats/', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

    def test_logout(self):
        resp = self.app.get('/logout/', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
