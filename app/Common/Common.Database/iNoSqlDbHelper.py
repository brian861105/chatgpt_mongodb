from abc import ABC, abstractmethod

class iNoSqlDbHelper(ABC):
    @abstractmethod
    def connect(self):
        pass
    @abstractmethod
    def insert(self, collection: str, document: dict):
        pass
    
    @abstractmethod
    def find(self, collection:str, document:dict):
        pass
    @abstractmethod
    def update(self, collection:str, document:dict):
        pass
    @abstractmethod
    def delete(self, collection:str, document:dict):
        pass
    @abstractmethod
    def closeConnection(self):
        pass
    