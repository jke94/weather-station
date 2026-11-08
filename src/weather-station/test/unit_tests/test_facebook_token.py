import os
import sys
import unittest
from unittest.mock import Mock, patch

UTILS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "utils")
)
sys.path.insert(0, UTILS_DIR)

from generate_facebook_long_lived_token import get_long_lived_token


class FacebookTokenTests(unittest.TestCase):
    @patch("generate_facebook_long_lived_token.requests.get")
    def test_exchange_uses_app_id_as_client_id(self, mock_get):
        response = Mock()
        response.ok = True
        response.json.return_value = {
            "access_token": "long-lived-token",
            "expires_in": 5184000,
        }
        mock_get.return_value = response

        result = get_long_lived_token(
            "app-id",
            "app-secret",
            "short-lived-user-token",
        )

        self.assertEqual(result["access_token"], "long-lived-token")
        mock_get.assert_called_once_with(
            "https://graph.facebook.com/v25.0/oauth/access_token",
            params={
                "grant_type": "fb_exchange_token",
                "client_id": "app-id",
                "client_secret": "app-secret",
                "fb_exchange_token": "short-lived-user-token",
            },
            timeout=30,
        )

    @patch("generate_facebook_long_lived_token.requests.get")
    def test_exchange_reports_graph_api_error(self, mock_get):
        response = Mock()
        response.ok = False
        response.status_code = 400
        response.text = "Bad request"
        response.json.return_value = {
            "error": {"message": "Error validating application."}
        }
        mock_get.return_value = response

        with self.assertRaisesRegex(
            RuntimeError, "Error validating application"
        ):
            get_long_lived_token("app-id", "app-secret", "short-token")


if __name__ == "__main__":
    unittest.main()
