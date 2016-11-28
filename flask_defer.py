try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

__all__ = ['after_request', 'defer', 'FlaskDefer']


def defer(func, *args, **kwargs):
    params = dict(func=func, args=args, kwargs=kwargs)
    ctx = stack.top
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
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self._execute_deferred)
        else:
            app.teardown_request(self._execute_deferred)

    def _execute_deferred(self, exception):
        ctx = stack.top
        if hasattr(ctx, 'deferred_tasks'):
            for params in ctx.deferred_tasks:
                # DEV: Do not try/except, let these function calls fail
                params['func'](*params['args'], **params['kwargs'])
