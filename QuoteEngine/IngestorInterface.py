from abc import ABC, abstractmethod
from typing import List
from .QuoteModel import QuoteModel

class IngestorInterface(ABC): 
    allowed_extensions = []

    @classmethod
    def can_ingest(cls, path) -> bool:
        if '.' not in path:
            return False
        ext = path.split('.', path[-1])
        return ext in cls.allowed_extensions
    
    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        pass


