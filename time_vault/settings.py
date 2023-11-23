import os


class Settings():
    def __init__(self):
        self.__database_url = os.environ.get("MONGO_URL")
        self.__api_key = os.environ.get("API_KEY")
        self.__time_vault_database = "time_vault"
        self.__report_collection = "reports"

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