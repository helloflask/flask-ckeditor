Changelog
=========

1.0.0
-----

Release date: 2024/7/5

Since CKEditor 4 is no longer maintained, this release is the last major release of Flask-CKEditor.

There will be no new features added to this package, only bug fixes will be provided.

- Add ``cleanify`` function to ``flask_ckeditor.utils`` for HTML sanitization.
- Disable the version check for old CKEditor versions.
- Update the default CDN library version to 4.22.1.
- Drop Python 3.7 support and add 3.12 support.

0.5.1
-----

Release date: 2023/11/27

- Make WTForms an optional dependency.


0.5.0
-----

Release date: 2023/10/12

- Drop Python 2 and 3.6 support.
- Migrate from Travis CI to GitHub Actions.
- Remove the deprecated ``codesnippet`` argument in ``ckeditor.config()``.
- Fix the compatibility issue with Flask 3.0 version.
- Add message parameter to ``upload_success`` callback to support custom warning message.


0.4.6
-----

Release date: 2021/4/25

- Support to pass ``standard-all`` and ``full-all`` as CKEditor package type.


0.4.5
-----

Release date: 2021/4/24

- Fix unnecessary "ckeditor" class when using ``ckeditor.config()``.

0.4.4.1
-------

Release date: 2020/4/28

- Fix project description.


0.4.4
-----

Release date: 2020/4/19

- Upgrade CKEditor from 4.9.2 to 4.14.0.
- Fix multiple minor bugs.
- Fix documentation.


0.4.3
-----

Release date: 2018/11/8

- Add CSRF protect support for image uplaoding, based on Flask-WTF (CSRFProtect).


0.4.2
-----

Release date: 2018/8/24

- Add documentation.
- Remove built-in support for markdown plugin since it's unmaintained and not work with CKEditor > 4.6.
- Rename argument ``codesnippet`` to ``enable_codesnippet`` in ``ckeditor.config()``.
- Add ``serve_local`` argument for ``ckeditor.load()``.

0.4.1
-----

Release date: 2018/6/8

-  Change built-in resource’s url path to ``ckeditor/static/...`` to
   prevent conflict with user’s static path.


0.4.0
-----

Release date: 2018/5/29

-  Add basic unit test.
-  Update resources, fix plugin register bug, use CKEditor 4.9.2.
-  Add configuration parameter ``CKEDITOR_ENABLE_CODESNIPPET``, used to
   enable/disable ``Code Snippet`` plugin.
-  Added Markdown plugin into built-in resouce, enabled markdown mode
   via ``CKEDITOR_ENABLE_MARKDOWN``.
-  Added configuration parameter ``CKEDITOR_EXTRA_PLUGINS``, a list used
   to register extra plugins.


0.3.3
-----

Release date: 2018/2/4

-  Added support to set ``name`` and ``value`` when using
   ``ckeditor.create()``.


0.3.2
-----

Release date: 2018/1/15

-  Fixed built-in resources bug.


0.3.1
-----

Release date: 2018/1/13

-  The value of ``CKEDITOR_FILE_UPLOADER``, ``CKEDITOR_FILE_BROWSER``,
   ``file_uploader`` and ``file_browser`` in ``ckeditor.config()`` can
   be URL or endpoint.
-  Change ``CKEDITOR_FILE_UPLOAD_URL`` to ``CKEDITOR_FILE_UPLOADER``.
-  Change ``CKEDITOR_FILE_BROWSER_URL`` to ``CKEDITOR_FILE_BROWSER``.
-  Change ``ckeditor.config(file_upload_url)`` to
   ``ckeditor.config(file_uploader)``.
-  Change ``ckeditor.config(file_browser_url)`` to
   ``ckeditor.config(file_browser)``.


0.3
---

Release date: 2017/12/4

-  Set custom resource url with ``custom_url`` argument in ``load()``.
-  Added support for configuration, ``config()`` method used to load
   config.
-  Added support to upload image.
-  Added local resources, it can be enabled with
   ``CKEDITOR_SERVE_LOCAL``, default to ``False``.


0.2
---

Release date: 2017/9/29

-  Added example and basic documentation.
-  Added support to custom version and pakage type.
-  Import CKEditorField directly from ``flask_ckeditor``.
-  Change ``include_ckeditor()`` to ``load()``.


0.1
---

Initialize release.
