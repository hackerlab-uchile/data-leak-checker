import re
from enum import StrEnum, auto
from typing import Any, Literal, Self, Sequence

from sqlalchemy import BindParameter, cast
from sqlalchemy.dialects.postgresql import ARRAY, ENUM
from sqlalchemy.sql.elements import ColumnElement


class ArrayOfEnum(ARRAY):
    def bind_expression(
        self, bindvalue: BindParameter[Sequence[Any]]
    ) -> ColumnElement[Sequence[Any]] | None:
        return cast(bindvalue, self)

    def result_processor(self, dialect, coltype):
        super_rp = super(ArrayOfEnum, self).result_processor(dialect, coltype)

        def handle_raw_string(value):
            return_list = []
            m = re.match(r"^{(.*)}$", value)
            inner = m.group(1) if m else ""
            for item in inner.split(","):
                return_list.append(item.strip('"'))
            return return_list

        def process(value):
            return super_rp(handle_raw_string(value))

        return process


class DataType(StrEnum):
    EMAIL = auto()
    PHONE = auto()
    RUT = auto()
    HASH = auto()
    IP_ADDR = auto()
    CREDIT_CARD = auto()
    DATE = auto()
    STRING = auto()
    UNKOWN = "unknown"

    @classmethod
    def from_str(cls, value: str) -> Self:
        for dtype in list(cls):
            if value == dtype.value:
                return dtype
        return cls("unknown")

    @classmethod
    def get_all_types(cls) -> list[str]:
        return [dtype.value for dtype in list(cls)]

    @classmethod
    def get_key_types(cls) -> list[Literal[EMAIL, PHONE, RUT]]:
        return [
            cls.EMAIL,
            cls.PHONE,
            cls.RUT,
        ]


DataTypePostgresEnum = ENUM(*DataType.get_all_types(), name="data_types")
