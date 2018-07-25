
Configuration
=============

Register Configuration
-----------------------

Except ``CKEDITOR_SERVE_LOCAL`` and ``CKEDITOR_PKG_TYPE``, when you use other configuration variabel,
you have to call ``ckeditor.config()`` in template to make them register with CKEditor:

.. code:: html

   <body>
       ...
       {{ ckeditor.config() }}
   </body>


.. tip::
    When using Flask-WTF/WTForms, you have to pass the field name as
    ``name`` in ``ckeditor.config()``. If you create the CKEditor through
    ``ckeditor.create()``, the default value (e.g. ``ckeditor``) will be
    used.

Available Configuration
------------------------

The configuration options available were listed below:

============================ ====================== ======================================================================================================================================================================
            Name                  Default Value                                                         Info
============================ ====================== ======================================================================================================================================================================
CKEDITOR_SERVE_LOCAL         ``False`` 	            Flag used to set serve resources from local when use ``ckeditor.load()``, default to retrieve from CDN.
CKEDITOR_PKG_TYPE 	         ``'standard'`` 	    The package type of CKEditor, one of ``basic``, ``standard`` and ``full``.
CKEDITOR_LANGUAGE 	         ``None`` 	            The lang code string to set UI language in ISO 639 format, for example: ``zh``, ``en``, ``jp`` etc. Leave it unset to enable auto detection by user's browser setting.
CKEDITOR_HEIGHT 	         CKEditor default      	The height of CKEditor textarea, in pixel.
CKEDITOR_WIDTH 	             CKEditor default      	The width of CKEditor textarea, in pixel.
CKEDITOR_FILE_UPLOADER 	     ``None`` 	            The URL or endpoint that handle file upload.
CKEDITOR_FILE_BROWSER 	     ``None`` 	            The URL or endpoint that handle file browser.
CKEDITOR_ENABLE_MARKDOWN 	 ``False`` 	            Flag used to enable markdown plugin, the plugin must be installed (included in built-in resources).
CKEDITOR_ENABLE_CODESNIPPET  ``False`` 	            Flag used to enable codesnippet plugin, the plugin must be installed (included in built-in resources).
CKEDITOR_CODE_THEME 	     ``'monokai_sublime'`` 	Set code snippet highlight theme when codesnippet plugin was enabled.
CKEDITOR_EXTRA_PLUGINS 	     ``[]`` 	            A list of extra plugins used in CKEditor, the plugins must be installed.
============================ ====================== ======================================================================================================================================================================


Custom Configuration String
----------------------------

In addition, you can pass custom settings with ``custom_config``
argument:

.. code:: html

   {{ ckeditor.config(name='body', custom_config="uiColor: '#9AB8F3'") }}

Keep it mind that the proper syntax for each option is
``configuration name : configuration value``. You can use comma to
separate multiple key-value pairs. See the list of available
configuration settings on `CKEditor
documentation <https://docs.ckeditor.com/ckeditor4/docs/#!/api/CKEDITOR.config%3E>`__.
