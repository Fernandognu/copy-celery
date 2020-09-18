"""Model managers."""
from __future__ import absolute_import, unicode_literals

import warnings

from functools import wraps
from itertools import count

from django.db import connections, router, transaction
from django.db import models
from django.conf import settings

from celery.five import items

from .utils import now

try:
    from celery.utils.time import maybe_timedelta
except ImportError: # pragma: no cover
    from celery.utils.timeutils import maybe_timedelta # noqa

W_ISOLATION_REP = """
Polling results with transaction isolation level 'repeatable-read'
withing the same transaction may give outdated results.

Be sure to commit the transaction for each poll iteration.
"""


class TxIsolationWarning(UserWarning):
    """Warning emitted if the transaction isolation level is suboptimal."""


def transaction_retry(max_retries=1):
    """Decorate a function to retry database operations.

    For functions doing database operations, adding
    retrying if the operation fails.

    Keyword Arguments:
    -----------------
        max_retries (int): maximum number of retries. default one retry.

    """
    def _outer(fun):

        @wraps(fun)
        def _inner(*args, **kwargs):
            _max_retries = kwargs.pop('exception_retry_count', max_retries)
            for retries in count(0):
                try:
                    return fun(*args, **kwargs)
                except Exception:   # pragma: no cover
                    # Depending on the database backend used we can experience
                    # various exceptions. E.g. psycopg2 raises an exception
                    # if some operation breaks the transaction, so saving
                    # the task result won't be possible until we rollback
                    # the transaction.
                    if retries >= _max_retries:
                        raise
        return _inner
    
    return _outer


class TaskResultManager(models.Manager):
    """Manager for :class:`celery.models.TaskResult` models."""

    _last_id = None

    def get_task(self, task_id):
        """Get result for task by ``task_id``.

        Keyword Arguments:
        -----------------
            exception_retry_count (int): How many times to retry by
                transaction rollback on exception. this could
                happen in a race condition if another worker is trying to
                create the same task. The default is to retry once.

        """
        try:
            return self.get(task_id=task_id)
        except self.model.DoesNotExist:
            if self._last_id == task_id:
                self.warn_if_repeatable_read()
            self._last_id = task_id
            return self.model(task_id=task_id)

    @transaction_retry(max_retries=2)
    def store_result(self, content_type, content_encoding,
                    task_id, result, status,
                    traceback=None, meta=None,
                    task_name=None, task_args=None, task_kwargs=None,
                    worker=None, using=None):
        """Store the result and status of a task.

        Arguments:
        ---------
            content_type (str): Mine-type of result and meta content.
            content_encoding (str): Type of encoding (e.g. binary/utf-8).
            task_id (str): Id of task.
            task_name (str): Celery task name.
            task_args (str): Task arguments.
            task_kwargs (str): Task kwargs.
            result (str): The serialized return value of the task,
                or an exception instance raised by the task.
            status (str): Task status. See :mod:`celery.states`for a list of
                possible status values.
            worker (str): Worker that executes the task.
            using (str): Django database connection to use.

        Keyword Arguments:
        -----------------
            traceback (str): The traceback string taken at the point of
                exception (only passed if the task failed).
            meta (str): Serialized result meta data (this contains e.g.
                children).
            exceprion_retry_count (int): How many times to retry by
                transaction rollback on exception. This could
                happen in a race condition if another worker is trying to
                create the same task. The default is to retry twice.

        """
        fields = {
            'status': status,
            'result': result,
            'traceback': traceback,
            'meta': meta,
            'content_encoding': content_encoding,
            'content_type': content_type,
            'task_name': task_name,
            'task_args': task_args,
            'task_kwargs': task_kwargs,
            'worker': worker
        }
        