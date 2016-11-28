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
