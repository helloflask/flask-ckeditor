"""
Flask-CKEditor
--------------

CKEditor integration for Flask, including image upload, code syntax highlight and more.

Main Features:

* Integrated with Flask-WTF/WTForms.
* Config CKEditor through Flask's configuration system.
* Image upload support.
* Code snippet highlight.
* Bulit-in CKEditor resources.

Go to `Github page
<https://github.com/greyli/flask-ckeditor>`_ , which you can check for more
details.
"""
from os import path
from codecs import open
from setuptools import setup

basedir = path.abspath(path.dirname(__file__))
with open(path.join(basedir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Flask-CKEditor',
    version='0.3.4',
    url='http://github.com/greyli/flask-ckeditor',
    license='MIT',
    author='Grey Li',
    author_email='withlihui@gmail.com',
    description='CKEditor integration for Flask.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['flask_ckeditor'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    test_suite='test_flask_ckeditor',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
