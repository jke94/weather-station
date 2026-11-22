import os
import runpy
import sys
import unittest
from unittest.mock import patch

TEST_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TEST_DIRECTORY)

from run_unit_tests import main


class TestUnitTestRunner(unittest.TestCase):
    @patch("run_unit_tests.unittest.TextTestRunner")
    @patch("run_unit_tests.unittest.TestLoader")
    def test_main_returns_nonzero_when_tests_fail(
        self, mock_loader, mock_runner
    ):
        mock_result = mock_runner.return_value.run.return_value
        mock_result.wasSuccessful.return_value = False

        self.assertEqual(main(), 1)

    @patch("run_unit_tests.unittest.TextTestRunner")
    @patch("run_unit_tests.unittest.TestLoader")
    def test_main_returns_zero_when_tests_pass(self, mock_loader, mock_runner):
        mock_result = mock_runner.return_value.run.return_value
        mock_result.wasSuccessful.return_value = True

        self.assertEqual(main(), 0)

    @patch("run_unit_tests.unittest.TextTestRunner.run")
    @patch("run_unit_tests.unittest.TestLoader.discover")
    def test_script_exits_nonzero_when_tests_fail(
        self, mock_discover, mock_run
    ):
        mock_run.return_value.wasSuccessful.return_value = False

        with self.assertRaises(SystemExit) as error:
            runpy.run_path(
                os.path.join(TEST_DIRECTORY, "run_unit_tests.py"),
                run_name="__main__",
            )

        mock_discover.assert_called_once()
        self.assertEqual(error.exception.code, 1)
