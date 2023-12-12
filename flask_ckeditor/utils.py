import os
import uuid
import warnings
from flask import url_for

try:
    import bleach
except ImportError:
    warnings.warn('The "bleach" library is not installed, `cleanify` function will not be available.')


def get_url(endpoint_or_url):
    if endpoint_or_url.startswith(('https://', 'http://', '/')):
        return endpoint_or_url
    else:
        return url_for(endpoint_or_url)


def random_filename(old_filename):
    ext = os.path.splitext(old_filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


def cleanify(text, *, allow_tags=None):
    """Clean the input from client, this function rely on bleach.

    :parm text: input str
    :parm allow_tags: if you don't want to use default `allow_tags`,
        you can provide a Iterable which include html tag string like ['a', 'li',...].
    """
    default_allowed_tags = {'a', 'abbr', 'b', 'blockquote', 'code',
                            'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p'}
    return bleach.clean(text, tags=allow_tags or default_allowed_tags)
