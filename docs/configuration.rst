
Configuration
=============

Register Configuration
-----------------------

Except for ``CKEDITOR_SERVE_LOCAL`` and ``CKEDITOR_PKG_TYPE``, when you use other configuration variables,
you have to call ``ckeditor.config()`` in the template to make them register with CKEditor:

.. code-block:: jinja

   <body>
       ...  <!-- {{ ckeditor.load() }} or <script src="/path/to/ckeditor.js"> -->
       {{ ckeditor.config() }}
   </body>

When using Flask-WTF/WTForms, you have to pass the field name as ``name`` in ``ckeditor.config()``, for example:
 
 .. code-block:: jinja

   <body>
       ...  <!-- {{ ckeditor.load() }} or <script src="/path/to/ckeditor.js"> -->
       {{ ckeditor.config(name='description') }}
   </body>

When using Flask-Admin, the default form field name is ``text``, so normally you will use this:

 .. code-block:: jinja

   <body>
       ...  <!-- {{ ckeditor.load() }} or <script src="/path/to/ckeditor.js"> -->
       {{ ckeditor.config(name='text') }}
   </body>

If you create the CKEditor through ``ckeditor.create()``, the default value (``name='ckeditor'``) will be used.

Available Configuration
------------------------

The configuration options available are listed below:

=============================== ======================= =========================================================================================================================================================================
            Name                    Default Value                                                                                  Info
=============================== ======================= =========================================================================================================================================================================
CKEDITOR_SERVE_LOCAL             ``False``               Flag used to enable serving resources from local when use ``ckeditor.load()``, default is to retrieve from CDN.
CKEDITOR_PKG_TYPE                ``'standard'``          The package type of CKEditor, one of ``basic``, ``standard`` or ``full``.
CKEDITOR_LANGUAGE                ``None``                The lang code string to set UI language in ISO 639 format, for example: ``zh``, ``en``, ``jp`` etc. Leave it unset to enable auto detection by user's browser setting.
CKEDITOR_HEIGHT                  CKEditor default        The height of CKEditor textarea, in pixel.
CKEDITOR_WIDTH                   CKEditor default        The width of CKEditor textarea, in pixel.
CKEDITOR_FILE_UPLOADER           ``None``                The URL or endpoint that handles file upload.
CKEDITOR_FILE_BROWSER            ``None``                The URL or endpoint that handles file browser.
CKEDITOR_ENABLE_CODESNIPPET      ``False``               Flag used to enable codesnippet plugin, the plugin must be installed (included in built-in resources).
CKEDITOR_CODE_THEME              ``'monokai_sublime'``   Set code snippet highlight theme when codesnippet plugin was enabled.
CKEDITOR_EXTRA_PLUGINS           ``[]``                  A list of extra plugins used in CKEditor, the plugins must be installed.
CKEDITOR_ENABLE_CSRF             ``False``               Flag used to enable CSRF protection for image uploading, see :doc:`/plugins` for more details.
CKEDITOR_UPLOAD_ERROR_MESSAGE    ``'Upload failed.'``    Default error message for failed upload.
=============================== ======================= =========================================================================================================================================================================


Custom Configuration String
----------------------------

In addition, you can pass custom settings with ``custom_config``
argument:

.. code-block:: jinja

   {{ ckeditor.config(custom_config="uiColor: '#9AB8F3'") }}

Keep it mind that the proper syntax for each option is
``configuration name : configuration value``. You can use comma to
separate multiple key-value pairs. See the list of available
configuration settings on `CKEditor
documentation <https://ckeditor.com/docs/ckeditor4/latest/api/CKEDITOR_config.html>`_.

If you are using Flask-WTF/WTForms or Flask-Admin, remember to pass the form field name with ``name``:

 .. code-block:: jinja

   <body>
       ...  <!-- {{ ckeditor.load() }} or <script src="/path/to/ckeditor.js"> -->
       {{ ckeditor.config(name='description') }}  <!-- use name='text' for Flask-Admin -->
   </body>

Configuring Multiple Text Area
--------------------------------

If you need to create multiple text areas in one page, here are some tips:

Without Flask-WTF/WTForms
##########################

Create two text areas with different name and configure them with a unique name:

.. code-block:: jinja

    <h1>About me</h1>
    {{ ckeditor.create(name='bio') }}

    <h1>About my team</h1>
    {{ ckeditor.create(name='team') }}


    {{ ckeditor.load() }}

    {{ ckeditor.config(name='bio') }}
    {{ ckeditor.config(name='team') }}

With Flask-WTF/WTForms
#######################

When creating multiple forms with Flask-WTF/WTForms, you just need to create
multiple ``CKEditorField`` fields:

.. code-block:: python

   from flask_wtf import FlaskForm
   from flask_ckeditor import CKEditorField
   from wtforms import StringField, SubmitField

   class PostForm(FlaskForm):
       title = StringField('Title')
       bio = CKEditorField('About me')  # <--
       team = CKEditorField('About my team')  # <--
       submit = SubmitField('Submit')

In the template, you render them and configure them with the right name:

.. code-block:: jinja

    {{ form.bio() }}
    {{ form.team() }}
    {{ form.submit() }}

    {{ ckeditor.load() }}

    {{ ckeditor.config(name='bio') }}
    {{ ckeditor.config(name='team') }}


Overwriting Global Configurations
----------------------------------
Sometimes you may want to use a different configuration for multiple text areas, in this case, you can pass the specific keyword arguments into ``ckeditor.config()`` directly.

The keyword arguments should map the corresponding configuration variables in this way:

- CKEDITOR_LANGUAGE --> language
- CKEDITOR_WIDTH --> width
- CKEDITOR_FILE_UPLOADER --> file_uploader
- etc

example:

.. code-block:: jinja

    {{ ckeditor.config(lanuage='en', width=500) }}

In the end, the keyword argument you pass will overwrite the corresponding configurations.

Comparatively, you can use ``serve_local`` and ``pkg_type`` in ``ckeditor.load()`` to overwrite
``CKEDITOR_SERVE_LOCAL`` and ``CKEDITOR_PKG_TYPE``.
