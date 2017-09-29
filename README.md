# Flask-CKEditor

Implementation of [CKEditor](https://ckeditor.com/) for WTForms/Flask-WTF.

Flask-CKEditor provides a `CKEditorField` class to render a CKEditor textarea.

## Installation

    $ pip install flask-ckeditor

## Initialize

The extension needs to be initialized in the usual way before it can be used:

    from flask_ckeditor import CKEditor
    
    app = Flask(__name__)
    ckeditor = CKEditor(app)

In the template which you want to put a CKEditor textarea, add this line in `<head></head>`:

    {{ ckeditor.load() }}

## How it work?

Here is a simple example. You can defined a form class with Flask-WTF just like normal. Then import the CKEditorField provided by Flask-CKEditor and use it like `StringField`:

    from flask_wtf import FlaskForm
    from flask_ckeditor import CKEditorField
    from wtforms import StringField, SubmitField
    
    class PostForm(FlaskForm):
		title = StringField('Title')
		body = CKEditorField('Body')
		submit = SubmitField('Submit')

## Try the live example

Open a terminal, type the commands below one by one:

	$ git clone https://github.com/greyli/flask-ckeditor
	$ cd flask-ckeditor
	$ pip install -r requirements.txt
	$ python app.py

Then go to http://127.0.0.1:5000 with your favourite browser.

## Changelog

### 0.2

Release date: 2017/9/29

- Add example and basic documentation.
- Add support to custom version and pakage type.
- Import CKEditorField directly from `flask_ckeditor`.
- Change `include_ckeditor()` to `load()`.

### 0.1

Initialize release.


