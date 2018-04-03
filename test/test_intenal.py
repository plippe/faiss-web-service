import unittest
from flask import Flask
from src.internal.blueprint import blueprint as InternalBlueprint

class TestInternal(unittest.TestCase):

    def setUp(self):
        app = Flask(__name__)
        app.register_blueprint(InternalBlueprint)
        app.testing = True

        self.app = app.test_client()

    def test_ping(self):
        rv = self.app.get('/ping')
        assert b'pong' in rv.data
