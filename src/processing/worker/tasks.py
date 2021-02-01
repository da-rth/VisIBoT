import os
import lisa
import utils.tor_session as tor_session
from processing import store_result
from mongoengine import connect
from celery import Celery


MONGO_URL = os.getenv("MONGO_URL", None)
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
celery.config_from_object('config')


@celery.task(name='tasks.process_result')
def process_result(result: dict) -> list:
    connect(host=MONGO_URL)

    payloads_to_process = store_result(result)

    for payload in payloads_to_process:
        lisa.create_lisa_task(payload)

    return 'task complete'


@celery.task(name='tasks.lisa_analysis_success')
def lisa_analysis_success(task_id: str, analysis_data: dict):
    connect(host=MONGO_URL)
    lisa.process_analysis(task_id, analysis_data)
    return f"lisa task {task_id} processed"


@celery.task(name='tasks.lisa_analysis_failed')
def lisa_analysis_failed(task_id: str, failure_data: dict):
    connect(host=MONGO_URL)
    lisa.process_failure(task_id, failure_data)
    return f"lisa task {task_id} processed"


# Check if tor proxy is working
tor_session.check_session()
