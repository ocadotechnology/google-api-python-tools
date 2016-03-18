import mock

with mock.patch('time.sleep'):
    import unittest

    from apiclient import errors
    from httplib2 import Response

    from google_api_python_tools.google_connectors.gceapiexception import GCEApiException
    from google_api_python_tools.google_connectors.utils import retry_on

    class TestClass(object):
        def some_method(self):
            pass

        def recovery_method(self):
            pass

    def error(x):
        return GCEApiException(errors.HttpError(Response({'status': x}), ""))

    class TopException(Exception):
        pass

    class DerivedException(TopException):
        pass

    class SomeDifferentException(Exception):
        pass

    class TestNetworkUtils(unittest.TestCase):
        def setUp(self):
            self.mocked_object = mock.Mock(TestClass)

        def test_retries_on_404(self):
            @retry_on('404', action_on_expected_failure=lambda ex: self.mocked_object.recovery_method())
            def tester():
                return self.mocked_object.some_method()

            self.mocked_object.some_method.side_effect = [error(404), error(404), "OK"]

            self.assertEqual(tester(), "OK")
            self.assertEqual(len(self.mocked_object.recovery_method.call_args_list), 2)

        def test_retries_on_some_method_traceback(self):
            @retry_on(expected_tracebacks='some_method')
            def tester():
                return self.mocked_object.some_method()

            self.mocked_object.some_method.side_effect = [error(404), error(404), "OK"]

            self.assertEqual(tester(), "OK")
            self.assertEqual(len(self.mocked_object.recovery_method.call_args_list), 0)

        def test_fails_on_404_after_number_of_retries_exceeded(self):
            @retry_on('404')
            def tester():
                return self.mocked_object.some_method()

            self.mocked_object.some_method.side_effect = [error(404), error(404), error(404), "OK"]

            self.assertRaises(GCEApiException, tester)

        def test_raises_exception_immediately_if_not_expected(self):
            @retry_on('404')
            def tester():
                return self.mocked_object.some_method()

            self.mocked_object.some_method.side_effect = Exception('unexpected')

            self.assertRaises(Exception, tester)

        def test_combination_of_retries(self):
            @retry_on('503')
            @retry_on('404')
            def tester():
                return self.mocked_object.some_method()

            self.mocked_object.some_method.side_effect = [error(404),
                                                          GCEApiException(Exception('503')), error(404), "OK"]

            self.assertEqual(tester(), "OK")

        def test_retries_with_messages_given_as_list(self):
            @retry_on(['404', '503'], max_retries=4)
            def tester():
                return self.mocked_object.some_method()

            self.mocked_object.some_method.side_effect = [error(404),
                                                          GCEApiException(Exception('503')), error(404), "OK"]

            self.assertEqual(tester(), "OK")

        def test_retries_when_either_class_or_message_matches(self):
            @retry_on(expected_messages='msg', expected_classes=TopException)
            def tester():
                return self.mocked_object.some_method()

            self.mocked_object.some_method.side_effect = [Exception('msg'), TopException(), SomeDifferentException()]

            self.assertRaises(SomeDifferentException, tester)

        def test_retries_on_expected_exception(self):
            @retry_on(expected_classes=TopException)
            def tester():
                return self.mocked_object.some_method()

            self.mocked_object.some_method.side_effect = [DerivedException(), SomeDifferentException()]

            self.assertRaises(SomeDifferentException, tester)
