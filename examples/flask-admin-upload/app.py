import os

from flask import Flask, render_template, request, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor, CKEditorField, upload_fail, upload_success
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_wtf import FlaskForm
# from flask_wtf import CSRFProtect  # if you want to enable CSRF protect, uncomment this line
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

# Create in-memory database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'
# app.config['CKEDITOR_ENABLE_CSRF'] = True  # if you want to enable CSRF protect, uncomment this line
app.config['UPLOADED_PATH'] = os.path.join(basedir, 'uploads')


db = SQLAlchemy(app)
ckeditor = CKEditor(app)
# csrf = CSRFProtect(app)  # if you want to enable CSRF protect, uncomment this line


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    text = db.Column(db.Text)


# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Go to Admin!</a>'


# Customized Post model admin
class PostAdmin(ModelView):
    # override form type with CKEditorField
    form_overrides = dict(text=CKEditorField)
    create_template = 'edit.html'
    edit_template = 'edit.html'


admin = Admin(app, name='Flask-CKEditor demo')
admin.add_view(PostAdmin(Post, db.session))


def init_db():
    """
    Populate a small db with some example entries.
    """
    db.drop_all()
    db.create_all()

    # Create sample Post
    title = "de Finibus Bonorum et Malorum - Part I"
    text = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor \
                incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud \
                exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure \
                dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. \
                Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt \
                mollit anim id est laborum."

    post = Post(title=title, text=text)
    db.session.add(post)
    db.session.commit()


@app.route('/files/<filename>')
def uploaded_files(filename):
    path = app.config['UPLOADED_PATH']
    return send_from_directory(path, filename)


@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    url = url_for('uploaded_files', filename=f.filename)
    return upload_success(url=url)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
