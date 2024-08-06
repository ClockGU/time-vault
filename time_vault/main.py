import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from typing import Annotated

import sentry_sdk
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import Depends, FastAPI, Query
from fastapi.security.api_key import APIKey

from .auth import required_api_key
from .database import get_report_collection, save_report_document
from .models import Report
from .settings import get_settings
from .tasks import deprovision_reports


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.add_job(deprovision_reports, trigger=CronTrigger(day=1))
    scheduler.start()
    yield


SETTINGS = get_settings()

if SETTINGS.DEBUG is False:
    sentry_sdk.init(dsn=SETTINGS.SENTRY_URL, enable_tracing=True)

app = FastAPI(debug=SETTINGS.DEBUG, lifespan=lifespan)

# Get the absolute path of the current file
current_file_path = os.path.abspath(__file__)
# Get the directory containing the current file
current_directory = os.path.dirname(current_file_path)
# Go up one directory level
ROOT_DIR = os.path.dirname(current_directory)

LOG_ROOT = os.path.join(ROOT_DIR, "logs")

try:
    os.mkdir(LOG_ROOT)
except FileExistsError:
    pass
logger = logging.getLogger("deprovisioning")
logger.setLevel(logging.DEBUG)
ch = TimedRotatingFileHandler(
    os.path.join(str(LOG_ROOT), "deprovision.log"),
    when="D",
    interval=1,
    backupCount=31,
)

logger.addHandler(ch)
logger.debug(f"INFO: Logger setup at {datetime.now().strftime('%d.%m.%Y - %H:%M:%S')}")


@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI app is starting up")


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
