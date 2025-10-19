#!/usr/bin/env python
# coding: utf-8

from pymongo import MongoClient, ASCENDING, TEXT
from pymongo.errors import PyMongoError

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self):
        # MongoDB login info
        USER = 'aacuser'
        PASS = 'password'
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 34363
        DB   = 'AAC'
        COL  = 'animals'

        # connect to MongoDB
        self.client = MongoClient(f'mongodb://{USER}:{PASS}@{HOST}:{PORT}', serverSelectionTimeoutMS=5000)
        self.database = self.client[DB]
        self.collection = self.database[COL]

        # enhanced: check connection works
        try:
            self.client.admin.command("ping")
        except Exception as e:
            print(f"[db] could not connect: {e}")

        # enhanced: add indexes for better search/filter
        self._ensure_indexes()

    def _ensure_indexes(self):
        """create helpful indexes to make searching faster"""
        try:
            # text index to search by name or breed
            self.collection.create_index(
                [("name", TEXT), ("breed", TEXT)],
                name="idx_text_name_breed"
            )
            # compound index for breed + outcome filters
            self.collection.create_index(
                [("breed", ASCENDING), ("outcome_type", ASCENDING)],
                name="idx_breed_outcome"
            )
        except PyMongoError as e:
            print(f"[db] index warning: {e}")

    # create a new animal record
    def create(self, data):
        if data:
            try:
                self.collection.insert_one(data)
                return True
            except Exception as e:
                print(f"[db] insert error: {e}")
                return False
        return False

    # read/find animals by query
    def read(self, query):
        try:
            return list(self.collection.find(query))
        except Exception as e:
            print(f"[db] read error: {e}")
            return []

    # update one or more animal records
    def update(self, query, new_data):
        if query and new_data:
            try:
                result = self.collection.update_many(query, {"$set": new_data})
                return result.modified_count
            except Exception as e:
                print(f"[db] update error: {e}")
                return 0
        return 0

    # delete one or more animal records
    def delete(self, query):
        if query:
            try:
                result = self.collection.delete_many(query)
                return result.deleted_count
            except Exception as e:
                print(f"[db] delete error: {e}")
                return 0
        return 0