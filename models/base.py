from typing import Set
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute,
    DiscriminatorAttribute,
)
from pynamodb.indexes import LocalSecondaryIndex, AllProjection, GlobalSecondaryIndex
import config
from models.attributes import UnixTimestampAttribute


class TimeSortLSI(LocalSecondaryIndex):
    class Meta:
        index_name = "TimeSortIndex"
        projection = AllProjection()

    pk = UnicodeAttribute(hash_key=True)
    time_sort_attr = UnixTimestampAttribute(range_key=True)


class SortKeyIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = "sort-key-index"
        read_capacity_units = 5
        write_capacity_units = 5
        projection = AllProjection()

    sk = UnicodeAttribute(hash_key=True)
    pk = UnicodeAttribute(range_key=True)


class UnicodeAttributeIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = "additional-attribute-index"
        read_capacity_units = 5
        write_capacity_units = 5
        projection = AllProjection()

    unicode_attribute = UnicodeAttribute(range_key=True, null=True)
    pk = UnicodeAttribute(hash_key=True)


class BaseModel(Model):
    class Meta:
        if config.STAGE == "staging":
            table_name = "STAGING_MAIN_TABLE"
        else:
            table_name = "MAIN_TABLE"
        region = "ap-southeast-1"
        read_capacity_units = 25
        write_capacity_units = 25
        if config.STAGE == "dev":
            host = "http://localhost:8392"

    pk = UnicodeAttribute(hash_key=True)
    sk = UnicodeAttribute(range_key=True)
    sk_index = SortKeyIndex()
    unicode_attribute = UnicodeAttribute(null=True)
    unicode_attribute_index = UnicodeAttributeIndex()
    type = DiscriminatorAttribute()
