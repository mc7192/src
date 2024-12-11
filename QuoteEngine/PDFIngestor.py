from typing import List
import subprocess
import os
import random

from .QuoteModel import QuoteModel
from .IngestorInterface import IngestorInterface

class PDFIngestor(IngestorInterface):
    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise Exception('Cannot ingest exception.')
        
        quotes = []
        tmp = f'./tmp/{random.randint(0,1000000)}.txt'
        call = subprocess.call(['pdftotext', path, tmp])

        file_ref = open(tmp, 'r')
        for line in file_ref.readlines():
            body, author = line.split(' - ')
            quote = QuoteModel(body.strip(), author.strip())
            quotes.append(quote)
        
        file_ref.close()
        os.remove(tmp)
        return quotes



        
