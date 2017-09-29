# -*- coding: utf-8 -*-
from flask import current_app, Markup
from flask_ckeditor.fields import CKEditorField


class _ckeditor(object):
    def load(self, pkg_type='standard', version='4.7.3'):
        """Load CKEditor resource from CDN.

        :param pkg_type: The type of CKEditor package, one of `basic`, `standard` and `full`. 
        :param version: The version of CKEditor.
        """
        return Markup('''
<script src="//cdn.ckeditor.com/%s/%s/ckeditor.js"></script>'''
 % (version, pkg_type))


class CKEditor(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['ckeditor'] = _ckeditor()
        app.context_processor(self.context_processor)

    @staticmethod
    def context_processor():
        return {'ckeditor': current_app.extensions['ckeditor']}
