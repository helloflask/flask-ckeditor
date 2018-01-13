# -*- coding: utf-8 -*-
import os

from flask import Flask, render_template, request, Markup, url_for, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from flask_ckeditor import CKEditor, CKEditorField

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_HEIGHT'] = 400
app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'
app.config['UPLOADED_PATH'] = basedir + '/uploads'

app.secret_key = 'secret string'

ckeditor = CKEditor(app)

class PostForm(FlaskForm):
	title = StringField('Title')
	body = CKEditorField('Body', validators=[DataRequired()])
	submit = SubmitField()


@app.route('/', methods=['GET', 'POST'])
def index():
	form = PostForm()
	if form.validate_on_submit():
		title = form.title.data
		body = form.body.data
		# You may need to store the data in database here
		return render_template('post.html', title=title, body=body)
	return render_template('index.html', form=form)


@app.route('/files/<filename>')
def files(filename):
	path = app.config['UPLOADED_PATH']
	return send_from_directory(path, filename)


@app.route('/upload', methods=['POST'])
@ckeditor.uploader
def upload():
	f = request.files.get('upload')
	f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
	url = url_for('files', filename=f.filename)
	return url


if __name__ == '__main__':
	app.run(debug=True)
