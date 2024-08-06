from contextlib import asynccontextmanager
from typing import Annotated

import sentry_sdk
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import Depends, FastAPI, Query
from fastapi.security.api_key import APIKey

from .auth import required_api_key
from .database import get_report_collection, save_report_document
from .log import setup_logger
from .models import Report
from .settings import get_settings
from .tasks import deprovision_reports


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup Logger
    setup_logger()
    # Setup Scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(deprovision_reports, trigger=CronTrigger(day=1))
    scheduler.start()
    yield


SETTINGS = get_settings()

if SETTINGS.DEBUG is False:
    sentry_sdk.init(dsn=SETTINGS.SENTRY_URL, enable_tracing=True)

app = FastAPI(debug=SETTINGS.DEBUG, lifespan=lifespan)


@app.post("/reports/", status_code=201)
def save_report(report: Report, api_key: APIKey = Depends(required_api_key)):
    return save_report_document(report)


@app.get("/retrieve/{month}/{year}/", status_code=200)
def get_reports(
    month: int,
    year: int,
    references: Annotated[list[str], Query()],
    api_key: APIKey = Depends(required_api_key),
):
    collection = get_report_collection()
    result = collection.find(
        {
            "general.month": month,
            "general.year": year,
            "general.reference": {"$in": references},
        },
    )
    return [Report(**item) for item in result]
