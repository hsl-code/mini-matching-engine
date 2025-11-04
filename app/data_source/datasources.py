"""Can easily extend and add more datasources here.
"""
import abc


class DataLoader(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def load(self, input_filepath):
        raise NotImplementedError


class FileLoader(DataLoader):
    def __init__(self) -> None:
        pass
    
    def load(self, input_filepath):
        pass


class KafkaInputStream(DataLoader):
    def __init__(self) -> None:
        pass
    
    def load(self, input_filepath):
        pass