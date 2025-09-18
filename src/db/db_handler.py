from enum import Enum

import pymongo

HOST_NAME = 'mongodb://localhost:27017/'
DB_NAME = "exchange-rates"
COLLECTION_NAME = "uae_rates"


def to_dict(obj):
    if isinstance(obj, list):
        return [to_dict(item) for item in obj]

    if isinstance(obj, set):  # 🔑 convert sets to lists
        return [to_dict(item) for item in obj]

    if isinstance(obj, Enum):
        return obj.value

    if hasattr(obj, "__dict__"):
        return {k: to_dict(v) for k, v in obj.__dict__.items() if v is not None}

    return obj


class DatabaseHandler:
    def __init__(self, collection_name=COLLECTION_NAME):
        self.client = pymongo.MongoClient(HOST_NAME)
        self.db = self.client[DB_NAME]
        self.collection = self.db[collection_name]

    def insert_data(self, data):
        try:
            # self.collection.insert_one(data)
            self.collection.insert_one(data)
        except Exception as e:
            print(f"Error: {e}")

    def remove_by_id(self, id):
        try:
            # self.collection.insert_one(data)
            self.collection.delete_one({"id": id})
        except Exception as e:
            print(f"Error: {e}")

    def replace_product_data(self, data):
        try:
            result = self.collection.replace_one({"id": data.id}, to_dict(data), True)
        except Exception as e:
            print(f"Error: {e}")

    def get_scraped_ids(self):
        scraped_documents = self.collection.find({}, {'id': 1})
        scrapedDocumentIds = []

        for document in scraped_documents:
            scrapedDocumentIds.append(document['id'])
        return scrapedDocumentIds

    def get_scraped_ids_set(self):
        scraped_documents = self.collection.find({}, {'id': 1})
        scrapedDocumentIds = set()

        for document in scraped_documents:
            scrapedDocumentIds.add(document['id'])
        return scrapedDocumentIds

    def get_scraped_ids_set_by_product_seller(self, product_seller):
        scraped_documents = self.collection.find({'product_seller': product_seller}, {'id': 1})
        scrapedDocumentIds = set()

        for document in scraped_documents:
            scrapedDocumentIds.add(document['id'])
        return scrapedDocumentIds
