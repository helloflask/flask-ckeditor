# Flask-CKEditor

CKEditor integration for Flask, including image upload, code syntax highlight and more.

## Installation

```bash
$ pip install flask-ckeditor
```

## Initialize

The extension needs to be initialized in the usual way before it can be used:

```python
from flask_ckeditor import CKEditor

app = Flask(__name__)
ckeditor = CKEditor(app)
```

In the template which you want to put a CKEditor textarea, add this line in `<head></head>`:

```python
{{ ckeditor.load() }}
```

## How it work?

Here is a simple example. You can defined a form class with Flask-WTF just like normal. Then import
the CKEditorField provided by Flask-CKEditor and use it like `StringField`:

```python
from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, SubmitField

class PostForm(FlaskForm):
	title = StringField('Title')
	body = CKEditorField('Body')
	submit = SubmitField('Submit')
```

Instead, you can also create the CKEditor textarea manually through `create()` method:

```html
<form method="post">
{{ ckeditor.create() }}
<input type="submit">
</form>
```

## Configuration

You can load settings for CKEditor with `config()` method in Jinja2 template:

```html
<body>
    ...
    {{ ckeditor.config(name='body') }}
</body>
```

When using Flask-WTF, you have to pass the field name as `name` in `ckeditor.config()`.
If you create the CKEditor through `ckeditor.create()`, the default value will be used.

The configuration options available were listed below:

- CKEDITOR_SERVE_LOCAL
- CKEDITOR_PKG_TYPE
- CKEDITOR_LANGUAGE
- CKEDITOR_HEIGHT
- CKEDITOR_WIDTH
- CKEDITOR_CODE_THEME
- CKEDITOR_FILE_UPLOAD_URL
- CKEDITOR_FILE_BROWSER_URL

In addition, you can pass custom settings with `custom_config` argument:

```python
{{ ckeditor.config(name='body', custom_config="uiColor: '#9AB8F3'") }}
```

Keep it mind that the proper syntax for each option is ``configuration name : configuration value``.
You can use comma to separate multiple key-value pairs. See the list of available configuration 
settings on [CKEditor documentation](https://docs.ckeditor.com/ckeditor4/docs/#!/api/CKEDITOR.config>).

## Image upload

The image can be uploaded with image widget. When you set `CKEDITOR_FILE_UPLOAD_URL`
with proper value, you will see the upload tab appear in image widget. You need to use `ckeditor.uploader`
to decorate the view function that handle the file upload. And, The upload view must return the uploaded 
image's url. For example:

```python
app.config['CKEDITOR_FILE_UPLOAD_URL'] = '/upload'

@app.route('/files/<filename>')
def files(filename):
    path = '/the/uploaded/directory'
    return send_from_directory(path, filename)

@app.route('/upload', methods=['POST'])
@ckeditor.uploader
def upload():
    f = request.files.get('upload')
    f.save(os.path.join('/the/uploaded/directory', f.filename))
    url = url_for('files', filename=f.filename)
    return url
```

Check the complete applicaiton at `examples/image-upload`. When you start the application, you can click
the image icon, then you will find a `Upload` tab.

## Code Snippet Highlight

The bulit-in CKEditor package include a [Code Snippet](ckeditor.com/addon/codesnippet)plugin. 
You can set the code theme through configuration option `CKEDITOR_CODE_THEME`. The default theme was 
`monokai_sublime`. See all available themes at [Highlight.js's demo page](https://highlightjs.org/static/demo/), and
the list of valid theme string can be find on this [page](https://sdk.ckeditor.com/samples/codesnippet.html).

Another step was load code theme resources in the page you want to display the text:

```html
<head>
    ...
    {{ ckeditor.load_code_theme() }}
</head>
```

## Try Examples

Open a terminal, type the commands below one by one:

```bash
$ git clone https://github.com/greyli/flask-ckeditor
$ cd flask-ckeditor/examples/basic
$ pip install -r requirements.txt
$ python app.py
```

Then go to http://127.0.0.1:5000 with your favourite browser.

Aside from the basic example, there are two additional examples:

- examples/image-upload: This example demonstrate how to support image upload in Flaks-CKEditor.
- examples/without-flask-wtf: This example demonstrate how to use CKEditor without Flask-WTF.

## TODO
- [ ] Documentation
- [ ] Test
- [ ] Markdown mode
- [ ] Integrate with a file browser

## Changelog

### 0.3

Release date: 2017/12/4.

- Set custom resource url with `custom_url` arguemnt in `load()`.
- Added support for configuration, `config()` method used to load config.
- Added support to upload image.
- Added local resources, it can be enabled with `CKEDITOR_SERVE_LOCAL`, default to `False`.

### 0.2

Release date: 2017/9/29

- Added example and basic documentation.
- Added support to custom version and pakage type.
- Import CKEditorField directly from `flask_ckeditor`.
- Change `include_ckeditor()` to `load()`.

### 0.1

Initialize release.
