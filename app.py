import random
import os
import requests # type: ignore
from flask import Flask, render_template, abort, request # type: ignore
from MemeGenerator.MemeEngine import MemeEngine 
from QuoteEngine.Ingestor import Ingestor

app = Flask(__name__)

meme = MemeEngine('./static')


def setup():
    """ Load all resources """

    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    quotes = []
    for file in quote_files:
        try:
            quotes.extend(Ingestor.parse(file))
        except Exception as e:
            print(f"Error processing file {file}: {e}")

    images_path = "./_data/photos/dog/"
    imgs = []
    try:
        for root, _, files in os.walk(images_path):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                    imgs.append(os.path.join(root, file))
    except Exception as e:
        print(f"Error processing images in {images_path}: {e}")

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme """
    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme """

    image_url = request.form.get('image_url')
    body = request.form.get('body')
    author = request.form.get('author')
    temp_file = './temp_image.jpg'

    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()  

        with open(temp_file, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        path = meme.make_meme(temp_file, body, author)

    except Exception as e:
        print(f"Error creating meme: {e}")
        path = None

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


    return render_template('meme.html', path=path)


if __name__ == "__main__":
    app.run()
