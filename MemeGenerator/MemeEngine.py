from PIL import Image, ImageDraw, ImageFont # type: ignore
import random
import os 

class MemeEngine:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def load_image(self, img_path):
        try:
            image = Image.open(img_path)
            return image
        except Exception as e:
            raise Exception('Not a valid file.')
    
    def resize(self, image, max_width):
        width, height = image.size
        if width > max_width:
            new_height = int(max_width * height / width)
            image = image.resize((max_width, new_height), Image.ANTIALIAS)
        return image
    
    def add_caption(self, image, text, author):
        draw = ImageDraw.Draw(image)
        caption = f"{text} - {author}"
        font = ImageFont.load_default()
        text_width, text_height = draw.multiline_textsize(caption, font=font)

        max_x = image.width - text_width
        max_y = image.height - text_height
        x_position = random.randint(0, max_x)
        y_position = random.randint(0, max_y)

        draw.multiline_text((x_position, y_position), caption, fill="white", font=font)
        return image

    def make_meme(self, img_path, text, author, width=500) -> str:
        try:
            image = self.load_image(img_path)
            image = self.resize(image, max_width=width)
            image = self.add_caption(image, text, author)
            output_path = os.path.join(self.output_dir, f"meme_{random.randint(0, 100000)}.jpg")
            image.save(output_path, format="JPEG")
            return output_path
        except Exception as e:
            raise Exception('Unable to create meme.')
