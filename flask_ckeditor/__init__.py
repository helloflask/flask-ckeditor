from jinja2 import Markup
from flask import current_app
from flask_ckeditor.flelds import *


class _ckeditor(object):
    def include_ckeditor(self):
        return Markup('''
<script src="//cdn.ckeditor.com/4.6.2/standard/ckeditor.js"></script>''')


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
