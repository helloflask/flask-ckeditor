Advanced
=========


Image Upload
-------------

The bulit-in CKEditor package include a `File
Browser <ckeditor.com/addon/filebrowser>`__ plugin. With this plugin,
you can upload and insert image with image widget. You need set
``CKEDITOR_FILE_UPLOADER`` to the URL or endpoint which handle upload
files, and the upload view must return ``upload_success()`` call with
the uploaded image's url. Usually, you also need to validate uploaded
image, then you can use ``upload_fail()`` to return a error message
(with ``message`` argument). For example:

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
       if extension not in ['jpg', 'gif', 'png', 'jpeg']:
           return upload_fail(message='Image only!')
       f.save(os.path.join('/the/uploaded/directory', f.filename))
       url = url_for('uploaded_files', filename=f.filename)
       return upload_success(url=url)  # return upload_success call

.. note:: The key pass to ``request.files.get()`` must be ``'upload'``,
it's defined by CKEditor and it's not the name of the view function.**

In the template, you have to call ``ckeditor.config()`` to make configuration work:

.. code-block:: html

    {{ ckeditor.config() }}


Now you will find the ``Upload`` tab appear in image widget. Besides,
you can drag and drop image directly into the editor area or copy and
paste the image (CKEditor >= 4.5).

.. tip:: Check the demo application at ``examples/image-upload/``.

Code Snippet Highlight
------------------------

The bulit-in CKEditor package include a `Code
Snippet <ckeditor.com/addon/codesnippet>`__ plugin. You need to set
``CKEDITOR_ENABLE_CODESNIPPET`` to ``True`` to enable it. You can set
the code theme through configuration option ``CKEDITOR_CODE_THEME``. The
default theme was ``monokai_sublime``. See all available themes and the
list of valid theme string on `this
page <https://sdk.ckeditor.com/samples/codesnippet.html>`__.

Another step was load code theme resources in the page you want to
display the text:

.. code:: html

   <head>
       ...
       {{ ckeditor.load_code_theme() }}
   </head>

Check the demo application at ``examples/codesnippet/``.

Markdown Mode
--------------

.. warning:: This plugin did not compitable with CKEditor after 4.6.1, do not enable it until
`#22 <https://github.com/hectorguo/CKEditor-Markdown-Plugin/issues/22>`_ was fixed.

Since 0.3.4, the bulit-in CKEditor package included a
`Markdown <ckeditor.com/addon/markdown>`__ plugin. You can set
``CKEDITOR_ENABLE_MARKDOWN`` to ``True`` to eanble Markdown mode.

.. tip:: Check the demo application at ``examples/markdown/``.