import re
from typing import Dict
from pydantic import BaseModel, field_validator, model_validator
from datetime import datetime


class Day(BaseModel):
    started: str
    stopped: str
    type: str
    worktime: str
    net_worktime: str
    breaktime: str
    sick_or_vac_time: str

    @field_validator("started", "stopped", "worktime", "breaktime")
    @classmethod
    def check_hh_mm(cls, string: str) -> str:
        hh_mm_patern = re.compile(r"^\d{2}:\d{2}$")
        assert hh_mm_patern.match(string)
        return string

    @field_validator("sick_or_vac_time", "net_worktime")
    @classmethod
    def check_empty_or_hh_mm(cls, string: str) -> str:
        if string != "":
            return cls.check_hh_mm(string)
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
    month: int
    year: int
    long_month_name: str
    debit_worktime: str
    total_worked_time: str
    last_month_carry_over: str
    next_month_carry_over: str
    net_worktime: str

    @field_validator("total_worked_time", "last_month_carry_over", "next_month_carry_over", "net_worktime")
    @classmethod
    def check_hh_mm(cls, string: str) -> str:
        hh_mm_patern = re.compile(r"\d{2}:\d{2}$")
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


k = {"days_content": {
    "09.11.2023": {"started": "17:00", "stopped": "18:00", "type": "", "worktime": "01:00", "net_worktime": "01:00",
                   "breaktime": "00:00", "sick_or_vac_time": ""},
    "15.11.2023": {"started": "10:00", "stopped": "18:00", "type": "Sick", "worktime": "08:00", "net_worktime": "",
                   "breaktime": "00:30", "sick_or_vac_time": "07:30"},
    "16.11.2023": {"started": "10:00", "stopped": "14:00", "type": "", "worktime": "04:00", "net_worktime": "04:00",
                   "breaktime": "00:00", "sick_or_vac_time": ""}},
    "general": {"user_name": "Grossmüller, Christian", "personal_number": "", "contract_name": "12", "month": 11,
                "year": 2023, "long_month_name": "November", "debit_worktime": "12:00", "total_worked_time": "12:30",
                "last_month_carry_over": "00:00", "next_month_carry_over": "00:30", "net_worktime": "12:30"}}
