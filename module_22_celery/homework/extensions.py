from celery import Celery
from app import create_app


def make_celery():
    app = create_app()
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)

    # Periodic tasks
    celery.conf.beat_schedule = {
        'weekly-digest': {
            'task': 'app.tasks.weekly_newsletter',
            'schedule': 604800.0,  # 1 week in seconds
        }
    }

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery()