# noqa: D205,D208,D400
"""
    tests.test_flask_sphinx_docs
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for flask_sphinx_docs.py.

    :copyright: (c) Christian Riedel
    :license: GPLv3
"""
from pathlib import Path

import pytest
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


def test_custom_index_file(tmp_path):
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


def doc_dir_guessing_option_1(tmp_path, monkeypatch):
    """Test guessing of doc dir with 'doc/_build'."""
    test_repo = tmp_path / "testrepo"
    test_repo.mkdir()

    py_code_dir = test_repo / "src" / "testrepo"
    py_code_dir.mkdir(parents=True)

    monkeypatch.setattr(Path, "parent", py_code_dir)

    with pytest.raises(IOError) as excinfo:
        SphinxDocServer._find_build_docs("")
        assert "No 'doc' or 'docs'" in str(excinfo.value)

    doc_dir = test_repo / "doc"
    doc_dir.mkdir()

    for child in doc_dir.iterdir(): print(child)

    with pytest.raises(IOError) as excinfo:
        SphinxDocServer._find_build_docs("")
        assert "No '_build' or 'build'" in str(excinfo.value)

    build_dir = doc_dir / "_build"
    build_dir.mkdir()

    with pytest.raises(IOError) as excinfo:
        SphinxDocServer._find_build_docs("")
        assert "No 'html'" in str(excinfo.value)

    html_dir = build_dir / "html"
    html_dir.mkdir()

    assert SphinxDocServer._find_build_docs("") == html_dir


def doc_dir_guessing_option_2(tmp_path, monkeypatch):
    """Test guessing of doc dir with 'docs/build'."""
    test_repo = tmp_path / "testrepo"
    test_repo.mkdir()

    py_code_dir = test_repo / "src" / "testrepo"
    py_code_dir.mkdir(parents=True)

    monkeypatch.setattr(Path, "parent", py_code_dir)

    with pytest.raises(IOError) as excinfo:
        SphinxDocServer._find_build_docs("")
        assert "No 'doc' or 'docs'" in str(excinfo.value)

    doc_dir = test_repo / "docs"
    doc_dir.mkdir()

    for child in doc_dir.iterdir(): print(child)

    with pytest.raises(IOError) as excinfo:
        SphinxDocServer._find_build_docs("")
        assert "No '_build' or 'build'" in str(excinfo.value)

    build_dir = doc_dir / "build"
    build_dir.mkdir()

    with pytest.raises(IOError) as excinfo:
        SphinxDocServer._find_build_docs("")
        assert "No 'html'" in str(excinfo.value)

    html_dir = build_dir / "html"
    html_dir.mkdir()

    assert SphinxDocServer._find_build_docs("") == html_dir
