from google_api_python_tools.google_connectors.connector import CredentialFactory


class AppEngineCredentialsFactory(CredentialFactory):
    def create(self, scope):
        from oauth2client.appengine import AppAssertionCredentials

        return AppAssertionCredentials(scope=scope)
