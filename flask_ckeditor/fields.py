# -*- coding: utf-8 -*-
"""
    flask_ckeditor.fields
    ~~~~~~~~~~~~~~~~~~~~~
    Add support for WTForms/Flask-WTF.

    :author: Grey Li <withlihui@gmail.com>
    :copyright: (c) 2020 by Grey Li.
    :license: MIT, see LICENSE for more details.
"""
from wtforms import TextAreaField
from wtforms.widgets import TextArea


class CKEditor(TextArea):
    def __call__(self, field, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = u'%s %s' % ('ckeditor', c)
        return super(CKEditor, self).__call__(field, **kwargs)


class CKEditorField(TextAreaField):
    widget = CKEditor()
