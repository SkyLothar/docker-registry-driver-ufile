# -*- coding: utf-8 -*-

from docker_registry.core import exceptions as de
from docker_registry import testing

from nose import tools

from .mock_session import MockSession


class TestQuery(testing.Query):
    def __init__(self):
        self.scheme = "ufile"


class TestDriver(testing.Driver):
    def __init__(self):
        self.scheme = "ufile"
        self.path = None
        self.config = testing.Config(dict(
            ufile_baseurl="http://bucket.ufile.ucloud.cn",
            ufile_public_key="public",
            ufile_private_key="private"
        ))

    def setUp(self):
        super(TestDriver, self).setUp()
        self._storage._session = MockSession()

    @tools.raises(de.FileNotFoundError, StopIteration)
    def test_empty_list_directory(self):
        path = self.gen_random_string()
        content = self.gen_random_string().encode('utf8')
        self._storage.put_content(path, content)

        iterator = self._storage.list_directory(path)
        next(iterator)

    # extra testing for better coverage
    def test_rm_tree(self):
        self._storage.put_content("/foo/bar/baz", "d")
        self._storage.put_content("/foo/quz", "d")
        self._storage.remove("foo/")

        tools.eq_(self._storage.exists("foo/bar/bar"), False)
        tools.eq_(self._storage.exists("foo/quz"), False)

    def test_exists_dir(self):
        self._storage.put_content("/foo/baz", "d")
        tools.eq_(self._storage.exists("foo/"), True)

        self._storage.remove("foo/")
        tools.eq_(self._storage.exists("foo/"), False)
