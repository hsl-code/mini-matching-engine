from storage.data_storage import FileStorage
from storage.data_storage import PostgreSQL


class DataStorageManager:
    def __init__(self, data_storage='psql') -> None:
        self.data_storage = data_storage

    def output_stream(self):
        """Given the data storage attribute value, returns the right data storage."""
        if self.data_storage == 'psql':
            return PostgreSQL()
    
        if self.data_storage == 'file':
            return FileStorage()