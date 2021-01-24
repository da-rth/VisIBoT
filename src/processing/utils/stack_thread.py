from concurrent.futures import ThreadPoolExecutor
import sys
import traceback
import logging

logger = logging.getLogger('thread-pool-executor')


class ThreadPoolExecutorStackTraced(ThreadPoolExecutor):
    """
    Creates an exception of same type with the traceback as message
    Original author: https://stackoverflow.com/users/3276106/se7entyse7en
    """
    def submit(self, fn, *args, **kwargs):
        """Submits the wrapped function instead of `fn`"""

        return super(ThreadPoolExecutorStackTraced, self).submit(
            self._function_wrapper, fn, *args, **kwargs)

    def _function_wrapper(self, fn, *args, **kwargs):
        """Wraps `fn` in order to preserve the traceback of any kind of
        raised exception

        """
        try:
            return fn(*args, **kwargs)
        except Exception:
            logger.exception("Error occurred in thread pool executor.")
            raise sys.exc_info()[0](traceback.format_exc())
