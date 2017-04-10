"""
Flask-CKEditor
--------------

Implementation of CKEditor for Flask-WTF.
"""
from setuptools import setup


setup(
    name='Flask-CKEditor',
    version='0.1.0',
    url='http://github.com/greyli/flask-ckeditor',
    download_url = 'https://github.com/greyli/flask-ckeditor/archive/0.1.tar.gz',
    license='MIT',
    author='Grey Li',
    author_email='withlihui@gmail.com',
    description=('Implementation of CKEditor for Flask-WTF.'),
    long_description=__doc__,
    packages=['flask_ckeditor'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'WTForms'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
