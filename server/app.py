from flask import Flask, render_template, send_from_directory

app = Flask(__name__, template_folder='static')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory('images', filename, cache_timeout=-1)