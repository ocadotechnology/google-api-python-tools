import unittest

from google_api_python_tools.dataproc.constants import ComputeEngineMachineType, DataprocImageVersion


class TestDataProcConstants(unittest.TestCase):
    def test_properly_calculates_machine_info(self):
        self.assertEqual(ComputeEngineMachineType.get_number_of_cores_for('n1-standard-4'), 4)
        self.assertEqual(ComputeEngineMachineType.get_number_of_cores_for('n1-highcpu-16'), 16)

        self.assertEqual(ComputeEngineMachineType.get_amount_of_memory_in_gb('n1-highcpu-2'), 1.8)
        self.assertEqual(ComputeEngineMachineType.get_amount_of_memory_in_gb('n1-highmem-4'), 26)

        self.assertAlmostEqual(ComputeEngineMachineType.get_per_hour_price_for('n1-standard-4'), 0.24)

    def test_has_all_available_machine_types(self):
        all_types = ComputeEngineMachineType.get_all()
        self.assertIn('n1-highmem-16', all_types)
        self.assertIn('n1-standard-2', all_types)
        self.assertIn('n1-highcpu-8', all_types)
        self.assertIn('n1-standard-32', all_types)

    def test_newest_image_is_listed_first(self):
        self.assertEqual(DataprocImageVersion.get_all()[0], DataprocImageVersion.V_1_0)
