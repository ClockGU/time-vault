from pymongo import MongoClient, database
from pymongo.typings import _DocumentType

from .models import Report
import os

TIME_VAULT_DATABASE = "time_vault"
REPORT_COLLECTION = "reports"


def get_time_vault_database() -> database.Database[_DocumentType]:
    CONNECTION_STRING = os.environ.get("MONGO_URL")

    client = MongoClient(CONNECTION_STRING)

    return client[TIME_VAULT_DATABASE]


def get_report_collection() -> database.Collection:
    return get_time_vault_database()[REPORT_COLLECTION]


def save_report_document(create: Report) -> Report:
    collection = get_report_collection()
    document = create.model_dump()
    report = collection.insert_one(document)
    return Report(**collection.find_one({"_id": report.inserted_id}))
