from pathlib import Path
import random
from flask import Flask, render_template, send_from_directory

app = Flask(__name__, template_folder='static')
images_path = Path('server/images')
all_images = list(images_path.iterdir())


@app.route('/')
def index():
    random.shuffle(all_images)
    return render_template('index.html')


@app.route('/images/<filename>')
def serve_image(filename):
    position = int(filename.split('.')[0].split('_')[1])
    return send_from_directory(images_path.name,
                               all_images[position].name,
                               cache_timeout=-1)