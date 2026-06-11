import json
from pathlib import Path

from app.version import __version__


def test_backend_and_frontend_versions_match():
    package_path = Path(__file__).parents[2] / "frontend" / "package.json"
    frontend_version = json.loads(package_path.read_text())["version"]

    assert __version__ == "1.0.0"
    assert frontend_version == __version__
