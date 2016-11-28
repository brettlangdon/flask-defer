"""
Flask-Defer
"""
from setuptools import setup


def get_long_description():
    with open('README.rst') as f:
        rv = f.read()
    return rv


setup(
    name='Flask-Defer',
    version='1.0.1',
    url='https://github.com/brettlangdon/flask-defer.git',
    license='MIT',
    author='Brett Langdon',
    author_email='me@brett.is',
    description='Flask extension to defer task execution under after request teardown',
    long_description=get_long_description(),
    py_modules=['flask_defer'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=['Flask'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
