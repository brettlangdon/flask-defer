import unittest

from flask import Flask, _request_ctx_stack as stack
from flask_defer import FlaskDefer, defer


def deferred_task(name, with_keyword=False):
    return (name, with_keyword)


class TestFlaskDefer(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.defer = FlaskDefer(app=self.app)

        @self.app.route('/')
        def test_endpoint():
            defer(deferred_task, 'name', with_keyword=True)
            return 'test_endpoint'

        @self.app.route('/multiple')
        def test_multiple():
            defer(deferred_task, 'first', with_keyword=True)
            defer(deferred_task, 'second', with_keyword=False)
            defer(deferred_task, 'third', with_keyword=True)
            return 'test_multiple'

        @self.app.route('/extra')
        def test_extra_params():
            defer(deferred_task, 'name', 'extra', with_keyword=True, extra_param='param')
            return 'test_extra_params'

        @self.app.route('/no-defer')
        def test_no_defer():
            return 'test_no_defer'

    def test_deferring_task(self):
        with self.app.test_client() as client:
            # Make the request so we register the task
            client.get('/')

            ctx = stack.top
            self.assertTrue(hasattr(ctx, 'deferred_tasks'))
            self.assertEqual(len(ctx.deferred_tasks), 1)

            task = ctx.deferred_tasks[0]
            self.assertDictEqual(task, dict(
                args=('name', ),
                func=deferred_task,
                kwargs=dict(with_keyword=True),
            ))

        # Assert that the deferred tasks aren't shared between requests
        with self.app.test_client() as client:
            client.get('/no-defer')

            ctx = stack.top
            self.assertFalse(hasattr(ctx, 'deferred_tasks'))

    def test_deferring_task_multiple(self):
        with self.app.test_client() as client:
            # Make the request so we register the task
            client.get('/multiple')

            ctx = stack.top
            self.assertTrue(hasattr(ctx, 'deferred_tasks'))
            self.assertEqual(len(ctx.deferred_tasks), 3)

            task = ctx.deferred_tasks[0]
            self.assertDictEqual(task, dict(
                args=('first', ),
                func=deferred_task,
                kwargs=dict(with_keyword=True),
            ))

            task = ctx.deferred_tasks[1]
            self.assertDictEqual(task, dict(
                args=('second', ),
                func=deferred_task,
                kwargs=dict(with_keyword=False),
            ))

            task = ctx.deferred_tasks[2]
            self.assertDictEqual(task, dict(
                args=('third', ),
                func=deferred_task,
                kwargs=dict(with_keyword=True),
            ))

    def test_deferring_task_no_defer(self):
        with self.app.test_client() as client:
            # Make the request
            client.get('/no-defer')

            ctx = stack.top
            self.assertFalse(hasattr(ctx, 'deferred_tasks'))

    def test_deferring_task_extra(self):
        # We get a TypeError from the invalid function call
        # TODO: There has to be a better/more concise way to test this
        with self.assertRaises(TypeError):
            with self.app.test_client() as client:
                # Make the request so we register the task
                client.get('/extra')

                ctx = stack.top
                self.assertTrue(hasattr(ctx, 'deferred_tasks'))
                self.assertEqual(len(ctx.deferred_tasks), 1)

                task = ctx.deferred_tasks[0]
                self.assertDictEqual(task, dict(
                    args=('name', 'extra'),
                    func=deferred_task,
                    kwargs=dict(with_keyword=True, extra_param='param'),
                ))

    def test_no_app_context(self):
        result = defer(deferred_task, 'name', with_keyword=True)
        self.assertEqual(result, ('name', True))


if __name__ == '__main__':
    unittest.main()
