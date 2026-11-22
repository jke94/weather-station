import unittest
import sys
import os

# Get the absolute path of the current directory (where run_unit_tests.py is)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Add the 'weather-station' directory to the sys.path (two levels up)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, PROJECT_ROOT)

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.discover("unit_tests", pattern="test_*.py")
    runner = unittest.TextTestRunner()
    runner.run(suite)