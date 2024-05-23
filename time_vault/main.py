from typing import Annotated

import sentry_sdk
from fastapi import Depends, FastAPI, Query
from fastapi.security.api_key import APIKey

from .auth import required_api_key
from .database import get_report_collection, save_report_document
from .models import Report
from .settings import get_settings

SETTINGS = get_settings()
if SETTINGS.DEBUG is False:
    sentry_sdk.init(dsn=SETTINGS.SENTRY_URL, enable_tracing=True)

app = FastAPI()


@app.post("/reports/", status_code=201)
def save_report(report: Report, api_key: APIKey = Depends(required_api_key)):
    return save_report_document(report)


@app.get("/retrieve/{month}/{year}", status_code=200)
def get_reports(references: Annotated[list, Query()], month: int, year: int):
    collection = get_report_collection()
    result = collection.find(
        {"month": month, "year": year, "general.reference": {"$in": references}}
    )

    return map(Report, result)
