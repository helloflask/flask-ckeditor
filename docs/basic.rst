Basic Usage
============

Installation
-------------

.. code-block:: bash

   $ pip install flask-ckeditor

Initialization
--------------

This extension needs to be initialized in the usual way before it can be
used:

.. code-block:: python

   from flask_ckeditor import CKEditor

   app = Flask(__name__)
   ckeditor = CKEditor(app)


This extension also supports the Flask application factory pattern by allowing you to create
a CKEditor object and then separately initialize it for an app:

.. code-block:: python

    from flask_ckeditor import CKEditor

    ckeditor = CKEditor()

    def create_app():
        app = Flask(__name__)
        ...
        ckeditor.init_app(app)
        ...
        return app

Include CKEditor Resources
--------------------------

In the template in which you want to put a CKEditor textarea, call ``ckeditor.load()``
in ``<head></head>`` or before ``</body>``:

.. code-block:: jinja

   <body>
       ...
       {{ ckeditor.load() }}
   </body>

By default, it will load the CKEditor resources from CND (cdn.ckeditor.com), you can set ``CKEDITOR_SERVE_LOCAL``
to True to use built-in resources. You can use ``custom_url`` to load your custom CKEditor build:

.. code-block:: jinja

   {{ ckeditor.load(custom_url=url_for('static', filename='ckeditor/ckeditor.js')) }}


CKEditor provides five types of preset (see `comparison table <https://ckeditor.com/cke4/presets-all>`_ for the differences):

- ``basic``
- ``standard`` (default value)
- ``full``
- ``standard-all`` (only available from CDN)
- ``full-all`` (only available from CDN)

You can use `pkg_type` parameter or ``CKEDITOR_PKG_TYPE`` configuration variable to set the package type. For example:

.. code-block:: jinja

   {{ ckeditor.load(pkg_type="basic") }}

Or:

.. code-block:: python

    app = Flask(__name__)
    app.config['CKEDITOR_PKG_TYPE'] = 'basic'
    ckeditor = CKEditor(app)

This method is just a helper to generate ``<script>`` to include CKEditor resources, you can also
write ``<script>`` element directly:

.. code-block:: html

    <script src="https://cdn.ckeditor.com/4.10.0/standard/ckeditor.js"></script>

Create a CKEditor Textarea
---------------------------

It's quite simple, just call ``ckeditor.create()`` in the template:

.. code-block:: jinja

   <form method="post">
       {{ ckeditor.create() }}
       <input type="submit">
   </form>

You can use ``value`` parameter to pass preset value (i.e. ``ckeditor.create(value='blah...blah...')``).

Get the Data
------------

Since the CKEditor textarea is just a normal ``<textarea>`` element, you can get the data
from ``request.form`` by passing ``ckeditor`` as key:

.. code-block:: python

    from flask import request, render_template

    @app.route('/write')
    def new_post():
        if request.method == 'POST':
            data = request.form.get('ckeditor')  # <--

        return render_template('index.html')

Clean the Data
--------------

It's recommended to sanitize the HTML input from user before saving it to the database.

The Flask-CKEditor provides a helper function `cleanify`. To use it, install the extra dependencies:

.. code-block:: bash

   $ pip install flask-ckeditor[all]

Then call it for your form data (you could use ``allowed_tags`` to pass a list of custom allowed HTML tags):

.. code-block:: python

    from flask import request, render_template
    from flask_ckeditor.utils import cleanify

    @app.route('/write')
    def new_post():
        if request.method == 'POST':
            data = cleanify(request.form.get('ckeditor'))  # <--

        return render_template('index.html')

Working with Flask-WTF/WTForms
-------------------------------

When using Flask-WTF/WTForms, you can import the ``CKEditorField``
provided by Flask-CKEditor and use it just like ``StringField``:

.. code-block:: python

   from flask_wtf import FlaskForm
   from flask_ckeditor import CKEditorField
   from wtforms import StringField, SubmitField

   class PostForm(FlaskForm):
       title = StringField('Title')
       body = CKEditorField('Body')  # <--
       submit = SubmitField('Submit')


One more step is to call ``ckeditor.config()`` and pass the CKEditorField attribute's name:

.. code-block:: jinja

    <form method="post">
       {{ form.title() }}
       {{ form.body() }}
       {{ form.submit() }}
   </form>

    {{ ckeditor.load() }}
    {{ ckeditor.config(name='body') }}
    </body>

In the view function, you can get the data either by ``request.form.get('body')`` or ``form.body.data``.


.. tip:: Check the demo application at ``examples/basic`` and ``examples/without-flask-wtf``.


Preset Value in CKEditor Textarea
----------------------------------

When you implement an edit feature for your CMS, you will need to get the article data from database, then preset the value
into the CKEditor textarea. First you need to pass the value into template:

.. code-block:: python

    @app.route('/edit')
    def edit_post():
        article_body = get_the_article_body_from_somewhere()
        return render_template('edit.html', article_body=article_body)

Then pass it to CKEditor with ``value`` parameter:

.. code-block:: jinja

   <form method="post">
       {{ ckeditor.create(value=article_body) }}
       <input type="submit">
   </form>

If you are using Flask-WTF/WTForms, it's even more simple, just pass the value to the form field's ``data`` attribute:

.. code-block:: python

    @app.route('/edit')
    def edit_post():
        form = EditForm()
        form.body.data = get_the_article_body_from_somewhere()  # <--
        return render_template('edit.html', form=form)
