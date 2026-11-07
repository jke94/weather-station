import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

import requests

from services.facebook_create_post_service import create_post


class TestFacebookCreatePostService(unittest.TestCase):

    @patch('services.facebook_create_post_service.requests.post')
    def test_create_post_returns_url_when_facebook_succeeds(self, mock_post):
        response = mock_post.return_value
        response.json.return_value = {'id': '123_456'}

        result = create_post('page-id', 'access-token', 'Weather report')

        self.assertEqual(result, 'https://www.facebook.com/123_456')
        mock_post.assert_called_once()

    @patch('services.facebook_create_post_service.requests.post')
    def test_create_post_logs_facebook_error_details(self, mock_post):
        response = mock_post.return_value
        response.status_code = 400
        response.json.return_value = {
            'error': {
                'message': 'Invalid OAuth access token.',
                'type': 'OAuthException',
                'code': 190
            }
        }
        response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            '400 Client Error',
            response=response
        )

        output = StringIO()
        with redirect_stdout(output):
            result = create_post('page-id', 'access-token', 'Weather report')

        self.assertEqual(result, 'NONE')
        self.assertIn('Invalid OAuth access token.', output.getvalue())
        self.assertIn("'code': 190", output.getvalue())
