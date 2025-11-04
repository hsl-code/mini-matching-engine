"""Can easily extend and add more data storage options here.
"""
import abc


class DataStorage(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def output_stream(self, input_filepath):
        raise NotImplementedError


class FileStorage(DataStorage):
    def __init__(self) -> None:
        pass
    
    def output_stream(self):
        pass


class PostgreSQL(DataStorage):
    def __init__(self) -> None:
        pass

    def output_stream(self):
        pass