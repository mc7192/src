from typing import List
from QuoteEngine.QuoteModel import QuoteModel
from .IngestorInterface import IngestorInterface
import pandas # type: ignore

class CSVIngestor(IngestorInterface):
    allowed_extensions = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise Exception('Cannot ingest exception.')
        
        quotes = []
        df = pandas.read_csv(path, header=0)

        for index, row in df.iterrows():
            quote = QuoteModel(row['body'], row['author'])

            quotes.append(quote)
        
        return quotes




    