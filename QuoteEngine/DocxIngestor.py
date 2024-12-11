from typing import List
from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel
import docx  # type: ignore

class DocxIngestor(IngestorInterface):
    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise Exception('Cannot ingest exception.')
        
        quotes = []
        doc = docx.Document(path)

        for paragraph in doc.paragraphs:
            body, author = paragraph.text.split(' - ')
            quote = QuoteModel(body.strip(),author.strip())
            quotes.append(quote)
        
        return quotes
        
