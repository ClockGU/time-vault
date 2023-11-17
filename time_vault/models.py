from typing import Dict
from pydantic import BaseModel, field_validator
from datetime import datetime


class Day(BaseModel):
    pass


class GeneralInfo(BaseModel):
    pass


class Report(BaseModel):
    shift_content: Dict[str, Day]
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
