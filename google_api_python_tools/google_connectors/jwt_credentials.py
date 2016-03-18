import httplib2

from google_api_python_tools.google_connectors.connector import CredentialFactory


class PlainJwtCredentialsFactory(CredentialFactory):
    def __init__(self, service_account_name, private_key):
        self.service_account_name = service_account_name
        self.private_key = private_key

    def create(self, scope):
        import oauth2client.crypt

        oauth2client.crypt.Signer = oauth2client.crypt.PyCryptoSigner
        oauth2client.crypt.Verifier = oauth2client.crypt.PyCryptoVerifier

        from oauth2client.client import SignedJwtAssertionCredentials

        return SignedJwtAssertionCredentials(
                service_account_name=self.service_account_name,
                private_key=self.private_key,
                scope=scope
        )

    def obtain_auth_headers(self, scope):
        credentials = self.create(scope)
        credentials.refresh(httplib2.Http())
        return {'Authorization': 'Bearer ' + credentials.token_response['access_token']}

    def __str__(self):
        return "%s(service_account_name=%s, private_key='***PRIVATE-KEY***')" % (self.__class__.__name__,
                                                                                 repr(self.service_account_name),)


class FileBasedJwtCredentialsFactory(PlainJwtCredentialsFactory):
    def __init__(self, private_key_path, service_account_name):
        self.service_account_name = service_account_name
        self.private_key_path = private_key_path

    def create(self, scope):
        with open(self.private_key_path) as key:
            self.private_key = key.read()

        return super(FileBasedJwtCredentialsFactory, self).create(scope)

    def __str__(self):
        return "%s(private_key_path=%s, service_account_name=%s)" % (self.__class__.__name__,
                                                                     repr(self.private_key_path),
                                                                     repr(self.service_account_name),)

    __repr__ = __str__
