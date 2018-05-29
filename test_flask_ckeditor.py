import unittest

from flask import Flask, render_template_string, current_app
from flask_wtf import FlaskForm

from flask_ckeditor import CKEditorField
from flask_ckeditor import _CKEditor, CKEditor


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
        self.assertIn('//cdn.ckeditor.com', rv)
        self.assertIn('standard/ckeditor.js', rv)

        current_app.config['CKEDITOR_PKG_TYPE'] = 'basic'
        rv = self.ckeditor.load()
        self.assertIn('//cdn.ckeditor.com', rv)
        self.assertIn('basic/ckeditor.js', rv)

    def test_local_resources(self):
        current_app.config['CKEDITOR_SERVE_LOCAL'] = True

        response = self.client.get('/static/ckeditor/basic/ckeditor.js')
        self.assertNotEqual(response.status_code, 404)

        response = self.client.get('/static/ckeditor/standard/ckeditor.js')
        self.assertNotEqual(response.status_code, 404)

        response = self.client.get('/static/ckeditor/full/ckeditor.js')
        self.assertNotEqual(response.status_code, 404)

        rv = self.ckeditor.load()
        self.assertIn('/static/ckeditor/standard/ckeditor.js', rv)
        self.assertNotIn('//cdn.ckeditor.com', rv)

        current_app.config['CKEDITOR_PKG_TYPE'] = 'full'
        rv = self.ckeditor.load()
        self.assertIn('/static/ckeditor/full/ckeditor.js', rv)

    def test_config(self):
        current_app.config['CKEDITOR_LANGUAGE'] = 'zh'
        current_app.config['CKEDITOR_HEIGHT'] = '300'
        current_app.config['CKEDITOR_WIDTH'] = '500'
        current_app.config['CKEDITOR_CODE_THEME'] = 'theme_foo'
        current_app.config['CKEDITOR_FILE_UPLOADER'] = '/foo'
        current_app.config['CKEDITOR_FILE_BROWSER'] = '/bar'
        current_app.config['CKEDITOR_ENABLE_MARKDOWN'] = True
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
        self.assertIn('extraPlugins: "foo,bar,filebrowser,codesnippet,markdown",', rv)
        self.assertIn('uiColor: "#9AB8F3"', rv)

    def test_ckeditor_field(self):
        response = self.client.get('/field')
        data = response.get_data(as_text=True)
        self.assertIn('//cdn.ckeditor.com', data)
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

    def test_render_template(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('//cdn.ckeditor.com', data)
        self.assertIn('CKEDITOR.replace', data)
        self.assertIn('<textarea class="ckeditor"', data)
