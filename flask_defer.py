from flask import has_request_context, _request_ctx_stack

__all__ = ['after_request', 'defer', 'FlaskDefer']


def defer(func, *args, **kwargs):
    # If we are not in a request/app context, then just execute
    if not has_request_context():
        return func(*args, **kwargs)

    ctx = _request_ctx_stack.top

    # We are in a request/app context, defer until request/app teardown
    params = dict(func=func, args=args, kwargs=kwargs)
    if not hasattr(ctx, 'deferred_tasks'):
        setattr(ctx, 'deferred_tasks', [])
    ctx.deferred_tasks.append(params)


# Alias `defer` as `after_request`
after_request = defer


class FlaskDefer(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.teardown_request(self._execute_deferred)

    def _execute_deferred(self, exception):
        ctx = _request_ctx_stack.top
        if hasattr(ctx, 'deferred_tasks'):
            for params in ctx.deferred_tasks:
                params['func'](*params['args'], **params['kwargs'])
