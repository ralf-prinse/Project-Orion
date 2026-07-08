from __future__ import annotations

from dataclasses import fields
from dataclasses import is_dataclass
from datetime import datetime
from enum import Enum
from types import UnionType
from typing import Any
from typing import get_args
from typing import get_origin


class DataclassSerializer:
    """
    Generic serializer for Orion dataclass models.

    Supports:
    - dataclasses
    - nested dataclasses
    - datetime
    - Enum
    - list
    - tuple
    - dict
    - Optional / Union
    - primitive values
    """

    def to_dict(
        self,
        value: Any,
    ) -> Any:
        if value is None:
            return None

        if isinstance(value, datetime):
            return {
                "__type__": "datetime",
                "value": value.isoformat(),
            }

        if isinstance(value, Enum):
            return {
                "__type__": "enum",
                "class": value.__class__.__name__,
                "value": value.value,
            }

        if is_dataclass(value):
            return {
                field.name: self.to_dict(
                    getattr(value, field.name),
                )
                for field in fields(value)
            }

        if isinstance(value, list):
            return [
                self.to_dict(item)
                for item in value
            ]

        if isinstance(value, tuple):
            return [
                self.to_dict(item)
                for item in value
            ]

        if isinstance(value, dict):
            return {
                str(key): self.to_dict(item)
                for key, item in value.items()
            }

        return value

    def from_dict(
        self,
        model_type,
        data: Any,
    ) -> Any:
        if data is None:
            return None

        if self._is_optional(model_type):
            inner_type = self._optional_inner_type(model_type)
            return self.from_dict(
                inner_type,
                data,
            )

        if model_type is datetime:
            if isinstance(data, dict):
                return datetime.fromisoformat(data["value"])

            return datetime.fromisoformat(data)

        origin = get_origin(model_type)

        if origin is list:
            item_type = get_args(model_type)[0]
            return [
                self.from_dict(item_type, item)
                for item in data
            ]

        if origin is tuple:
            item_type = get_args(model_type)[0]
            return tuple(
                self.from_dict(item_type, item)
                for item in data
            )

        if origin is dict:
            key_type, value_type = get_args(model_type)

            return {
                self._cast_key(key_type, key): self.from_dict(
                    value_type,
                    value,
                )
                for key, value in data.items()
            }

        if isinstance(model_type, type) and issubclass(model_type, Enum):
            if isinstance(data, dict):
                return model_type(data["value"])

            return model_type(data)

        if is_dataclass(model_type):
            kwargs = {}

            for field in fields(model_type):
                if field.name not in data:
                    continue

                kwargs[field.name] = self.from_dict(
                    field.type,
                    data[field.name],
                )

            return model_type(**kwargs)

        return data

    def _is_optional(
        self,
        model_type,
    ) -> bool:
        origin = get_origin(model_type)

        return (
            origin is UnionType
            or str(origin) == "typing.Union"
        ) and type(None) in get_args(model_type)

    def _optional_inner_type(
        self,
        model_type,
    ):
        return next(
            item
            for item in get_args(model_type)
            if item is not type(None)
        )

    def _cast_key(
        self,
        key_type,
        key,
    ):
        if key_type is str:
            return str(key)

        if key_type is int:
            return int(key)

        return key