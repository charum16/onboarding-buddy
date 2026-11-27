import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from onboarding_buddy_ui.api import APIError, BuddyAPI


class BuddyAPITests(unittest.TestCase):
    def setUp(self):
        self.api = BuddyAPI("http://localhost:8080/")

    @patch("onboarding_buddy_ui.api.requests.Session.request")
    def test_list_conversations_uses_existing_endpoint(self, request):
        response = Mock(ok=True, status_code=200, content=b"[]")
        response.json.return_value = [{"id": 1, "convo_name": "Welcome"}]
        request.return_value = response

        result = self.api.list_conversations()

        self.assertEqual(result, [{"id": 1, "convo_name": "Welcome"}])
        self.assertEqual(request.call_args.args[:2], ("GET", "http://localhost:8080/conversations"))

    @patch("onboarding_buddy_ui.api.requests.Session.request")
    def test_send_message_uses_existing_payload(self, request):
        response = Mock(ok=True, status_code=200, content=b"{}")
        response.json.return_value = {"response": "Hello", "chunks": []}
        request.return_value = response

        result = self.api.send_message(9, "Hello there")

        self.assertEqual(result["response"], "Hello")
        self.assertEqual(request.call_args.kwargs["json"], {"content": "Hello there"})
        self.assertEqual(request.call_args.args[1], "http://localhost:8080/conversations/9/messages")

    @patch("onboarding_buddy_ui.api.requests.Session.request")
    def test_api_errors_are_reported(self, request):
        response = Mock(ok=False, status_code=400, text="bad request")
        response.json.return_value = {"detail": "Unsupported file type"}
        request.return_value = response

        with self.assertRaisesRegex(APIError, "Unsupported file type"):
            self.api.list_conversations()

    @patch("onboarding_buddy_ui.api.requests.Session.request")
    def test_connection_failure_is_actionable(self, request):
        import requests
        request.side_effect = requests.ConnectionError("offline")

        with self.assertRaisesRegex(APIError, "Check that the backend is running"):
            self.api.list_conversations()


if __name__ == "__main__":
    unittest.main()
