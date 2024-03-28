import logging
import os
import sys
from datetime import datetime, timedelta

from pymongo.errors import ConfigurationError
from pymongo.mongo_client import MongoClient

# Set up logging
logging.basicConfig(level=logging.INFO)


class Database:
    def __init__(self):
        self.db_uri = os.getenv("DB_URI")
        self.db_name = os.getenv("DB_NAME")
        try:
            self.client = MongoClient(self.db_uri)
            self.db = self.client[self.db_name]
            logging.info("Connected to MongoDB")
        except ConfigurationError:
            print(
                "An Invalid URI host error was received. Is your Atlas host name correct in your connection string?"
            )
            sys.exit(1)

    def update_segment_effort_data(self, segment):
        fetch_date = datetime.now().strftime("%d-%m-%Y")
        logging.info(f"Writing data for segment {segment['id']} to MongoDB")
        self.db.segment_stats.update_one(
            {"segment_id": segment["id"], "name": segment["name"]},
            {
                "$push": {
                    "efforts": {
                        "effort_count": segment["effort_count"],
                        "fetch_date": fetch_date,
                    }
                }
            },
            upsert=True,
        )
        logging.info("Data written to MongoDB")

    def get_segment_effort_data(self, segment_id):
        logging.info(f"Fetching data for segment {segment_id} from MongoDB")
        segment_effort_data = self.db.segment_stats.find_one({"segment_id": segment_id})
        return segment_effort_data

