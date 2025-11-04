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
import pandas as pd


class DataLoader(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def load(self, input_filepath):
        raise NotImplementedError


class FileLoader(DataLoader):
    def __init__(self) -> None:
        pass
    
    def load(self, input_filepath):
        df = pd.read_json(input_filepath, lines=True)
        return df 