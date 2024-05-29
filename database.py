from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv




class mongoDb:
    def __init__(self, connection_string):
        self.client = MongoClient(connection_string)
        self.db = self.client['CIA']  

    def add_data_to_collection(self, collection_name, data):
        collection = self.db[collection_name]
        result = collection.insert_one(data)
        return str(result.inserted_id)

    def search_data(self, collection_name, search_param):
        collection = self.db[collection_name]
        result = collection.find_one(search_param)
        if result:
            result['_id'] = str(result['_id'])  
        return result

    def update_document_with_id(self, collection_name, document_id, update_param):
        collection = self.db[collection_name]
        result = collection.update_one({'_id': ObjectId(document_id)}, {'$set': update_param})
        return result.modified_count > 0    

    def get_user_by_token(self, token):
        collection = self.db['Users']
        result = collection.find_one({'Token.AccessToken': token})
        if result:
            result['_id'] = str(result['_id'])  
        return result