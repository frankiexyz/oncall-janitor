import unittest
from unittest.mock import Mock
from oncall_janitor import fetch_alertmanager
import responses

requests = Mock()


class Test_oncalljanitor(unittest.TestCase):
    @responses.activate
    def test_fetch_alertmanger_no_alert(self):
        responses.add(responses.GET, "https://127.0.0.1", json=[], status=200)
        _, result = fetch_alertmanager("https://127.0.0.1")
        assert len(result) == 0

    @responses.activate
    def test_fetch_alertmanger_alerts(self):
        alert_sample = [
            {
                "annotations": {"summary": "Alert1"},
                "endsAt": "2020-11-24T02:58:04.627Z",
                "fingerprint": "fb70448b0c7dee8a",
                "labels": {
                    "alertname": "Alert1",
                },
                "receivers": [{"name": "event_rules"}],
                "startsAt": "2020-11-23T22:08:04.627Z",
                "status": {"inhibitedBy": [], "silencedBy": [], "state": "active"},
                "updatedAt": "2020-11-24T02:54:05.660Z",
            }
        ]
        responses.add(responses.GET, "https://127.0.0.1", json=alert_sample, status=200)
        _, result = fetch_alertmanager("https://127.0.0.1")
        assert len(result) == 1


if __name__ == "__main__":
    unittest.main()
