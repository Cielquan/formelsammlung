# noqa: D205,D208,D400
"""
    tests.test_flask_sphinx_docs
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for flask_sphinx_docs.py.

    :copyright: (c) Christian Riedel
    :license: GPLv3
"""
from flask import Flask

from formelsammlung.flask_sphinx_docs import SphinxDocServer


def test_serving_direct_app(tmp_path):
    """Test doc serving for direct invoked app."""
    test_dir = tmp_path / "docs"
    test_dir.mkdir()
    test_file = test_dir / "index.html"
    test_file.write_text("TEST_CONTENT")

    app = Flask(__name__)
    SphinxDocServer(app, doc_dir=str(test_dir))
    client = app.test_client()

    resp = client.get("/docs/")
    assert resp.status_code == 200
    assert resp.data.decode() == "TEST_CONTENT"


def test_serving_factory_app(tmp_path):
    """Test doc serving for app-factory invoked app."""
    test_dir = tmp_path / "docs"
    test_dir.mkdir()
    test_file = test_dir / "index.html"
    test_file.write_text("TEST_CONTENT_2")

    sds = SphinxDocServer()

    def _create_app():
        app = Flask(__name__)
        sds.init_app(app, doc_dir=str(test_dir))
        return app

    app = _create_app()
    client = app.test_client()

    resp = client.get("/docs/")
    assert resp.status_code == 200
    assert resp.data.decode() == "TEST_CONTENT_2"
