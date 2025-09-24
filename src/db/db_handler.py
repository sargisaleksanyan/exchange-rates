from enum import Enum

import pymongo

from src.util.common_classes.exchange_company import ExchangeCompany

HOST_NAME = 'mongodb://localhost:27017/'
DB_NAME = "exchange_rates"
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
            dict = to_dict(data)
            self.collection.insert_one(dict)
        except Exception as e:
            print(f"Error: while inserting data {e}")

    def update_exchange_rate(self, company_exchange_data: ExchangeCompany):
        try:
            # self.collection.insert_one(data)
            dict = to_dict(company_exchange_data)
            result = self.collection.update_one({'url': dict['url']}, {
                '$set': {'company_exchange_rates': dict['company_exchange_rates']}})
            m = 5
        except Exception as e:
            print(f"Error: while updating exchange data {e}")

    def remove_by_id(self, id):
        try:
            # self.collection.insert_one(data)
            self.collection.delete_one({"id": id})
        except Exception as e:
            print(f"Error: {e}")

    def replace_data(self, data):
        try:
            result = self.collection.replace_one({"id": data.id}, to_dict(data), True)
        except Exception as e:
            print(f"Error: {e}")

    def find_company_by_url(self, url):
        company = self.collection.find_one({'url': url})
        return company
