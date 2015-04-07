# -*- coding: utf-8 -*-

import io
import logging

from docker_registry.core import exceptions as de

from requests import compat


logger = logging.getLogger(__name__)


class StubResponse(object):
    def __init__(self, status_code, content="", json=None, headers=None):
        self.status_code = status_code
        self.content = content
        self.headers = headers or {}
        self.headers["content-length"] = len(content)
        self.headers["etag"] = "mock-etag"
        self.json_content = json or {}

    def __str__(self):
        return "<StubResponse {0}>".format(self.status_code)

    @property
    def ok(self):
        return self.status_code // 100 < 3

    def iter_content(self, chunk_size):
        content = io.BytesIO(self.content)
        data = content.read(chunk_size)
        while data:
            yield data
            data = content.read(chunk_size)

    def iter_lines(self):
        for line in self.text.splitlines():
            yield line

    def json(self):
        return self.json_content

    @property
    def text(self):
        if isinstance(self.content, bytes):
            return self.content.decode("utf8")
        else:
            return self.content

    def raise_for_status(self):
        if not self.ok:
            raise ValueError("Reqests Error")


class MockSession(object):
    def __init__(self):
        self._storage = dict()
        self._headers = dict()

    def _get_path(self, url):
        s_url = compat.urlsplit(url)
        return s_url.path

    def _not_there(self, path):
        raise de.FileNotFoundError("{0} is not there".format(path))

    def get(self, url, **options):
        path = self._get_path(url)
        key = path[1:]

        content = self._storage.get(key)
        if not content:
            return StubResponse(404)

        h_range = options.get("headers", {}).get("range")
        if h_range:
            l, r = h_range.split("=")[1].split("-")
            content = content[int(l): int(r) + 1]

        return StubResponse(200, content, headers=self._headers.get(key, {}))

    def head(self, url, **options):
        return self.get(url, **options)

    def put(self, url, **options):
        path = self._get_path(url)
        key = path[1:]

        self._storage[key] = options["data"]
        self._headers[key] = options.get("headers", {})

        return StubResponse(200)

    def post(self, url, **options):
        if "?uploads" in url:
            return StubResponse(200, json=dict(BlkSize=10, UploadId="id"))
        else:
            return StubResponse(200)

    def delete(self, url, **options):
        path = self._get_path(url)
        key = path[1:]

        if key in self._storage:
            del self._storage[key]
            del self._headers[key]
            return StubResponse(200)
        else:
            return StubResponse(404)
