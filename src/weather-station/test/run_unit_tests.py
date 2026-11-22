from pathlib import Path
import runpy


if __name__ == "__main__":
    repository_root = Path(__file__).resolve().parents[3]
    runpy.run_path(
        str(repository_root / "test" / "run_unit_tests.py"),
        run_name="__main__",
    )
