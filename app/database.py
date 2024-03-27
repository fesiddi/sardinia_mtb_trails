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

    def write_to_mongodb(self, result):
        fetch_date = datetime.now().strftime("%d-%m-%Y")
        for segment in result:
            logging.info(f"Writing data for segment {segment['id']} to MongoDB")
            self.db.segment_stats.update_one(
                {"segment_id": segment["id"]},
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

    def get_effort_count_change(self, segment_id, days):
        x_days_ago = (datetime.now() - timedelta(days=days)).strftime("%d-%m-%Y")
        segment_data = self.db.segment_stats.find_one({"segment_id": segment_id})
        if segment_data:
            efforts_last_x_days = [
                effort
                for effort in segment_data["efforts"]
                if effort["fetch_date"] >= x_days_ago
            ]
            efforts_last_x_days = sorted(
                efforts_last_x_days, key=lambda x: x["fetch_date"]
            )
            if len(efforts_last_x_days) >= 2:
                initial_effort_count = efforts_last_x_days[0]["effort_count"]
                final_effort_count = efforts_last_x_days[-1]["effort_count"]
                effort_count_change = final_effort_count - initial_effort_count
                return effort_count_change
        return None

    def get_effort_counts_for_date_range(self, segment_id, start_date, end_date):
        start_date = datetime.strptime(start_date, "%d-%m-%Y")
        end_date = datetime.strptime(end_date, "%d-%m-%Y")
        segment_data = self.db.segment_stats.find_one({"segment_id": segment_id})
        if segment_data:
            efforts_in_date_range = [
                effort
                for effort in segment_data["efforts"]
                if start_date <= effort["fetch_date"] <= end_date
            ]
            efforts_in_date_range = sorted(
                efforts_in_date_range, key=lambda x: x["fetch_date"]
            )
            effort_counts = [
                {
                    "fetch_date": effort["fetch_date"],
                    "effort_count": effort["effort_count"],
                }
                for effort in efforts_in_date_range
            ]
            return effort_counts
        return None
