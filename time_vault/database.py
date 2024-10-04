from pymongo import MongoClient, database
from pymongo.typings import _DocumentType

from .models import Report
from .settings import get_settings

SETTINGS = get_settings()


def get_time_vault_database() -> database.Database[_DocumentType]:
    client = MongoClient(SETTINGS.DATABASE_URL)
    return client[SETTINGS.TIME_VAULT_DATABASE]


def get_report_collection() -> database.Collection:
    return get_time_vault_database()[SETTINGS.REPORT_COLLECTION]


def save_report_document(create: Report) -> Report:
    collection = get_report_collection()
    document = create.model_dump()
    report = collection.insert_one(document)
    return Report(**collection.find_one({"_id": report.inserted_id}))
