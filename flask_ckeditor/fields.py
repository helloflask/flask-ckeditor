# -*- coding: utf-8 -*-
from wtforms import TextAreaField
from wtforms.widgets import TextArea

class CKEditor(TextArea):
    def __call__(self, field, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = u'%s %s' % ('ckeditor', c)
        return super(CKEditor, self).__call__(field, **kwargs)


class CKEditorField(TextAreaField):
    widget = CKEditor()
