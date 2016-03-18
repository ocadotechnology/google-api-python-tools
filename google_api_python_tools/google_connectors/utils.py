import logging
import traceback
from time import sleep

logger = logging.getLogger()


class retry_on(object):
    def __init__(self, expected_messages=None, expected_tracebacks=None, expected_classes=None, max_retries=3,
                 action_on_expected_failure=lambda ex: None):
        self._set_param("expected_messages", expected_messages)
        self._set_param("expected_tracebacks", expected_tracebacks)
        self._set_param("expected_classes", expected_classes)

        self.max_retries = max_retries
        self.action_on_expected_failure = action_on_expected_failure

    def _set_param(self, argument_name, arg):
        setattr(self, argument_name, arg)
        if arg is not None and not isinstance(arg, list):
            setattr(self, argument_name, [arg])

    def __call__(self, f):
        def wrapper(*args, **kwargs):
            for i in xrange(self.max_retries):
                try:
                    return f(*args, **kwargs)
                except Exception, ex:
                    logger.debug("Retry... Expected message (%s) (%s): %s" % (
                        ex.args, self._matches_message(ex), self.expected_messages,))

                    if i < self.max_retries - 1 and \
                            (self._matches_message(ex) or self._matches_traceback(ex) or self._matches_classes(ex)):
                        logger.info("Retrying execution, because one of (%s, %s, %s) occurred: %s" % (
                            self.expected_messages, self.expected_tracebacks, self.expected_classes, ex,))
                        self.action_on_expected_failure(ex)
                    else:
                        raise

                    sleep(2 ** i)

        return wrapper

    def _matches_classes(self, ex):
        return any([isinstance(ex, clazz) for clazz in self.expected_classes]) if self.expected_classes else False

    def _matches_message(self, ex):
        return any([expected_message in str(ex.message) for expected_message in self.expected_messages]) \
            if self.expected_messages else False

    def _matches_traceback(self, ex):
        formatted_traceback = traceback.format_exc(ex)
        return any([expected_traceback in formatted_traceback for expected_traceback in self.expected_tracebacks]) \
            if self.expected_tracebacks else None
