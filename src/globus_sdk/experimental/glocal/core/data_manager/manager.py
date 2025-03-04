from __future__ import annotations

import abc
import dataclasses
import json
import typing as t

import requests

from globus_sdk import MISSING

DataType = t.TypeVar("DataType")
ErrorType = t.TypeVar("ErrorType", bound=Exception)

class DataManager(t.Generic[DataType]):

    def __init__(
        self,
        data_type: t.Type[DataType],
    ) -> None:
        self._data_type = data_type

    def create(self, request: requests.PreparedRequest) -> DataType:
        """
        Load data from a request object.
        """
        # Note - if we want to support non-json bodies, we'll need a more complex
        # loading mechanism.
        request_json = json.loads(request.body)
        # TODO - map error handler base on service error shape.

        # self._validate_data(request_json)
        return self._data_type(**request_json)

    def update(self, request: requests.PreparedRequest, data: DataType) -> DataType:
        """
        Update data from a request object.
        """
        request_json = json.loads(request.body)
        return dataclasses.replace(data, **request_json)

    def serialize(self, data: DataType) -> str:
        """
        Serialize data to a string.
        """

        return json.dumps(self.to_dict(data))

    def to_dict(self, data: DataType) -> dict[str, t.Any]:
        """
        Convert data to a dictionary.
        """
        data_dict = dataclasses.asdict(data)
        return {k: v for k, v in data_dict.items() if v is not MISSING}

    def _validate_data(self, data: DataType) -> None:
        """ Validate the data object. """
        for field in dataclasses.fields(data):
            if not isinstance(field.default, field.type):
                raise ValueError(f"Invalid type for field {field.name}")
        pass


class JSONDataLoader:
    def load(self):
        ...



class ErrorMapper(abc.ABC, t.Generic[ErrorType]):
    @abc.abstractmethod
    def map(self, error: KeyError) -> ErrorType:
        ...


