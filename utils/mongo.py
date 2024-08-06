from pymongo import MongoClient
from config import MONGO
from bson.objectid import ObjectId

class Database:
    DATABASE = None

    @staticmethod
    def initialize():
        client = MongoClient(MONGO)
        Database.DATABASE = client['bot']

    @staticmethod
    def insert(collection, data):
        result = Database.DATABASE[collection].insert_one(data)
        return result

    @staticmethod
    def fetchall(collection):
        return list(Database.DATABASE[collection].find())

    @staticmethod
    def remove(collection, id):
        result = Database.DATABASE[collection].delete_one({'_id': ObjectId(id)})
        return result

    @staticmethod
    def update(collection, query, update_data, upsert=True):
        result = Database.DATABASE[collection].update_one({'_id':ObjectId(query)}, {'$set': update_data}, upsert=upsert)
        return result

    @staticmethod
    def fetchOne(collection, id):
        return Database.DATABASE[collection].find_one({'_id': ObjectId(id)})
    
    @staticmethod
    def fetchOneFrom(collection_name, identifier, column):
      return Database.DATABASE[collection_name].find_one({column: identifier})