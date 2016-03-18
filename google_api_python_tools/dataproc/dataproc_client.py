from google_api_python_tools.google_connectors.client import ApiClient

from google_api_python_tools.dataproc.cluster import DataProcCluster
from google_api_python_tools.google_connectors.connector import Connector


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
