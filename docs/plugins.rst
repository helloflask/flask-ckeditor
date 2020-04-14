Advanced Usage
===============

Image Upload
-------------

CKEditor >= 4.5
################

The built-in CKEditor package includes a `File
Browser <https://ckeditor.com/addon/filebrowser>`__ plugin. With this plugin,
you can upload and insert images with the image widget. You need to set
``CKEDITOR_FILE_UPLOADER`` to the URL or endpoint which handles uploading
files, and the upload view must return ``upload_success()`` call with
the url of the uploaded image. Usually, you also need to validate the uploaded
image, then you can use ``upload_fail()`` to return an error message
with the ``message`` argument. If ``message`` was ``None``, the value in 
the configuration variable ``CKEDITOR_UPLOAD_ERROR_MESSAGE`` will be used, 
defaults to ``Upload failed.``. Here is the full example:

.. code-block:: python

   from flask_ckeditor import upload_success, upload_fail

   app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'  # this value can be endpoint or url

   @app.route('/files/<path:filename>')
   def uploaded_files(filename):
       path = '/the/uploaded/directory'
       return send_from_directory(path, filename)

   @app.route('/upload', methods=['POST'])
   def upload():
       f = request.files.get('upload')
       # Add more validations here
       extension = f.filename.split('.')[-1].lower()
       if extension not in ['jpg', 'gif', 'png', 'jpeg']:
           return upload_fail(message='Image only!')
       f.save(os.path.join('/the/uploaded/directory', f.filename))
       url = url_for('uploaded_files', filename=f.filename)
       return upload_success(url=url)  # return upload_success call

.. note:: The key passed to ``request.files.get()`` must be ``'upload'``,
it's defined by CKEditor and it's not the name of the view function.

In the template, you have to call ``ckeditor.config()`` to make the configuration work:

.. code-block:: jinja

    {{ ckeditor.config() }}

.. tip::
    When using Flask-WTF/WTForms, you have to pass the field name as
    ``name`` in ``ckeditor.config()``, for example ``ckeditor.config(name='description')``. 
    If you create the CKEditor through ``ckeditor.create()``, the default value (``ckeditor``) 
    will be used.

Now you will find the ``Upload`` tab appear in the image widget. Besides,
you can drag and drop the image directly into the editor area or copy and
paste the image (CKEditor >= 4.5).

.. tip:: Check the demo application at ``examples/image-upload/``.


CKEditor < 4.5
###############

If the CKEditor version you use is below 4.5, you will need to use ``@ckeditor.uploader`` to decorate the view function that handles the file upload. The upload view must return the url of the uploaded image. For example:

.. code-block:: python

    from flask import send_from_directory

    app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'  # this value can be endpoint or url
    
    @app.route('/files/<filename>')
    def uploaded_files(filename):
        path = '/the/uploaded/directory'
        return send_from_directory(path, filename)
    
    @app.route('/upload', methods=['POST'])
    @ckeditor.uploader
    def upload():
        f = request.files.get('upload')
        f.save(os.path.join('/the/uploaded/directory', f.filename))
        url = url_for('uploaded_files', filename=f.filename)
        return url

You can use the configuration variable ``CKEDITOR_UPLOAD_ERROR_MESSAGE`` to customize the error message when the upload failed, it defaults to ``Upload failed.``

.. note:: The key passed to ``request.files.get()`` must be ``'upload'``,
it's defined by CKEditor and it's not the name of the view function.

In the template, you have to call ``ckeditor.config()`` to make the configuration work:

.. code-block:: jinja

    {{ ckeditor.config() }}

.. tip::
    When using Flask-WTF/WTForms, you have to pass the field name as
    ``name`` in ``ckeditor.config()``, for example ``ckeditor.config(name='description')``. 
    If you create the CKEditor through ``ckeditor.create()``, the default value (``ckeditor``) will be used.

Now you will find the ``Upload`` tab appear in the image widget.


CSRF Protection for Image Upload
--------------------------------

Required version: CKEditor >= 4.9.0

The CSRF Protection feature was provided by Flask-WTF's ``CSRFProtect``
extension, so you have to install Flask-WTF first:

.. code-block:: bash

    $ pip install flask-wtf

Then initialize the CSRFProtect extension:

.. code-block:: python

    from flask_wtf.csrf import CSRFProtect

    app = Flask(__name__)

    # the secret key used to generate CSRF token
    app.config['SECRET_KEY'] = 'dev key'

    # enable CSRF protection
    app.config['CKEDITOR_ENABLE_CSRF'] = True

    csrf = CSRFProtect(app)

Make sure to set the secret key and set ``CKEDITOR_ENABLE_CSRF`` to True. Now all the image upload requests will be protected!


Code Snippet Highlight
------------------------

The built-in CKEditor package includes a `Code Snippet <https://ckeditor.com/addon/codesnippet>`__ plugin. You need to set ``CKEDITOR_ENABLE_CODESNIPPET`` to ``True`` to enable it. You can set the code theme through the configuration option ``CKEDITOR_CODE_THEME``. The default theme is ``monokai_sublime``. See all available themes and the list of valid theme strings on `this page <https://sdk.ckeditor.com/samples/codesnippet.html>`__.

Another step is to load code theme resources on the page you want to display the text in:

.. code-block:: jinja

   <head>
       ...
       {{ ckeditor.load_code_theme() }}
   </head>

Check the demo application at ``examples/codesnippet/``.
