import datetime

from time_vault.database import get_report_collection

from .log import LOGGER


def deprovision_reports():
    """
    Deprovision all saved reports that are older than two years upon execution of this function.
    :return:
    """
    today = datetime.date.today()
    collection = get_report_collection()
    # use $lte to assure deletion of reports even after the original deletion date
    d = collection.delete_many(
        {"general.year": today.year - 2, "general.month": {"$lte": today.month}}
    )
    LOGGER.debug(
        f"{d.deleted_count} reports deleted for month {today.month} in year {today.year - 2}. (Run at {today.strftime('%d.%m.%Y')})"
    )
