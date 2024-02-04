from flask import Flask, render_template, request, redirect, request, url_for
from threading import Thread

app = Flask(__name__)

try:
    with open('posts.txt', 'r', encoding='utf-8') as f:
        posts = [eval(post) for post in f.readlines()]
except FileNotFoundError:
    posts = []

@app.route('/')
def home():
    return render_template('home.html', posts=posts)

@app.route('/post', methods=['POST'])
def post():
    title = request.form.get('title')
    content = request.form.get('content')
    posts.append({'title': title, 'content': content})

    with open('posts.txt', 'w', encoding='utf-8') as f:
        for post in posts:
            f.write(str(post) + "\n")

    return render_template('home.html', posts=posts)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    if 0 < post_id <= len(posts):
        return render_template('post.html', post=posts[post_id - 1])
    return "게시글을 찾을 수 없습니다.", 404

@app.errorhandler(404)
def not_found_error(error):
  return """
    <pre>
    \       What a maze!        /
     \                         /
      \    This page does     /
       ]     not exist.      [    ,'|
       ]                     [   /  |
       ]___               ___[ ,'   |
       ]  ]\             /[  [ |:   |
       ]  ] \           / [  [ |:   |
       ]  ]  ]         [  [  [ |:   |
       ]  ]  ]__     __[  [  [ |:   |
       ]  ]  ] ]\ _ /[ [  [  [ |:   |
       ]  ]  ] ] (#) [ [  [  [ :===='
       ]  ]  ]_].nHn.[_[  [  [
       ]  ]  ]  HHHHH. [  [  [
       ]  ] /   `HH("N  \ [  [
       ]__]/     HHH  "  \[__[
       ]         NNN         [
       ]         N/"         [
       ]         N H         [
      /          N            \
     /           q,            \
    /                           \
    </pre>
    """

if __name__ == '__main__':
    app.run(debug=True)
def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()
