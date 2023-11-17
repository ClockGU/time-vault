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
    sick_or_vac_time: str = ""

    @field_validator("started", "stopped", "worktime", "net_worktime", "breaktime")
    @classmethod
    def check_hh_mm(cls, string: str) -> str:
        hh_mm_patern = re.compile(r"\d{2}:\d{2}$")
        assert hh_mm_patern.match(string)
        return string

    @field_validator("sick_or_vac_time")
    @classmethod
    def check_empty_or_hh_mm(cls, string: str) -> str:
        if string != "":
            return cls.check_hh_mm(string)
        return string

    @field_validator("started", "stopped")
    @classmethod
    def not_negative_hh_mm(cls, string: str) -> str:
        assert not string.startswith("-")
        return string

    @model_validator(mode="after")
    def started_before_stopped(self) -> "Day":
        started = int(self.started.replace(":", ""))
        stopped = int(self.stopped.replace(":", ""))
        assert started < stopped
        return self


class GeneralInfo(BaseModel):
    pass


class Report(BaseModel):
    days_content: Dict[str, Day]
    general: GeneralInfo

    @field_validator("general")
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
# {
# 	"09.11.2023": {
# 		"started": "17:00",
# 		"stopped": "18:00",
# 		"type": "",
# 		"worktime": "01:00",
# 		"net_worktime": "01:00",
# 		"breaktime": "00:00",
# 		"sick_or_vac_time": ""
# 	}
# }