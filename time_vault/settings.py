import os
from functools import lru_cache


class Settings:
    def __init__(self):
        self.__database_url = os.environ.get("MONGO_URL")
        self.__api_key = os.environ.get("API_KEY")
        self.__time_vault_database = os.environ.get("MONGO_DATABASE", "time_vault")
        self.__report_collection = "reports"
        self.__debug = bool(os.environ.get("DEBUG", False))
        self.__sentry_url = os.environ.get("SENTRY_URL", "")

    @property
    def SENTRY_URL(self):
        return self.__sentry_url

    @property
    def DEBUG(self):
        return self.__debug

    @property
    def DATABASE_URL(self):
        return self.__database_url

    @property
    def API_KEY(self):
        return self.__api_key

    @property
    def TIME_VAULT_DATABASE(self):
        return self.__time_vault_database

    @property
    def REPORT_COLLECTION(self):
        return self.__report_collection


@lru_cache()
def get_settings():
    return Settings()
