from google_api_python_tools.google_connectors.connector import CredentialFactory


class GCECredentialsFactory(CredentialFactory):
    def create(self, scope):
        from oauth2client.gce import AppAssertionCredentials

        return AppAssertionCredentials(scope=scope)
