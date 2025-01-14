from pymongo import MongoClient
from pymongo.server_api import ServerApi
import datetime
import certifi
from os import environ as env


class MongoDB:
    def __init__(self, table):
        self.table = table
        self.connect()
        pass

    def connect(self):
        passw = env.get('mongo_pass')
        uri = "mongodb+srv://ihamilton:"+passw+"@talent-os.z0ioh.mongodb.net/?retryWrites=true&w=majority&appName=Talent-os"
        self.client = MongoClient(uri, tlsCAFile=certifi.where(), server_api=ServerApi(
            version='1', strict=True, deprecation_errors=True))
        database = self.client["divbr"]
        self.collection = database[self.table]

        pass

    def insert_one(self, document):
        """
        Insert a document into the collection
        :param document: Dictionary
        :return:
        """
        document['schema_version'] = 1
        document['date'] = datetime.datetime.now()
        result = self.collection.insert_one(document)
        self.client.close()

        return result

    def update_or_insert(self, document, filter):
        set = {'$set':document}
        result = self.collection.update_one(update=set, upsert=True, filter=filter)

        self.client.close()
        return result


    def find_one(self, filter):

        result = self.collection.find_one(filter)

        return result

    def delete(self, query):


        post = self.collection.delete_one(query)

        return

    def find(self,filter):

        result = self.collection.find(filter)

        return result

    def add_to_set(self, filter_set, data):


        result = self.collection.update_one(
            filter_set,
            {
                    '$addToSet':{
                        'connecttions':
                            data

                    }
            }
        )

        return result




