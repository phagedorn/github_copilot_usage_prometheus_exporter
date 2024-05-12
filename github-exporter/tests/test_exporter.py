import unittest
import sys
from unittest.mock import patch, MagicMock
sys.path.append('../github_copilot_usage_prometheus_exporter')
from prometheus_client.core import GaugeMetricFamily

# Import the script/module you want to test
import github_copilot_usage_prometheus_exporter as exporter

class TestGitHubCopilotUsagePrometheusExporter(unittest.TestCase):
    def test_fetch_data(self):
        """
        Test fetching data correctly handles API responses.
        """
        # Example of mocking requests.get to simulate API response
        with patch('requests.get') as mocked_get:
            # Simulate a successful API response
            mocked_get.return_value.ok = True
            mocked_get.return_value.json.return_value = {
                'count': 100,
                'uniques': 50
            }

            data = exporter.fetch_data()
            mocked_get.assert_called_once()
            self.assertEqual(data, {'count': 100, 'uniques': 50})

            # Simulate a failed API response
            mocked_get.return_value.ok = False
            data = exporter.fetch_data()
            self.assertIsNone(data)

    def test_process_metrics(self):
        """
        Test processing metrics updates the Prometheus gauge correctly.
        """
        # Setup a mock for the Prometheus Gauge set method
        with patch.object(exporter.github_usage, 'set', autospec=True) as mock_set:
            data = {'count': 200, 'uniques': 120}
            exporter.process_metrics(data)
            mock_set.assert_called_with(200)  # Assuming we're only setting 'count'

    # Additional tests can be added here to cover more functions and edge cases

if __name__ == '__main__':
    unittest.main()
