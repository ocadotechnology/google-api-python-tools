HTTP_ERROR_EXCEPTIONS = []
try:
    from googleapiclient.errors import HttpError

    HTTP_ERROR_EXCEPTIONS.append(HttpError)
except ImportError:
    pass

try:
    from apiclient import errors

    HTTP_ERROR_EXCEPTIONS.append(errors.HttpError)
except ImportError:
    pass


class GCEApiException(Exception):
    def __init__(self, ex):
        super(GCEApiException, self).__init__(ex)
        self.error = ex
        self.status = 0
        self._message = "%s: %s" % (str(ex), ex.message if hasattr(ex, 'message') else None)

        if isinstance(ex, tuple(HTTP_ERROR_EXCEPTIONS)):
            self.status = ex.resp.status

    @property
    def message(self):
        if self._message:
            return self._message
        if hasattr(self.error, '_get_reason'):
            return self.error._get_reason()
        if hasattr(self.error, 'message'):
            return "%s: %s" % (str(self.error), self.error.message)

    def __str__(self):
        return self.message

    @classmethod
    def from_json(cls, error_dict):
        ex = GCEApiException(Exception())
        ex.status = error_dict['error']['code']
        ex._message = error_dict['error']['message']
        return ex

    @classmethod
    def from_response(cls, response):
        error_dict = response.json()
        try:
            return cls.from_json(error_dict)
        except KeyError:
            ex = GCEApiException(Exception())
            ex.status = response.status_code
            import json
            ex._message = json.dumps(error_dict.get('message'))
            return ex
