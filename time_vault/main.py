from fastapi import FastAPI

from .database import save_report_document
from .models import Report
from settings import Settings

SETTINGS = Settings()

app = FastAPI()


@app.post("/reports/")
def save_report(report: Report):
    return save_report_document(report)
