class DataProcJob(object):
    def __init__(self, client, project, region, response):
        self.client = client
        self.project = project
        self.region = region
        self.response = response

    @classmethod
    def from_id(cls, client, project, job_id, region="global"):
        return DataProcJob(client, project, region, {'reference': {'jobId': job_id}}).update()

    def update(self):
        self.response = self.client.execute(
                lambda x: x.projects().regions().jobs().get(projectId=self.project,
                                                            region=self.region,
                                                            jobId=self.get_job_id()))
        return self

    def get_current_state(self):
        self.update()
        return self.get_last_state()

    def get_last_state(self):
        return self.response['status']['state']

    def get_details_message(self):
        status = self.response['status']
        return status['details'] if 'details' in status else None

    def get_job_id(self):
        return self.response['reference']['jobId']
