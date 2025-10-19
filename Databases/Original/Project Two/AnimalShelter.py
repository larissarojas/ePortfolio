#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pymongo import MongoClient

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self):
        USER = 'aacuser'
        PASS = 'password'
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 34363  
        DB = 'AAC'
        COL = 'animals'

        # Initialize MongoDB Client
        self.client = MongoClient(f'mongodb://{USER}:{PASS}@{HOST}:{PORT}')
        self.database = self.client[DB]
        self.collection = self.database[COL]

    # Create method
    def create(self, data):
        if data:
            try:
                self.collection.insert_one(data)
                return True
            except Exception as e:
                print(f"An error occurred: {e}")
                return False
        else:
            return False

    # Read method
    def read(self, query):
        try:
            results = self.collection.find(query)
            return list(results)
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    # Update method
    def update(self, query, new_data):
        if query and new_data:
            try:
                result = self.collection.update_many(query, {"$set": new_data})
                return result.modified_count  # Number of documents updated
            except Exception as e:
                print(f"An error occurred: {e}")
                return 0
        else:
            return 0

    # Delete method
    def delete(self, query):
        if query:
            try:
                result = self.collection.delete_many(query)
                return result.deleted_count  # Number of documents deleted
            except Exception as e:
                print(f"An error occurred: {e}")
                return 0
        else:
            return 0


# In[ ]:




