import sentry_sdk
from fastapi import FastAPI, Depends
from fastapi.security.api_key import APIKey

from .database import save_report_document
from .models import Report
from .auth import required_api_key
from .settings import get_settings

SETTINGS = get_settings()
if SETTINGS.DEBUG is False:
    sentry_sdk.init(dsn=SETTINGS.SENTRY_URL, enable_tracing=True)

app = FastAPI()


@app.post("/reports/", status_code=201)
def save_report(report: Report, api_key: APIKey = Depends(required_api_key)):
    return save_report_document(report)
