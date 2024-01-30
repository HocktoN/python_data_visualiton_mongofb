import pymongo

from unittest import TestCase
from src.tools import connect_to_mongo

"""
Test file for testing database connection
"""


class TestDBConnect(TestCase):
    def test_connect_to_mongo(self):
        self.assertIsInstance(connect_to_mongo(), pymongo.MongoClient)
