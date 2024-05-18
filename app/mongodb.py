from pymongo.mongo_client import MongoClient

from app.config import URI


class MongoDB:
    def __init__(self):
        self.client = MongoClient(URI)