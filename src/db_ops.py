import pymongo

from src.config import BaseConfig as Config
from src.tools import BaseLogger


try:
    client = pymongo.MongoClient(Config.PYMONGO_URI)
    BaseLogger.logger.info("Connected to database")
except Exception as e:
    BaseLogger.logger.error(f"{e} error while connecting to database")


class DB:

    """
    This class contains database operations for MongoDB
    """

    def __init__(self, db=None, collection=None):
        self.db = client[db]
        self.collection = self.db[collection]

    def insert(self, data):
        self.collection.insert_one(data)

    def find(self, data):
        return self.collection.find_one(data)

    def find_all(self):
        return self.collection.find()

    def update(self, data, new_data):
        self.collection.update_one(data, new_data)

    def delete(self, data):
        self.collection.delete_one(data)
