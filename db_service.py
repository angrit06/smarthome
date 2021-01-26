from pymongo import MongoClient
from datetime import datetime

class DBService:
    def __init__(self, db_address="raspberrypi"):
        self.client = MongoClient(db_address)
        self.db = self.client.smarthome
        self.collection = self.db.bedroom

    def __create_doc(self, topic, payload):
        doc = {topic: payload, "date": datetime.utcnow()}
        return doc

    def __insert_doc(self, doc):
        id = self.collection.insert_one(doc).inserted_id
        return id

    def save_data(self,topic,payload):
        id = self.__insert_doc(doc=self.__create_doc(topic=topic,payload=payload))
        return id
