from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from pymongo.mongo_client import MongoClient

from app.config import URI


class MongoDB:
    HOUR = "hour"
    DAY = "day"
    MONTH = "month"
    TYPE_FILTER = {
        HOUR: "%Y-%m-%dT%H:00:00",
        DAY: "%Y-%m-%dT00:00:00",
        MONTH: "%Y-%m-01T00:00:00"
    }

    def __init__(self):
        self.client = MongoClient(URI)

    def get_data(self, query_data):
        db = self.client.sampleDB
        dict_with_dates = self._get_dict_with_dates(query_data)
        pipeline = self._get_pipeline(query_data)
        data_from_db = db.sample_collection.aggregate(pipeline)
        self.fill_dict_with_data(dict_with_dates, data_from_db)
        return dict_with_dates

    @staticmethod
    def fill_dict_with_data(dict_with_dates, data_from_db):
        for item in data_from_db:
            dict_with_dates[item["_id"]] = item["value"]

    def _get_pipeline(self, query_data):
        return [
            {
                "$match": {
                    "dt": {
                        "$gte": query_data.dt_from,
                        "$lte": query_data.dt_upto
                    }
                }
            },
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": self.TYPE_FILTER[
                                query_data.group_type
                            ],
                            "date": "$dt"
                        }
                    },
                    "value": {
                        "$sum": "$value"
                    }
                }
            }
        ]

    def _get_dict_with_dates(self, query_data):
        match query_data.group_type:
            case self.MONTH:
                return self._get_dict_with_dates_month(query_data.dt_from, query_data.dt_upto)
            case self.DAY:
                return self._get_dict_with_dates_day(query_data.dt_from, query_data.dt_upto)
            case self.HOUR:
                return self._get_dict_with_dates_hour(query_data.dt_from, query_data.dt_upto)

    def _get_dict_with_dates_month(self, start_date: datetime, end_date: datetime):
        return {
            (start_date + relativedelta(months=item)).strftime(self.TYPE_FILTER[self.MONTH]): 0
            for item in range(0, (end_date.month - start_date.month) + 1)
        }

    def _get_dict_with_dates_day(self, start_date: datetime, end_date: datetime):
        return {
            (start_date + timedelta(days=item)).strftime(self.TYPE_FILTER[self.DAY]): 0
            for item in range(0, (end_date - start_date).days + 1)
        }

    def _get_dict_with_dates_hour(self, start_date: datetime, end_date: datetime):
        return {
            (start_date + timedelta(hours=item)).strftime(self.TYPE_FILTER[self.HOUR]): 0
            for item in range(0, int((end_date - start_date).total_seconds() // 3600) + 1)
        }
