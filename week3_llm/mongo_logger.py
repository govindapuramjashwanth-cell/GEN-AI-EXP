import os
from datetime import datetime, timezone
from pymongo import MongoClient

class MongoLogger:
    def __init__(self):
        uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        self.db = self.client["llm_monitoring"]
        self.collection = self.db["call_logs"]
        self.client.admin.command("ping")

    def log_call(self, log_data):
        log_data["timestamp"] = datetime.now(timezone.utc)
        self.collection.insert_one(log_data)
        print("Call details saved in MongoDB!")

    def close(self):
        self.client.close()
