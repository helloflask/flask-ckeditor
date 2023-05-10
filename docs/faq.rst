FAQ
=====

Using ckeditor with flask-admin
---------------------------------------------------

Example __init__.py

.. code-block:: python
    from flask import Flask
    from flask_ckeditor import CKEditor
    from flask_sqlalchemy import SQLAlchemy

    db = SQLAlchemy()
    ckeditor = CKEditor()

    def create_app():
        app = Flask(__name__, instance_relative_config=False)
        app.config.from_object('config.Config')

        db.init_app(app)
        ckeditor.init_app(app)

        with app.app_context():
            from .admin import admin

            return app

Example admin.py

.. code-block:: python
    from flask import current_app as app
    from your_app import db
    from flask_admin import Admin, AdminIndexView
    from flask_ckeditor import CKEditorField


    class Post(db.Model):
        __tablename__ = 'post'
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(80))
        text = db.Column(db.Text)
    

    db.create_all()
    

    class MyAdminIndexView(AdminIndexView):
        def is_accessible(self):
            try:
                # your_logic
                return True
            except:
                pass
    

    admin = Admin(
        app,
        name='',
        static_url_path='admin/static/',
        template_mode='bootstrap3',
        index_view=MyAdminIndexView(
            name='Admin',
        ),
    )


    class PostView(ModelView):
        column_list = ['id', 'title', 'text',]
        create_template = 'edit.html'
        edit_template = 'edit.html'
        form_overrides = {'text': CKEditorField}
    

    admin.add_views(
        PostView(
            Post,
            db.session,
            name='Post',
        )
    )

Add in templates edit.html

.. code-block:: jinja
    {% extends 'admin/model/edit.html' %}

    {% block tail %}
        {{ super() }}
            {{ ckeditor.load() }}
        The name value should be the name of the CKEditor form field, it defaults to "text" in Flask-Admin.
        {{ ckeditor.config(name='text') }}
    {% endblock %}


Additionally you can check `this SO answer <https://stackoverflow.com/a/46481343/5511849>`_ and the demo application at ``examples/flask-admin``.
