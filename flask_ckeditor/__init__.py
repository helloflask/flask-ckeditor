# -*- coding: utf-8 -*-
from flask import current_app, Markup, Blueprint, url_for, request
from flask_ckeditor.fields import CKEditorField


class _CKEditor(object):
    """The class implement funcitons for Jinja2.
    """
    @staticmethod
    def load(custom_url=None, pkg_type=None, version='4.7.3'):
        """Load CKEditor resource from CDN or local.

        :param custom_url: The custom resoucre url to use, build your CKEditor
        on `CKEditor builder <https://ckeditor.com/cke4/builder>`_.
        :param pkg_type: The type of CKEditor package, one of ``basic``, 
        ``standard`` and ``full``. Default to ``standard``.
        :param version: The version of CKEditor.
        """
        if pkg_type is None:
            pkg_type = current_app.config['CKEDITOR_PKG_TYPE']
        if current_app.config['CKEDITOR_SERVE_LOCAL']:
            url = url_for('ckeditor.static', filename='%s/ckeditor.js' % pkg_type)
        else:
            url = '//cdn.ckeditor.com/%s/%s/ckeditor.js' % (version, pkg_type)
        if custom_url:
            url = custom_url
        return Markup('<script src="%s"></script>'% url)

    @staticmethod
    def config(language=None, height=None, width=None, code_theme=None,
               file_upload_url=None, file_browser_url=None, custom_config=''):
        """Config CKEditor.

        :param language: The lang code string to set UI language in ISO 639 format, one of 
        ``zh``, ``ko``, ``ja``, ``es``, ``fr``, ``de`` and ``en``, 
        default to ``en``(i.e. English).
        :param height: The heighe of CKEditor window, default to 200.
        :param width: The heighe of CKEditor window.
        :param code_theme: The theme's name in string used for code snippets, default to 
        ``monokai_sublime``.
        :param file_upload_url: The url to send the upload data. The releated view function 
        must be decorated with ``ckeditor.uploader`` and return the uploaded image's url. 
        For example::
            
            @app.route('/files/<filename>')
            def files(filename):
                path = app.config['UPLOADED_PATH']
                return send_from_directory(path, filename)

            @app.route('/upload', methods=['POST'])
            @ckeditor.uploader
            def upload():
                f = request.files.get('upload')
                f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
                url = url_for('files', filename=f.filename)
                return url
        
        :param file_browser_url: The url to link a file browser.
        :param custom_config: The addition config, for example ``uiColor: '#9AB8F3'``.
        The proper syntax for each option is ``configuration name : configuration value``.
        You can use comma to separate multiple key-value pairs. See the list of available
        configuration settings on
        `CKEditor documentation <https://docs.ckeditor.com/ckeditor4/docs/#!/api/CKEDITOR.config>`_.
        
        .. versionadded:: 0.3
        """
        language = language or current_app.config['CKEDITOR_LANGUAGE']
        height = height or current_app.config['CKEDITOR_HEIGHT']
        width = width or current_app.config['CKEDITOR_WIDTH']
        code_theme = code_theme or current_app.config['CKEDITOR_CODE_THEME']
        file_upload_url = file_upload_url or current_app.config['CKEDITOR_FILE_UPLOAD_URL']
        file_browser_url = file_browser_url or current_app.config['CKEDITOR_FILE_BROWSER_URL']
        return Markup('''
<script type="text/javascript">
        CKEDITOR.replace( 'ckeditor', {
            language: %r,
            height: %r,
            width: %r,
            toolbarCanCollapse: true,
            codeSnippet_theme: %r,
            filebrowserUploadUrl: %r,
            filebrowserBrowseUrl: %r,
            %s
        });
    </script>''' % (language, height, width, code_theme, file_upload_url, file_browser_url, custom_config))

    @staticmethod
    def create():
        """Create a ckeditor textarea directly.

        .. versionadded:: 0.3
        """
        return Markup('<textarea class="ckeditor" id="ckeditor" name="ckeditor"></textarea>')


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

        app.config.setdefault('CKEDITOR_LANGUAGE', '')
        app.config.setdefault('CKEDITOR_HEIGHT', '')
        app.config.setdefault('CKEDITOR_WIDTH', '')
        app.config.setdefault('CKEDITOR_CODE_THEME', 'monokai_sublime')
        app.config.setdefault('CKEDITOR_FILE_UPLOAD_URL', '')
        app.config.setdefault('CKEDITOR_FILE_BROWSER_URL', '')

    @staticmethod
    def context_processor():
        return {'ckeditor': current_app.extensions['ckeditor']}

    @staticmethod
    def uploader(func):
        """Decorated the view function that handle the file upload. The upload 
        view must return the uploaded image's url. For example::
            
            @app.route('/files/<filename>')
            def files(filename):
                path = app.config['UPLOADED_PATH']
                return send_from_directory(path, filename)

            @app.route('/upload', methods=['POST'])
            @ckeditor.uploader
            def upload():
                f = request.files.get('upload')
                f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
                url = url_for('files', filename=f.filename)
                return url
        
        Check ``example/app.py`` for complete code. 

        .. versionadded:: 0.3
        """
        def wrapper(*args, **kwargs):
            func_num = request.args.get('CKEditorFuncNum') 
            ckeditor = request.args.get('CKEditor') 
            # language code used for error message, not used yet.
            lang_code = request.args.get('langCode')
            # the error message to display when upload failed, not used yet.
            message = ''
            url = func(*args, **kwargs)
            return Markup('''
<script type="text/javascript">
window.parent.CKEDITOR.tools.callFunction(%s, "%s", "%s");</script>'''
% (func_num, url, message))
        return wrapper
