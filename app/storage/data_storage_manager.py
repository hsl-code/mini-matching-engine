from storage.data_storage import DictOutput


class DataStorageManager:
    def __init__(self, data_storage='psql') -> None:
        self.data_storage = data_storage

    def output_stream(self):
        """Given the data storage attribute value, returns the right data storage.
        
        For instance, if we were using PostgreSQL, then we could add:
        if self.data_storage == 'psql':
            return PostgreSQL()
        where PostgreSQL would be a new class in data_storage.py
        """    
        if self.data_storage == 'dict_array':
            return DictOutput().output_stream()