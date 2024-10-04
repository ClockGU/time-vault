import re
from datetime import datetime
from typing import Dict

from pydantic import BaseModel, field_validator, model_validator


class Day(BaseModel):
    started: str
    stopped: str
    type: str
    absence_type: str
    notes: str
    worktime: str
    breaktime: str

    @field_validator("started", "stopped", "worktime", "breaktime")
    @classmethod
    def check_hh_mm(cls, string: str) -> str:
        hh_mm_patern = re.compile(r"^\d{2}:\d{2}$")
        assert hh_mm_patern.match(string)
        return string

    @model_validator(mode="after")
    def started_before_stopped(self) -> "Day":
        started = int(self.started.replace(":", ""))
        stopped = int(self.stopped.replace(":", ""))
        assert started < stopped
        return self


class GeneralInfo(BaseModel):
    user_name: str
    personal_number: str
    contract_name: str
    reference: str
    month: int
    year: int
    long_month_name: str
    debit_worktime: str
    total_worked_time: str
    last_month_carry_over: str
    next_month_carry_over: str
    net_worktime: str

    @field_validator(
        "total_worked_time",
        "last_month_carry_over",
        "next_month_carry_over",
        "net_worktime",
    )
    @classmethod
    def check_hh_mm(cls, string: str) -> str:
        hh_mm_patern = re.compile(r"-?\d{2}:\d{2}$")
        assert hh_mm_patern.match(string)
        return string

    @field_validator("debit_worktime", "total_worked_time")
    @classmethod
    def not_negative_hh_mm(cls, string: str) -> str:
        assert not string.startswith("-")
        return string


class Report(BaseModel):
    days_content: Dict[str, Day]
    general: GeneralInfo

    @field_validator("days_content")
    @classmethod
    def check_date_string(cls, dictionary: Dict) -> Dict:
        """
        Check if all keys in a Dict are of DD.MM.YYYY format.
        :param dictionary:
        :return:
        """
        for key in dictionary.keys():
            datetime.strptime(key, "%d.%m.%Y")
        return dictionary
