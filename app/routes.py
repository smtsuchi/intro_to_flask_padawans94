from app import app
from flask import render_template

@app.route('/')
def index():
    staff = [
        {'name':'Shoha',
        'img':'https://img.freepik.com/premium-vector/smiling-face-emoji_1319-431.jpg?w=360',
        'age': 9000},
        {'name':'Brandt','img':'https://img.freepik.com/premium-vector/smiling-face-emoji_1319-431.jpg?w=360', 'age': 9001}, {'name':'Blair','img':'https://img.freepik.com/premium-vector/smiling-face-emoji_1319-431.jpg?w=360', 'age': 9002}]

    return render_template('index.html', names=staff)

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/hi')
def hi():
    return render_template('contact.html')