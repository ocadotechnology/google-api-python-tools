import sys

from google_api_python_tools.google_connectors.gceapiexception import GCEApiException
from google_api_python_tools.google_connectors.utils import retry_on


__author__ = 'ppastuszka'


def execute_request(request, dry_run=False):
    try:
        response = []
        if not dry_run:
            response = request.execute()
    except Exception, ex:
        raise GCEApiException(ex), None, sys.exc_info()[2]
    return response


def general_execute_request(request_executor, connector):
    @retry_on(expected_tracebacks=['BadStatusLine',
                                   'ConnectionError'
                                   'ResponseNotReady',
                                   'Connection reset by peer',
                                   'Cannot connect to proxy'])
    def reconnect(ex):
        connector.connect(reuse_connection=False)

    @retry_on(expected_messages=['503', '500', '502', '403'],
              expected_tracebacks=['BadStatusLine',
                                   'ResponseNotReady',
                                   'ConnectionError',
                                   'Cannot connect to proxy',
                                   'Connection reset by peer',
                                   'is not allowed',
                                   'You don\'t have permission to use',
                                   'Unable to fetch URL',
                                   'Deadline exceeded while waiting for HTTP response',
                                   'Broken pipe',
                                   'invalid_grant'
                                   'Error reading SSH protocol banner'],
              action_on_expected_failure=reconnect)
    @retry_on()
    def inner():
        return execute_request(request_executor(connector.connect(reuse_connection=True)))

    return inner()
