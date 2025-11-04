from data_source.datasources import FileLoader


class DataSourceManager:
    def __init__(self, input_source='kafka') -> None:
        self.input_source = input_source
        self.datasource = self.datasource_mapper()
    
    def datasource_mapper(self):
        """Given the datasource attribute value, returns the right datasource loader.
        
        For instance, if consuming from kafka, one could add the following:
        if self.input_source == 'kafka':
            return KafkaInputStream()
        where KafkaInputStream will be a new class created in datasources.py.
        """
        if self.input_source == 'file':
            return FileLoader()

    def load(self, input_filepath):
        return self.datasource.load(input_filepath)