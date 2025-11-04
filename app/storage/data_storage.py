"""Module containing classes for various potential data storage integrations.

This module was written in an extensible manner so as to
enable ease of adding new data stores.

For instance, if we wanted to add PostgreSQL as an output datastore, we could 
simply add

class PostgreSQL(DataStorage):
    def __init__(self) -> None:
        pass

    def output_stream(self):
        pass
"""
import abc


class DataStorage(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def output_stream(self, input_filepath):
        raise NotImplementedError


class DictOutput(DataStorage):
    def __init__(self) -> None:
        pass
    
    def output_stream(self):
        """Output processed data as an array of dictionaries."""
        pass