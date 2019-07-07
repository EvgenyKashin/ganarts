import time
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           indexes=list(range(9)))


# @app.route('/images/<filename>')
# def serve_image(filename):
#     return send_from_directory(images_path,
#                                filename,
#                                as_attachment=True,
#                                cache_timeout=-1)


@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory('images',
                               filename,
                               cache_timeout=-1)


if __name__ == '__main__':
    app.run(host='0.0.0.0')


def benchmark():
    for i in range(3):
        start = time.time()
        download_next_images()
        print('{:.2f}'.format(time.time() - start))