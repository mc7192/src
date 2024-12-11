import os
import random
from MemeGenerator import MemeEngine
from QuoteEngine.Ingestor import Ingestor, QuoteModel
import argparse

def generate_meme(path=None, body=None, author=None):
    """Generate a meme given an image path and a quote."""
    img = None
    quote = None

    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs.extend([os.path.join(root, name) for name in files if name.lower().endswith(('jpg', 'jpeg', 'png', 'gif', 'bmp'))])
        img = random.choice(imgs)
    else:
        img = path

    if body is None:
        quote_files = [
            './_data/DogQuotes/DogQuotesTXT.txt',
            './_data/DogQuotes/DogQuotesDOCX.docx',
            './_data/DogQuotes/DogQuotesPDF.pdf',
            './_data/DogQuotes/DogQuotesCSV.csv'
        ]
        quotes = []
        for f in quote_files:
            try:
                quotes.extend(Ingestor.parse(f))
            except Exception as e:
                print(f"Error parsing file {f}: {e}")
        quote = random.choice(quotes)
    else:
        if author is None:
            raise ValueError('Author is required if a quote body is provided.')
        quote = QuoteModel(body, author)

    meme = MemeEngine('./tmp')
    path = meme.make_meme(img, quote.body, quote.author)
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a meme with a quote.")
    parser.add_argument('--path', type=str, help="Path to the image file.")
    parser.add_argument('--body', type=str, help="Quote body to add to the image.")
    parser.add_argument('--author', type=str, help="Quote author to add to the image.")
    args = parser.parse_args()

    try:
        print(generate_meme(args.path, args.body, args.author))
    except Exception as e:
        print(f"Error: {e}")