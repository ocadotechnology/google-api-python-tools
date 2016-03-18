class DataProcOperation(object):
    def __init__(self, client, response):
        self.client = client
        self.response = response

    @classmethod
    def from_id(cls, client, operation_id):
        return DataProcOperation(client, {'name': operation_id}).update()

    def update(self):
        self.response = self.client.execute(
                lambda x: x.projects().regions().operations().get(name=self.get_job_id()))
        return self

    def get_current_state(self):
        self.update()
        return self.get_last_state()

    def get_last_state(self):
        if self.response.get('done', False):
            if 'error' in self.response:
                return 'ERROR'
            return 'DONE'
        else:
            return 'RUNNING'

    def get_details_message(self):
        if 'error' in self.response:
            return self.response['error']['message']

    def get_job_id(self):
        return self.response['name']
