"""Module containing classes for various data sources.

This module was written in an extensible manner so as to
enable ease of adding new data sources.

For instance, if we wanted to add Kafka as an input stream, we could 
simply add

class KafkaInputStream(DataLoader):
    def __init__(self) -> None:
        pass
    
    def load(self, input_filepath):
        pass
"""
import abc
import ndjson

from domain.data_models import Amend
from domain.data_models import Cancel
from domain.data_models import Sell
from domain.data_models import Buy


class DataLoader(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def load(self, input_filepath):
        raise NotImplementedError


class FileLoader(DataLoader):
    def __init__(self) -> None:
        pass
    
    def load(self, input_filepath):
        # load from file-like objects
        with open(input_filepath) as f:
            data = ndjson.load(f)

        text = ndjson.dumps(data)
        data = ndjson.loads(text)

        objects_list = self.load_array(data)
        return objects_list

    def load_array(self, data):
        """Takes in an array of dictionaries and converts it into an array of corresponding data models."""
        objects_list = []

        for datum in data:
            objects_list.append(self.to_obj(datum))

        return objects_list

    def to_obj(self, datum):
        """Takes a dictionary and converts it into the suitable data model."""
        if datum["type"] == "amend":
            return Amend(datum)
        if datum["type"] == "cancel":
            return Cancel(datum)
        else:
            if datum["side"] == "B":
                return Buy(datum)
            elif datum["side"] == "S":
                return Sell(datum)
        
