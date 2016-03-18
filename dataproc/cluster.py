from dataproc.constants import DataprocImageVersion
from dataproc.job import DataProcJob
from dataproc.operation import DataProcOperation


class DataProcCluster(object):
    class ClusterJob(object):
        def __init__(self, cluster):
            self.cluster = cluster

        def get_last_state(self):
            return self.translate_state(self.cluster.description['status']['state'])

        def get_details_message(self):
            status = self.cluster.description['status']
            return status['detail'] if 'detail' in status else None

        def get_current_state(self):
            self.cluster.update()
            return self.get_last_state()

        def translate_state(self, state):
            raise NotImplementedError

    class StartJob(ClusterJob):
        translations = {
            "UNKNOWN": "ERROR",
            "CREATING": "RUNNING",
            "RUNNING": "DONE",
            "ERROR": "ERROR",
            "DELETING": "ERROR",
            "UPDATING": "RUNNING"
        }

        @classmethod
        def from_id(cls, client, project, name, region="global"):
            return DataProcCluster.StartJob(DataProcCluster(client, project, name, region).update())

        def translate_state(self, state):
            return self.translations[state]

    DEFAULT_SCOPES = ['https://www.googleapis.com/auth/monitoring',
                      'https://www.googleapis.com/auth/devstorage.full_control',
                      'https://www.googleapis.com/auth/compute',
                      'https://www.googleapis.com/auth/userinfo.email',
                      'https://www.googleapis.com/auth/bigquery',
                      'https://www.googleapis.com/auth/logging.write',
                      'https://www.googleapis.com/auth/logging.admin']

    def __init__(self, client, project, name, region):
        self.client = client
        self.project = project
        self.name = name
        self.region = region
        self.description = None

    def update(self):
        self.description = self.client.execute(
                lambda x: x.projects().regions().clusters().get(projectId=self.project,
                                                                clusterName=self.name,
                                                                region=self.region))
        return self

    def create(self, master_machine_type, worker_machine_type, worker_instance_count,
               image=DataprocImageVersion.V_1_0, zone="europe-west1-b", network="default", scopes=None, uid=None):
        master_configuration = {
            "numInstances": 1,
            "machineTypeUri": "https://www.googleapis.com/compute/v1/projects/%s/zones/%s/machineTypes/%s" % (
                self.project, zone, master_machine_type),
            "diskConfig": {},
            "isPreemptible": False
        }
        worker_configuration = {
            "numInstances": worker_instance_count,
            "machineTypeUri": "https://www.googleapis.com/compute/v1/projects/%s/zones/%s/machineTypes/%s" % (
                self.project, zone, worker_machine_type),
            "diskConfig": {},
            "isPreemptible": False
        }
        self.description = {
            "projectId": self.project,
            "clusterName": self.name,
            "config": {
                "gceClusterConfig": {
                    "zoneUri": "https://www.googleapis.com/compute/v1/projects/%s/zones/%s" % (self.project, zone),
                    "networkUri": "https://www.googleapis.com/compute/v1/projects/%s/global/networks/%s" %
                                  (self.project, network),
                    "serviceAccountScopes": scopes or self.DEFAULT_SCOPES,
                    "metadata": {
                        "uid": uid
                    }
                },
                "masterConfig": master_configuration,
                "workerConfig": worker_configuration,
                "softwareConfig": {
                    "imageVersion": image
                }
            }
        }
        response = self.client.execute(lambda x: x.projects().regions().clusters().create(projectId=self.project,
                                                                                          region=self.region,
                                                                                          body=self.description))
        return DataProcOperation(self.client, response)

    def delete(self):
        """
            Delete cluster
        """
        response = self.client.execute(lambda x: x.projects().regions().clusters().delete(projectId=self.project,
                                                                                          region=self.region,
                                                                                          clusterName=self.name))
        return DataProcOperation(self.client, response)

    def exists(self):
        """
            Check that cluster exists
        """
        response = self.client.execute(lambda x: x.projects().regions().clusters().list(projectId=self.project,
                                                                                        region=self.region))
        return 'clusters' in response and self.name in [b['clusterName'] for b in response['clusters']]

    def get_default_logging_config(self):
        return {"driverLogLevels": {"com.ocado": "INFO", "root": "FATAL", "org.apache": "INFO"}}

    def submit_spark_sql_job(self, queries, job_id=None):
        return self.submit_job('sparkSqlJob', {
            'loggingConfig': self.get_default_logging_config(),
            'queryList': {
                'queries': queries
            }
        }, job_id)

    def submit_spark_job(self, job_body, job_id=None):
        if 'loggingConfig' not in job_body.keys():
            job_body['loggingConfig'] = self.get_default_logging_config()
        return self.submit_job('sparkJob', job_body, job_id)

    def submit_job(self, job_name, job_body, job_id=None):
        request_body = {
            'job': {
                'placement': {
                    'clusterName': self.name
                },
                job_name: job_body
            }
        }
        if job_id:
            request_body['job']['reference'] = {
                'projectId': self.project,
                'jobId': job_id
            }
        response = self.client.execute(lambda x: x.projects().regions().jobs().submit(projectId=self.project,
                                                                                      region=self.region,
                                                                                      body=request_body))
        return DataProcJob(self.client, self.project, self.region, response)
