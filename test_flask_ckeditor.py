# -*- coding: utf-8 -*-
"""
    test_flask_ckeditor
    ~~~~~~~~~~~~~~~~~~~~

    :author: Grey Li <withlihui@gmail.com>
    :copyright: (c) 2020 by Grey Li.
    :license: MIT, see LICENSE for more details.
"""
import json
import unittest
import sys
import builtins

from flask import Flask, render_template_string, current_app
from flask_wtf import FlaskForm, CSRFProtect

from flask_ckeditor import CKEditorField, _CKEditor, CKEditor, upload_success, upload_fail
from flask_ckeditor.utils import cleanify


class CKEditorTestCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)

        self.app.testing = True
        self.app.secret_key = 'for test'
        self.app.config['WTF_ENABLE_CSRF'] = False

        ckeditor = CKEditor(self.app)  # noqa

        self.ckeditor = _CKEditor

        class PostForm(FlaskForm):
            body = CKEditorField('Body')

        @self.app.route('/')
        def index():
            return render_template_string('''
                    {{ ckeditor.create() }}
                    {{ ckeditor.load() }}
                    {{ ckeditor.config() }}''')

        @self.app.route('/field', methods=['GET', 'POST'])
        def ckeditor_field():
            form = PostForm()
            if form.validate_on_submit():
                return form.body.data
            return render_template_string('''
                            {{ form.body() }}
                            {{ ckeditor.load() }}
                            {{ ckeditor.config(name='body') }}''', form=form)

        self.context = self.app.test_request_context()
        self.context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.context.pop()

    def test_extension_init(self):
        self.assertIn('ckeditor', current_app.extensions)

    def test_load(self):
        rv = self.ckeditor.load()
        self.assertIn('https://cdn.ckeditor.com', rv)
        self.assertIn('standard/ckeditor.js', rv)

        current_app.config['CKEDITOR_PKG_TYPE'] = 'basic'
        rv = self.ckeditor.load()
        self.assertIn('https://cdn.ckeditor.com', rv)
        self.assertIn('basic/ckeditor.js', rv)

    def test_local_resources(self):
        current_app.config['CKEDITOR_SERVE_LOCAL'] = True

        response = self.client.get('/ckeditor/static/basic/ckeditor.js')
        response.close()
        self.assertNotEqual(response.status_code, 404)

        response = self.client.get('/ckeditor/static/standard/ckeditor.js')
        response.close()
        self.assertNotEqual(response.status_code, 404)

        response = self.client.get('/ckeditor/static/full/ckeditor.js')
        response.close()
        self.assertNotEqual(response.status_code, 404)

        rv = self.ckeditor.load()
        self.assertIn('/ckeditor/static/standard/ckeditor.js', rv)
        self.assertNotIn('https://cdn.ckeditor.com', rv)

        current_app.config['CKEDITOR_PKG_TYPE'] = 'full'
        rv = self.ckeditor.load()
        self.assertIn('/ckeditor/static/full/ckeditor.js', rv)

        current_app.config['CKEDITOR_PKG_TYPE'] = 'standard-all'
        rv = self.ckeditor.load()
        self.assertIn('/ckeditor/static/standard/ckeditor.js', rv)

        current_app.config['CKEDITOR_PKG_TYPE'] = 'full-all'
        rv = self.ckeditor.load()
        self.assertIn('/ckeditor/static/standard/ckeditor.js', rv)

    def test_config(self):
        current_app.config['CKEDITOR_LANGUAGE'] = 'zh'
        current_app.config['CKEDITOR_HEIGHT'] = '300'
        current_app.config['CKEDITOR_WIDTH'] = '500'
        current_app.config['CKEDITOR_CODE_THEME'] = 'theme_foo'
        current_app.config['CKEDITOR_FILE_UPLOADER'] = '/foo'
        current_app.config['CKEDITOR_FILE_BROWSER'] = '/bar'
        current_app.config['CKEDITOR_ENABLE_CODESNIPPET'] = True
        current_app.config['CKEDITOR_EXTRA_PLUGINS'] = ['foo', 'bar']

        rv = self.ckeditor.config(custom_config='uiColor: "#9AB8F3"')
        self.assertIn('language: "zh",', rv)
        self.assertIn('height: 300,', rv)
        self.assertIn('width: 500,', rv)
        self.assertIn('codeSnippet_theme: "theme_foo",', rv)
        self.assertIn('imageUploadUrl: "/foo",', rv)
        self.assertIn('filebrowserUploadUrl: "/foo",', rv)
        self.assertIn('filebrowserBrowseUrl: "/bar",', rv)
        self.assertIn('extraPlugins: "foo,bar,filebrowser,codesnippet",', rv)
        self.assertIn('uiColor: "#9AB8F3"', rv)

    def test_config_overwrite(self):
        current_app.config['CKEDITOR_LANGUAGE'] = 'zh'
        current_app.config['CKEDITOR_HEIGHT'] = '300'
        current_app.config['CKEDITOR_WIDTH'] = '500'
        current_app.config['CKEDITOR_CODE_THEME'] = 'theme_foo'
        current_app.config['CKEDITOR_FILE_UPLOADER'] = '/foo'
        current_app.config['CKEDITOR_FILE_BROWSER'] = '/bar'
        current_app.config['CKEDITOR_ENABLE_CODESNIPPET'] = True
        current_app.config['CKEDITOR_EXTRA_PLUGINS'] = ['foo', 'bar']

        rv = self.ckeditor.config(language='en', height=1000, width=800, code_theme='theme_bar',
                                  file_uploader='/1', file_browser='/2', enable_codesnippet=False,
                                  extra_plugins=['1', '2'])
        self.assertNotIn('language: "zh",', rv)
        self.assertNotIn('height: 300,', rv)
        self.assertNotIn('width: 500,', rv)
        self.assertNotIn('codeSnippet_theme: "theme_foo",', rv)
        self.assertNotIn('imageUploadUrl: "/foo",', rv)
        self.assertNotIn('filebrowserUploadUrl: "/foo",', rv)
        self.assertNotIn('filebrowserBrowseUrl: "/bar",', rv)
        self.assertNotIn('extraPlugins: "foo,bar,filebrowser,codesnippet",', rv)

        self.assertIn('language: "en",', rv)
        self.assertIn('height: 1000,', rv)
        self.assertIn('width: 800,', rv)
        self.assertIn('codeSnippet_theme: "theme_bar",', rv)
        self.assertIn('imageUploadUrl: "/1",', rv)
        self.assertIn('filebrowserUploadUrl: "/1",', rv)
        self.assertIn('filebrowserBrowseUrl: "/2",', rv)
        self.assertIn('extraPlugins: "1,2,filebrowser",', rv)

    def test_ckeditor_field(self):
        response = self.client.get('/field')
        data = response.get_data(as_text=True)
        self.assertIn('https://cdn.ckeditor.com', data)
        self.assertIn('CKEDITOR.replace', data)
        self.assertIn('<textarea class="ckeditor', data)
        self.assertIn('name="body"', data)

        response = self.client.post('/field', data=dict(body='Hello, World'))
        data = response.get_data(as_text=True)
        self.assertIn('Hello, World', data)
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        rv = self.ckeditor.create()
        self.assertIn('<textarea class="ckeditor"', rv)

        rv = self.ckeditor.create(name='foo')
        self.assertIn('<textarea class="ckeditor" name="foo" id="foo"', rv)

        rv = self.ckeditor.create(value='bar')
        self.assertIn('<textarea class="ckeditor" name="ckeditor" id="ckeditor">bar</textarea>', rv)

    def test_render_template(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('https://cdn.ckeditor.com', data)
        self.assertIn('CKEDITOR.replace', data)
        self.assertIn('<textarea class="ckeditor"', data)

    def test_csrf_protect(self):
        csrf = CSRFProtect(self.app)  # noqa

        current_app.config['CKEDITOR_ENABLE_CSRF'] = True
        rv = self.ckeditor.config()
        self.assertIn('X-CSRFToken', rv)

    def test_local_resources_plugins(self):
        # basic package plugins
        plugins = {'filebrowser', 'lineutils', 'widgetselection',
                   'codesnippet', 'filetools', 'popup', 'widget'}
        for plugin in plugins:
            url = f'/ckeditor/static/basic/plugins/{plugin}/plugin.js'
            response = self.client.get(url)
            response.close()
            self.assertEqual(response.status_code, 200)

        # standard package plugins
        plugins = {'codesnippet', 'filetools', 'popup', 'widget'}
        for plugin in plugins:
            url = f'/ckeditor/static/standard/plugins/{plugin}/plugin.js'
            response = self.client.get(url)
            response.close()
            self.assertEqual(response.status_code, 200)

        # full package plugins
        plugins = {'codesnippet', 'filetools', 'popup', 'widget'}
        for plugin in plugins:
            url = f'/ckeditor/static/full/plugins/{plugin}/plugin.js'
            response = self.client.get(url)
            response.close()
            self.assertEqual(response.status_code, 200)

    def test_ckeditor_class(self):
        @self.app.route('/create-without-config')
        def create_without_config():
            return render_template_string('''
                    {{ ckeditor.create() }}
                    {{ ckeditor.load() }}''')

        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('document.getElementById("ckeditor").classList.remove("ckeditor")', data)
        self.assertIn('id="ckeditor"', data)

        response = self.client.get('/field')
        data = response.get_data(as_text=True)
        self.assertIn('document.getElementById("body").classList.remove("ckeditor")', data)
        self.assertIn('id="body"', data)

        response = self.client.get('/create-without-config')
        data = response.get_data(as_text=True)
        self.assertIn('class="ckeditor', data)
        self.assertNotIn('document.getElementById("ckeditor").classList.remove("ckeditor")', data)

    def test_codesnippet_plugin_from_cdn(self):
        current_app.config['CKEDITOR_ENABLE_CODESNIPPET'] = True
        current_app.config['CKEDITOR_SERVE_LOCAL'] = False
        current_app.config['CKEDITOR_PKG_TYPE'] = 'basic'
        rv = self.ckeditor.load()
        self.assertIn('standard-all', rv)
        current_app.config['CKEDITOR_PKG_TYPE'] = 'standard'
        rv = self.ckeditor.load()
        self.assertIn('standard-all', rv)
        current_app.config['CKEDITOR_PKG_TYPE'] = 'full'
        rv = self.ckeditor.load()
        self.assertIn('standard-all', rv)
        current_app.config['CKEDITOR_PKG_TYPE'] = 'full-all'
        rv = self.ckeditor.load()
        self.assertIn('full-all', rv)

    def test_upload_success(self):
        rv = upload_success(url='test_url', filename='test_filename')
        self.assertEqual(
            json.loads(rv.data),
            {'uploaded': 1, 'url': 'test_url', 'filename': 'test_filename'}
        )

        rv = upload_success(url='test_url', filename='test_filename', message='warning')
        self.assertEqual(
            json.loads(rv.data),
            {'uploaded': 1, 'url': 'test_url', 'filename': 'test_filename', 'error': {'message': 'warning'}}
        )

    def test_upload_fail(self):
        rv = upload_fail(message='error')
        self.assertEqual(
            json.loads(rv.data),
            {'uploaded': 0, 'error': {'message': 'error'}}
        )

        default_error_message = current_app.config['CKEDITOR_UPLOAD_ERROR_MESSAGE']
        rv = upload_fail()
        self.assertEqual(
            json.loads(rv.data),
            {'uploaded': 0, 'error': {'message': default_error_message}}
        )

        current_app.config['CKEDITOR_UPLOAD_ERROR_MESSAGE'] = 'new error message'
        rv = upload_fail()
        self.assertEqual(
            json.loads(rv.data),
            {'uploaded': 0, 'error': {'message': 'new error message'}}
        )

    def test_cleanify_input_js(self):
        input = 'an <script>evil()</script> example'
        clean_ouput = cleanify(input)
        self.assertEqual(clean_ouput,
                         u'an &lt;script&gt;evil()&lt;/script&gt; example')

    def test_cleanify_by_allow_tags(self):
        input = '<b> hello <a> this is a url </a> !</b> <h1> this is h1 </h1>'
        clean_out = cleanify(input, allow_tags=['b'])
        self.assertEqual(clean_out,
                         '<b> hello &lt;a&gt; this is a url &lt;/a&gt; !</b> &lt;h1&gt; this is h1 &lt;/h1&gt;')

    def test_cleanify_by_default_allow_tags(self):
        self.maxDiff = None
        input = """<a>xxxxx</a>
                <abbr>xxxxx</abbr>
                <b>xxxxxxx</b>
                <blockquote>xxxxxxx</blockquote>
                <code>print(hello)</code>
                <em>xxxxx</em>
                <i>xxxxxx</i>
                <li>xxxxxx</li>
                <ol>xxxxxx</ol>
                <pre>xxxxxx</pre>
                <strong>xxxxxx</strong>
                <ul>xxxxxx</ul>
                <h1>xxxxxxx</h1>
                <h2>xxxxxxx</h2>
                <h3>xxxxxxx</h3>
                <h4>xxxxxxx</h4>
                <h5>xxxxxxx</h5>
                <p>xxxxxxxx</p>
        """
        clean_out = cleanify(input)
        self.assertEqual(clean_out, input)

    def test_import_cleanify_without_install_bleach(self):
        origin_import = builtins.__import__
        origin_modules = sys.modules.copy()

        def import_hook(name, *args, **kwargs):
            if name == 'bleach':
                raise ImportError('test case module')
            else:
                return origin_import(name, *args, **kwargs)

        if 'flask_ckeditor.utils' in sys.modules:
            del sys.modules['flask_ckeditor.utils']
        builtins.__import__ = import_hook

        with self.assertWarns(UserWarning) as w:
            from flask_ckeditor.utils import cleanify  # noqa: F401

        self.assertEqual(str(w.warning),
                         'The "bleach" library is not installed, `cleanify` function will not be available.')

        # recover default
        builtins.__import__ = origin_import
        sys.modules = origin_modules


if __name__ == '__main__':
    unittest.main()
