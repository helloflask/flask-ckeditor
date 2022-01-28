# -*- coding: utf-8 -*-
"""
    flask_ckeditor.fields
    ~~~~~~~~~~~~~~~~~~~~~
    Add support for WTForms/Flask-WTF.

    :author: Grey Li <withlihui@gmail.com>
    :copyright: (c) 2020 by Grey Li.
    :license: MIT, see LICENSE for more details.
"""
from flask import Markup, escape
from wtforms import TextAreaField
from wtforms.widgets import html_params

class CKEditor():
    def __call__(self, field, **kwargs):
        ckeditor=field.name+'_'
        kwargs.setdefault('id', field.id)
        if 'required' not in kwargs and 'required' in getattr(field, 'flags', []):
            kwargs['required'] = True
        return Markup('<textarea hidden class="ckeditor" %s></textarea><div %s></div><div %s>%s</div>'
                % (html_params(name=field.name, **kwargs),
                    html_params(id='ckeditor-toolbox'),
                    html_params(name=ckeditor, id=ckeditor),
                    escape(field._value())))


class CKEditorField(TextAreaField):
    widget = CKEditor()
