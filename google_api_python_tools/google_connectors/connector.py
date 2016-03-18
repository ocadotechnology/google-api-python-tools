import httplib2
from apiclient import discovery


class CredentialFactory(object):
    def create(self, scope):
        pass

    def __str__(self):
        return '%s()' % self.__class__.__name__


connections = {}


class Connector(object):
    def __init__(self, credentials_factory, scope, discovery_url, service_name, api_version,
                 description=None,
                 timeout=None):
        self.scope = scope
        self.discovery_url = discovery_url
        self.service_name = service_name
        self.api_version = api_version
        self.credentials_factory = credentials_factory
        self.description = description or service_name
        self.timeout = timeout

    def connect(self, reuse_connection=True):
        if self.description in connections and reuse_connection:
            return connections[self.description]

        service = self._prepare_service(self.credentials_factory.create(self.scope), self.discovery_url,
                                        self.service_name,
                                        self.api_version)
        connections[self.description] = service
        return service

    def _prepare_service(self, credentials, discovery_url, service_name, api_version):
        http = httplib2.Http(timeout=self.timeout)
        http = credentials.authorize(http)
        return discovery.build(service_name, api_version, discoveryServiceUrl=discovery_url, http=http)
