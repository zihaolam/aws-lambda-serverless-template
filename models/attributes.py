from typing import Any, Union
from pynamodb.attributes import NumberAttribute, UnicodeSetAttribute, UnicodeAttribute
from datetime import date, datetime

from exceptions import LambdaException


class UnixTimestampAttribute(NumberAttribute):
    """
    A Unix Time attribute
    """

    def serialize(self, time_to_serialize: Union[datetime, str, float]):
        if isinstance(time_to_serialize, str):
            return datetime.fromisoformat(time_to_serialize).timestamp()

        if isinstance(time_to_serialize, datetime):
            return time_to_serialize.timestamp()

        if isinstance(time_to_serialize, float):
            return time_to_serialize

        raise LambdaException(status_code=422, message="Invalid Timestamp Attribute")

    def deserialize(self, timestamp: float):
        ## return timestamp
        return float(timestamp)


class CustomUnicodeSetAttribute(UnicodeSetAttribute):
    def serialize(self, value):
        return list(value) or []

    def deserialize(self, value):
        return super().deserialize(value) or []


class DateAttribute(UnicodeAttribute):
    def serialize(self, date_object: date) -> str:
        return str(date_object)

    def deserialize(self, date_string: str) -> date:
        return date(*[int(s) for s in date_string.split("-")])
