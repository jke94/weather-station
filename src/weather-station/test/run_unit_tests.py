import unittest
import sys
import os

# Obtener la ruta absoluta del directorio actual (donde está run_unit_tests.py)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Agregar al sys.path el directorio 'weather-station' (dos niveles arriba)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, PROJECT_ROOT)

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.discover("unit_tests", pattern="test_*.py")
    runner = unittest.TextTestRunner()
    runner.run(suite)
