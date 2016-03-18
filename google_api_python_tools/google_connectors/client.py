from google_api_python_tools.google_connectors.executor import general_execute_request


class ApiClient(object):
    def __init__(self, connector):
        self.connector = connector

    def execute(self, request_executor):
        return general_execute_request(request_executor, self.connector)
