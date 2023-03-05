from wtforms import TextAreaField
from wtforms.widgets import TextArea


class CKEditor(TextArea):
    def __call__(self, field, **kwargs):
        class_ = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = f'ckeditor {class_}'
        return super(CKEditor, self).__call__(field, **kwargs)


class CKEditorField(TextAreaField):
    widget = CKEditor()
