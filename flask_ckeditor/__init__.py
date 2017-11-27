# -*- coding: utf-8 -*-
from flask import current_app, Markup, Blueprint, url_for, request
from flask_ckeditor.fields import CKEditorField


class _CKEditor(object):
    """The class that implement extension funciton.
    """
    @staticmethod
    def load(custom_url=None, pkg_type=None, version='4.7.3'):
        """Load CKEditor resource from CDN or local.

        :param custom_url: The custom resoucre url to use.
        :param pkg_type: The type of CKEditor package, one of `basic`, 
        `standard` and `full`. Default to 'standard'.
        :param version: The version of CKEditor.
        """
        if pkg_type is None:
            pkg_type = current_app.config['CKEDITOR_PKG_TYPE']
        if current_app.config['CKEDITOR_SERVE_LOCAL']:
            return Markup('<script src="%s"></script>' %
                url_for('ckeditor.static', filename='%s/ckeditor.js' % pkg_type))
        if custom_url:
            return Markup('<script src="%s"></script>' % custom_url)
        return Markup('''
<script src="//cdn.ckeditor.com/%s/%s/ckeditor.js"></script>'''
 % (version, pkg_type))

    def config(self):
        """Config CKEditor.
        """
        pass

    @staticmethod
    def create():
        """Create a ckeditor textarea directly.
        """
        return Markup('<textarea class="ckeditor" name="ckeditor"></textarea>')


def random_filename(old_filename):
    ext = os.path.splitext(old_filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


class CKEditor(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        blueprint = Blueprint('ckeditor', __name__,
            static_folder='static',
            static_url_path=app.static_url_path + '/ckeditor',)
        app.register_blueprint(blueprint)

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['ckeditor'] = _CKEditor()
        app.context_processor(self.context_processor)

        app.config.setdefault('CKEDITOR_SERVE_LOCAL', False)
        app.config.setdefault('CKEDITOR_PKG_TYPE', 'standard')
        app.config.setdefault('CKEDITOR_AUTO_HEIGHT', False)
        app.config.setdefault('CKEDITOR_HEIGHT', None)

    @staticmethod
    def context_processor():
        return {'ckeditor': current_app.extensions['ckeditor']}

    @staticmethod
    def uploader(func):
        def wrapper(*args, **kwargs):
            func_num = request.args.get('CKEditorFuncNum') 
            ckeditor = request.args.get('CKEditor') 
            lang_code = request.args.get('langCode')
            message = ''
            url = func(*args, **kwargs)
            return Markup('''
<script type="text/javascript">
window.parent.CKEDITOR.tools.callFunction(%s, "%s", "%s");</script>'''
% (func_num, url, message))
        return wrapper
