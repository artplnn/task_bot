import datetime

from pydantic import BaseModel
from typing import Literal


class FilterSalaryQuery(BaseModel):
    dt_from: datetime.datetime
    dt_upto: datetime.datetime
    group_type: Literal["hour", "day", "month"]
