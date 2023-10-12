"""
Flask-CKEditor
--------------

CKEditor integration for Flask, including image upload, code syntax
highlighting, and more.

Features:

* Integrate with Flask-WTF/WTForms.
* Configure CKEditor through Flask's configuration system.
* Image upload support.
* Code snippet highlighting.
* Built-in CKEditor resources.
"""
from setuptools import setup

setup(
    name='Flask-CKEditor',
    version='0.5.0',
    url='http://github.com/helloflask/flask-ckeditor',
    license='MIT',
    author='Grey Li',
    author_email='withlihui@gmail.com',
    description='CKEditor integration for Flask.',
    long_description=__doc__,
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
