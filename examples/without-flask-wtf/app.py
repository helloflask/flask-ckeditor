# -*- coding: utf-8 -*-
"""
    :author: Grey Li <withlihui@gmail.com>
    :copyright: (c) 2017 by Grey Li.
    :license: MIT, see LICENSE for more details.
"""
from flask import Flask, render_template, request

from flask_ckeditor import CKEditor

app = Flask(__name__)
app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_HEIGHT'] = 400

app.secret_key = 'secret string'

ckeditor = CKEditor(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('ckeditor')
        # You may need to store the data in database here
        return render_template('post.html', title=title, body=body)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
