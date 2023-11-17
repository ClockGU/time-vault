from typing import Dict
from pydantic import BaseModel


class Day(BaseModel):
    pass


class GeneralInfo(BaseModel):
    pass


class Report(BaseModel):
    shift_content: Dict[str, Day]
    general: GeneralInfo

