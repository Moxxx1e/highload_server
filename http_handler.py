import socket
import asyncio
from response import *
from http_parser import HttpParser
import mimetypes
import os.path
from consts import *
from urllib.parse import unquote
from config import *


def parse_request(request: bytes):
    p = HttpParser()
    try:
        p.execute(request)
    except ValueError:
        pass
    return p


def get_filename_from_path(path: str) -> (str, str, int):
    path = unquote(path)

    index_flag = False
    if path.endswith("/"):
        # TODO: refactor
        split_path = path.split("/")
        last_part = split_path[len(split_path) - 2]
        if last_part.find(".") > 0:
            return "", "", 404
        path += "index.html"
        index_flag = True

    path = DOCUMENT_ROOT + path

    if '/..' in path:
        return "", "", 403

    if os.path.exists(path):
        _, extension = os.path.splitext(path)
        return path, extension, 200

    return "", "", 403 if index_flag else 404


SEND_BUF_SIZE = 16384


async def send_body(loop, client_socket, filename):
    with open(filename, 'rb') as file:
        string = file.read(SEND_BUF_SIZE)
        while len(string) > 0:
            await loop.sock_sendall(client_socket, string)
            string = file.read(SEND_BUF_SIZE)


async def handle_request(loop, client_socket: socket.socket, request: bytes):
    p = parse_request(request)

    if p.get_method() not in [METHOD_GET, METHOD_HEAD]:
        response = build_bad_client_response(405)
        await loop.sock_sendall(client_socket, response)
        return

    filename, extension, code = get_filename_from_path(p.get_path())
    if code != 200:
        response = build_bad_client_response(code)
        await loop.sock_sendall(client_socket, response)
        return

    content_length = os.path.getsize(filename)
    content_type = mimetypes.types_map[extension]

    response = build_ok_response(200, content_type=content_type, content_length=content_length)
    await loop.sock_sendall(client_socket, response)

    if p.get_method() == METHOD_GET:
        await send_body(loop, client_socket, filename)


READ_BUF_SIZE = 4096


async def read_request(loop, client_socket: socket.socket):
    request = ""
    while True:
        buf = (await loop.sock_recv(client_socket, READ_BUF_SIZE)).decode()
        request += buf
        # TODO: fix
        if '\r\n' in buf or len(buf) == 0:
            break
    await handle_request(loop, client_socket, request.encode())
    client_socket.close()


async def accept_connection(server_socket: socket.socket):
    loop = asyncio.get_event_loop()

    while True:
        client_socket, addr = await loop.sock_accept(server_socket)
        loop.create_task(read_request(loop, client_socket))
