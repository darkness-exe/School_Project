from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return '<img src="/static/img/back.jpg" />'

if __name__ == '__main__':
    app.run(debug=True)

#этот файл не нужен
