import argparse
import os

from oauth2client import tools

from google_api_python_tools.google_connectors.connector import CredentialFactory


class FileBasedCredentials(CredentialFactory):
    @classmethod
    def get_default_for(cls, project, env, type=None, main_path=os.getcwd()):
        client_secrets_path = os.path.join(main_path, 'settings/', env, 'oauth2.json')
        credentials_storage_path = '.%s.%s.dat' % (type, project)
        return FileBasedCredentials(client_secrets_path=client_secrets_path,
                                    credentials_storage_path=credentials_storage_path)

    def __init__(self, client_secrets_path, credentials_storage_path, flags=None):
        self.client_secrets_path = client_secrets_path
        self.credentials_storage_path = credentials_storage_path
        if not flags:
            parser = argparse.ArgumentParser(description=__doc__,
                                             formatter_class=argparse.RawDescriptionHelpFormatter,
                                             parents=[tools.argparser])
            flags = parser.parse_args([])
        self.flags = flags

    def create(self, scope):
        from oauth2client import file, client, tools

        flow = client.flow_from_clientsecrets(self.client_secrets_path,
                                              scope=scope,
                                              message=tools.message_if_missing(self.client_secrets_path))

        storage = file.Storage(self.credentials_storage_path)
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            credentials = tools.run_flow(flow, storage, self.flags)

        return credentials

    def __str__(self):
        return "%s(client_secrets_path=%s, credentials_storage_path=%s, flags=%s)" % (
            self.__class__.__name__,
            repr(self.client_secrets_path),
            repr(self.credentials_storage_path),
            repr(self.flags))

    __repr__ = __str__
