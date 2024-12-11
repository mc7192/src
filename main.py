import argparse
import random
import os
from MemeGenerator import MemeEngine
from QuoteEngine import Ingestor

def main():
    """Main entry point for the meme generator program."""
    parser = argparse.ArgumentParser(description="Generate a random captioned image or specify custom inputs.")
    parser.add_argument('--body', type=str, help="Quote body to add to the image.")
    parser.add_argument('--author', type=str, help="Quote author to add to the image.")
    parser.add_argument('--path', type=str, help="Path to an image file.")
    args = parser.parse_args()

    quote_files = [
        './_data/DogQuotes/DogQuotesTXT.txt',
        './_data/DogQuotes/DogQuotesDOCX.docx',
        './_data/DogQuotes/DogQuotesPDF.pdf',
        './_data/DogQuotes/DogQuotesCSV.csv'
    ]
    quotes = []
    for file in quote_files:
        try:
            quotes.extend(Ingestor.parse(file))
        except Exception as e:
            print(f"Error loading quotes from {file}: {e}")

    images_path = "./_data/photos/dog/"
    imgs = []
    try:
        for root, _, files in os.walk(images_path):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                    imgs.append(os.path.join(root, file))
    except Exception as e:
        print(f"Error loading images from {images_path}: {e}")

    img = args.path if args.path else random.choice(imgs)
    if args.body and args.author:
        quote_body = args.body
        quote_author = args.author
    else:
        quote = random.choice(quotes)
        quote_body = quote.body
        quote_author = quote.author

    try:
        path = MemeEngine.generate_meme(img, quote_body, quote_author)
        print(f"Meme generated at: {path}")
    except Exception as e:
        print(f"Error generating meme: {e}")


if __name__ == "__main__":
    main()