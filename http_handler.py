import asyncio
from response import *
from http_parser import HttpParser
import mimetypes
import os.path
from consts import *
from urllib.parse import unquote
from config import *
import socket


class RequestHandler:
    def __init__(self, loop: asyncio.AbstractEventLoop, client_socket: socket.socket):
        self.loop = loop
        self.client_socket = client_socket

    async def handle_request(self):
        request = b""
        while True:
            buf = (await self.loop.sock_recv(self.client_socket, READ_BUF_SIZE))
            request += buf
            if buf:
                break
        await self._handle_request(request)
        self.client_socket.close()

    async def _handle_request(self, request: bytes):
        p = parse_request(request)

        if p.get_method() not in [METHOD_GET, METHOD_HEAD]:
            response = build_bad_client_response(405)
            await self.loop.sock_sendall(self.client_socket, response)
            return

        filename, extension, code = get_filename_from_path(p.get_path())
        if code != 200:
            response = build_bad_client_response(code)
            await self.loop.sock_sendall(self.client_socket, response)
            return

        await self.send_ok_response(p, filename, extension)

    async def send_ok_response(self, p: HttpParser, filename: str, extension: str):
        content_length = os.path.getsize(filename)
        content_type = mimetypes.types_map[extension]

        response = build_ok_response(200, content_type=content_type, content_length=content_length)
        await self.loop.sock_sendall(self.client_socket, response)

        if p.get_method() == METHOD_GET:
            await self.send_body(filename)

    async def send_body(self, filename: str):
        with open(filename, 'rb') as file:
            string = file.read(SEND_BUF_SIZE)
            while len(string) > 0:
                await self.loop.sock_sendall(self.client_socket, string)
                string = file.read(SEND_BUF_SIZE)


def parse_request(request: bytes) -> HttpParser:
    p = HttpParser()
    try:
        p.execute(request)
    except ValueError:
        pass
    return p


def get_filename_from_path(path: str) -> (str, str, int):
    path = unquote(path)

    search_for_index_html = False
    if path.endswith("/"):
        split_path = path.split("/")
        last_part = split_path[len(split_path) - 2]
        if last_part.find(".") > 0:
            return "", "", 404
        path += "index.html"
        search_for_index_html = True

    path = DOCUMENT_ROOT + path

    if '/..' in path:
        return "", "", 403

    if os.path.exists(path):
        _, extension = os.path.splitext(path)
        return path, extension, 200

    return "", "", 403 if search_for_index_html else 404
