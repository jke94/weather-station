import os
import sys
import unittest

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
SOURCE_ROOT = os.path.join(PROJECT_ROOT, "src")
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, SOURCE_ROOT)


def main() -> int:
    loader = unittest.TestLoader()
    suite = loader.discover(
        os.path.join(CURRENT_DIR, "unit_tests"),
        pattern="test_*.py",
        top_level_dir=PROJECT_ROOT,
    )
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())