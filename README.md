# Flask-CKEditor

**WARNING: This project is under active development. Nothing is set in stone at this point of time.**

CKEditor integration for Flask, including image upload, code syntax highlight, Markdown mode and more.

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

In the template which you want to put a CKEditor textarea, add this line in `<head></head>` or before `</body>`:

```python
<body>
    ...
    {{ ckeditor.load() }}
</body>
```
You can use `custom_url` to load your custom CKEditor build:
```python
{{ ckeditor.load(custom_url=url_for('static', filename='ckeditor/ckeditor.js')) }}
```

## How it work?

Here is a simple example. You can defined a form class with Flask-WTF/WTForms just like normal. Then import
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

Check the demo application at `examples/basic/` and `examples/without-flask-wtf`.

## Configuration

You can load settings for CKEditor with `config()` method in Jinja2 template, after the `load()` call:

```html
<body>
    ...
    {{ ckeditor.load() }}
    {{ ckeditor.config(name='body') }}
</body>
```

When using Flask-WTF/WTForms, you have to pass the field name as `name` in `ckeditor.config()`.
If you create the CKEditor through `ckeditor.create()`, the default value (e.g. `ckeditor`) will be used.

The configuration options available were listed below:

- CKEDITOR_SERVE_LOCAL
- CKEDITOR_PKG_TYPE
- CKEDITOR_LANGUAGE
- CKEDITOR_HEIGHT
- CKEDITOR_WIDTH
- CKEDITOR_CODE_THEME
- CKEDITOR_FILE_UPLOADER
- CKEDITOR_FILE_BROWSER
- CKEDITOR_ENABLE_MARKDOWN
- CKEDITOR_ENABLE_CODESNIPPET
- CKEDITOR_EXTRA_PLUGINS

In addition, you can pass custom settings with `custom_config` argument:

```python
{{ ckeditor.config(name='body', custom_config="uiColor: '#9AB8F3'") }}
```

Keep it mind that the proper syntax for each option is ``configuration name : configuration value``.
You can use comma to separate multiple key-value pairs. See the list of available configuration 
settings on [CKEditor documentation](https://docs.ckeditor.com/ckeditor4/docs/#!/api/CKEDITOR.config>).

## Image Upload

The bulit-in CKEditor package include a [File Browser](ckeditor.com/addon/filebrowser)
plugin. With this plugin, you can upload and insert image with image widget.
You need set `CKEDITOR_FILE_UPLOADER` to the URL or endpoint which handle
upload files, and the upload view must return `upload_success()` call with the uploaded
image's url. Usually, you also need to validate uploaded image,
then you can use `upload_fail()` to return a error message (with `message` argument). For example:

```python
from flask_ckeditor import upload_success, upload_fail

app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'

@app.route('/files/<path:filename>')
def uploaded_files(filename):
    path = '/the/uploaded/directory'
    return send_from_directory(path, filename)

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    # Add more validations here
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    f.save(os.path.join('/the/uploaded/directory', f.filename))
    url = url_for('uploaded_files', filename=f.filename)
    return upload_success(url=url)  # return upload_success call
```

Now you will find the `Upload` tab appear in image widget. Besides, you can drag
and drop image directly into the editor area or copy and paste the image (CKEditor >= 4.5).

Check the demo application at `examples/image-upload/`.

## Code Snippet Highlight

The bulit-in CKEditor package include a [Code Snippet](ckeditor.com/addon/codesnippet) plugin. 
You need to set `CKEDITOR_ENABLE_CODESNIPPET` to `True` to enable it.
You can set the code theme through configuration option `CKEDITOR_CODE_THEME`.
The default theme was `monokai_sublime`. See all available themes and the
list of valid theme string on [this page](https://sdk.ckeditor.com/samples/codesnippet.html).

Another step was load code theme resources in the page you want to display the text:

```html
<head>
    ...
    {{ ckeditor.load_code_theme() }}
</head>
```

Check the demo application at `examples/codesnippet/`.

## Markdown Mode

Since 0.3.4, the bulit-in CKEditor package included a [Markdown](ckeditor.com/addon/markdown) plugin. 
You can set `CKEDITOR_ENABLE_MARKDOWN` to `True` to eanble Markdown mode.

Check the demo application at `examples/markdown/`.

## Try Examples

Open a terminal, type the commands below one by one:

```bash
$ git clone https://github.com/greyli/flask-ckeditor
$ cd flask-ckeditor/examples
$ pip install -r requirements.txt
$ python basic/app.py
```

Then go to http://127.0.0.1:5000 with your favourite browser.

Aside from the basic example, there are four additional examples:

- examples/image-upload: This example demonstrate how to support image upload in Flaks-CKEditor.
- examples/codesnippet: This example demonstrate how to use Code Snippet plugin.
- examples/without-flask-wtf: This example demonstrate how to use CKEditor without Flask-WTF.
- examples/markdown: This example demonstrate how to use add Markdown plugin.

## TODO
- [ ] Documentation
- [ ] Integrate with a file browser
- [ ] CSRF protection for image upload

## Changelog

### 0.4.1

Release date: 2018/6/8

- Change built-in resource's url path to `ckeditor/static/...` to prevent conflict with user's static path.


### 0.4.0

Release date: 2018/5/29

- Add basic unit test.
- Update resources, fix plugin register bug, use CKEditor 4.9.2.
- Add configuration parameter `CKEDITOR_ENABLE_CODESNIPPET`, used to enable/disable `Code Snippet` plugin.
- Added Markdown plugin into built-in resouce, enabled markdown mode via `CKEDITOR_ENABLE_MARKDOWN`.
- Added configuration parameter `CKEDITOR_EXTRA_PLUGINS`, a list used to register extra plugins.

### 0.3.3

Release date: 2018/2/4

- Added support to set `name` and `value` when using `ckeditor.create()`.


### 0.3.2

Release date: 2018/1/15

- Fixed built-in resources bug.

### 0.3.1

Release date: 2018/1/13

- The value of `CKEDITOR_FILE_UPLOADER`, `CKEDITOR_FILE_BROWSER`, `file_uploader`
and `file_browser` in `ckeditor.config()` can be URL or endpoint.
- Change `CKEDITOR_FILE_UPLOAD_URL` to `CKEDITOR_FILE_UPLOADER`.
- Change `CKEDITOR_FILE_BROWSER_URL` to `CKEDITOR_FILE_BROWSER`.
- Change `ckeditor.config(file_upload_url)` to `ckeditor.config(file_uploader)`.
- Change `ckeditor.config(file_browser_url)` to `ckeditor.config(file_browser)`.

### 0.3

Release date: 2017/12/4

- Set custom resource url with `custom_url` argument in `load()`.
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
