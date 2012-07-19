#!/usr/bin/env python

from distutils.core import setup

setup(
    name='Flask-MimeRender',
    version='0.1.2',
    description='RESTful resource variant rendering using MIME Media-Types, for the Flask Micro Web Framework',
    author='Nicola Iarocci',
    author_email='nicola@nicolaiarocci.com',
    url='https://github.com/nicolaiarocci/flask-mimerender',
    license='MIT',
    long_description="""
    This module allows, with the use of python decorators, to transparently select a render function for an HTTP request handler's result. It uses mimeparse to parse the HTTP Accept header and select the best available representation.
    This is a Flask port from the original, excellent, mimerender v0.2.3 by Martin Blech (http://code.google.com/p/mimerender/)
    """,
    platforms=['all'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],

    py_modules=['flaskmimerender'],
    package_dir={'':'src'},
    requires=['flask'],
    install_requires=['flask'],
)
