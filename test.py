from flask import Flask, render_template,request
import random
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('test0.html')


@app.route('/test')
def test():
    return render_template('test.html', poziom=0, wiadomosc="melepeta")


if __name__ == '__main__':
    app.run(debug=True)
