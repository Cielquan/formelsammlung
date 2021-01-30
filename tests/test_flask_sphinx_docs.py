"""
    tests.test_flask_sphinx_docs
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for flask_sphinx_docs.py.

    :copyright: (c) 2020, Christian Riedel and AUTHORS
    :license: GPL-3.0-or-later, see LICENSE for details
"""  # noqa: D205,D208,D400
# pylint: disable=W0212
from pathlib import Path

import pytest

from flask import Flask

from formelsammlung.flask_sphinx_docs import SphinxDocServer


def test_serving_direct_app(tmp_path) -> None:
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


def test_serving_factory_app(tmp_path) -> None:
    """Test doc serving for app-factory invoked app."""
    test_dir = tmp_path / "docs"
    test_dir.mkdir()
    test_file = test_dir / "index.html"
    test_file.write_text("TEST_CONTENT_2")

    sds = SphinxDocServer()

    def _create_app() -> None:
        app = Flask(__name__)
        sds.init_app(app, doc_dir=str(test_dir))
        return app

    app = _create_app()
    client = app.test_client()

    resp = client.get("/docs/")
    assert resp.status_code == 200
    assert resp.data.decode() == "TEST_CONTENT_2"


def test_custom_index_file(tmp_path) -> None:
    """Test custom index file."""
    test_dir = tmp_path / "docs"
    test_dir.mkdir()
    test_file = test_dir / "custom.html"
    test_file.write_text("TEST_CONTENT")

    app = Flask(__name__)
    SphinxDocServer(app, doc_dir=str(test_dir), index_file="custom.html")
    client = app.test_client()

    resp = client.get("/docs/")
    assert resp.status_code == 200
    assert resp.data.decode() == "TEST_CONTENT"


def test_no_app_root() -> None:
    """Test error when no app root dir is given."""
    with pytest.raises(OSError, match="Got no root dir"):
        SphinxDocServer._find_built_docs("")


@pytest.mark.parametrize(
    ("doc_dir_name", "build_dir_name"), [("doc", "_build"), ("docs", "build")]
)
def test_doc_dir_guessing_option_1(
    doc_dir_name, build_dir_name, tmp_path, monkeypatch
) -> None:
    """Test guessing of doc dir with 'doc/_build'."""
    test_repo = tmp_path / "testrepo"
    test_repo.mkdir()

    py_code_dir = test_repo / "src" / "testrepo"
    py_code_dir.mkdir(parents=True)

    monkeypatch.setattr(Path, "parent", py_code_dir)

    with pytest.raises(OSError, match="No 'doc' or 'docs'"):
        SphinxDocServer._find_built_docs("fake_app_root")

    doc_dir = test_repo / doc_dir_name
    doc_dir.mkdir()

    with pytest.raises(OSError, match="No '_build' or 'build'"):
        SphinxDocServer._find_built_docs("fake_app_root")

    build_dir = doc_dir / build_dir_name
    build_dir.mkdir()

    with pytest.raises(OSError, match="No 'html'"):
        SphinxDocServer._find_built_docs("fake_app_root")

    html_dir = build_dir / "html"
    html_dir.mkdir()

    assert SphinxDocServer._find_built_docs("fake_app_root") == html_dir
