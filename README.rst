Flask-Defer
=========

.. image:: https://badge.fury.io/py/flask-defer.svg
    :target: https://badge.fury.io/py/flask-defer
.. image:: https://travis-ci.org/brettlangdon/flask-defer.svg?branch=master
    :target: https://travis-ci.org/brettlangdon/flask-defer

Easily register a function to execute at the end of the current request.

Installation
~~~~~~~~~~~~

.. code:: bash

   pip install Flask-Defer


Usage
~~~~~

Passing a function and it's arguments to `flask_defer.after_request` will register that function to execute when the Flask request has ended.

If a call to `flask_defer.after_request` happens outside of a request context then the function will be executed immediately.

.. code:: python

   from flask import Flask
   from flask_defer import FlaskDefer, after_request

   app = Flask(__name__)
   FlaskDefer(app)


   def defer_me(name, say_hello=False):
       if say_hello:
           print 'Saying hello to, {name}'.format(name=name)


   @app.route('/')
   def index():
       print 'Start of request method'

       # Defer `defer_me` until after the current request has finished
       after_request(defer_me, 'name', say_hello=True)

       print 'Ending request method'

       return 'Thanks!'


   if __name__ == '__main__':
       app.run()


.. code:: bash

   $ python example.py
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
   Start of request method
   Ending request method
   Saying hello to, name
   127.0.0.1 - - [28/Nov/2016 15:41:39] "GET / HTTP/1.1" 200 -
