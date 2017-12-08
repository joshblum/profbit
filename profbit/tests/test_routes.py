import unittest

from profbit.app import app


class RouteTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

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
