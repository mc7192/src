from typing import List
from QuoteEngine.QuoteModel import QuoteModel
from .IngestorInterface import IngestorInterface


class TextIngestor(IngestorInterface):
    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise Exception('Cannot ingest exception.')
        
        quotes = []
    
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                body, author = line.split(' - ')
                quote = QuoteModel(body.strip(), author.strip())
                quotes.append(quote)

        return quotes

            
                

