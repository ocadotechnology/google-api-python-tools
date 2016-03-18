from api_requests.client import ApiClient
from api_requests.connector import Connector
from dataproc.cluster import DataProcCluster


class DataProcClient(ApiClient):
    def __init__(self, credentials_factory, timeout=20):
        super(DataProcClient, self).__init__(Connector(
                credentials_factory,
                scope='https://www.googleapis.com/auth/cloud-platform',
                discovery_url='https://www.googleapis.com/discovery/v1/apis/dataproc/v1/rest',
                service_name='dataproc',
                api_version='v1',
                description='dataproc::%s' % str(credentials_factory),
                timeout=timeout
        ))

    def cluster(self, project, name, region="global"):
        return DataProcCluster(self, project, name, region)
