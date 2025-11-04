from data_source.datasources import FileLoader
from data_source.datasources import KafkaInputStream


class DataSourceManager:
    def __init__(self, input_source='kafka') -> None:
        self.input_source = input_source
        self.datasource = self.datasource_mapper()
    
    def datasource_mapper(self):
        """Given the datasource attribute value, returns the right datasource loader."""
        if self.input_source == 'kafka':
            return KafkaInputStream()
    
        if self.input_source == 'file':
            return FileLoader()

    def load(self, input_filepath):
        return self.datasource.load(input_filepath)