from pymongo import MongoClient
from pymongo.errors import ConfigurationError

from app.utils.logger import Logger


class DatabaseConnectionError(Exception):
    def __init__(self, message="Could not connect to the database"):
        self.message = message
        super().__init__(self.message)


class Database:
    _instance = None

    def __new__(cls, config):
        if not cls._instance:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.config = config
        return cls._instance

    def __init__(self, config):
        if not hasattr(self, "initialized"):
            self.config = config
            self.db_uri = self.config.DB_URI
            self.db_name = self.config.DB_NAME

            if not self.db_uri or not self.db_name:
                Logger.error("DB_URI and DB_NAME environment variables must be set")
                raise DatabaseConnectionError(
                    "DB_URI and DB_NAME environment variables must be set"
                )
            try:
                self.client = MongoClient(self.db_uri)
                self.db = self.client[self.db_name]
                Logger.debug("Connected to MongoDB")
            except ConfigurationError:
                Logger.error(
                    "An Invalid URI host error was received. Is your Atlas host name correct in your connection string?"
                )
                raise DatabaseConnectionError(
                    "An Invalid URI host error was received. Is your Atlas host name correct in your connection string?"
                )
            except Exception as e:
                Logger.error(f"An error occurred: {e}")
                raise DatabaseConnectionError(f"An error occurred: {e}")

            self.initialized = True

    def insert_one(self, collection_name, document):
        self.db[collection_name].insert_one(document)

    def update_one(self, collection_name, query, new_values, upsert=False):
        self.db[collection_name].update_one(query, new_values, upsert=upsert)

    def find_one(self, collection_name, query):
        return self.db[collection_name].find_one(query)

    def find_one_without_id(self, collection_name, query):
        return self.db[collection_name].find_one(query, {"_id": 0})

    def find_many(self, collection_name, query):
        return self.db[collection_name].find(query)

    def delete_one(self, collection_name, query):
        result = self.db[collection_name].delete_one(query)
        return result.deleted_count > 0

    def close_connection(self):
        self.client.close()
        Logger.debug("Connection to MongoDB closed")
