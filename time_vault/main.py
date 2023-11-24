from fastapi import FastAPI, Depends
from fastapi.security.api_key import APIKey

from .database import save_report_document
from .models import Report
from .auth import required_api_key

app = FastAPI()


@app.post("/reports/")
def save_report(report: Report, api_key: APIKey = Depends(required_api_key)):
    return save_report_document(report)
