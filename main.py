from multiprocessing import Process
from http_handler import *
import asyncio
from config import *
import socket


class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.server_socket.bind((HOST, PORT))
        except socket.error as err:
            self.server_socket.close()
            print(err)

        self.server_socket.listen()
        self.server_socket.setblocking(False)

    def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.accept_connection())

    async def accept_connection(self):
        loop = asyncio.get_event_loop()
        while True:
            client_socket, _ = await loop.sock_accept(self.server_socket)
            request_handler = RequestHandler(loop, client_socket)
            loop.create_task(request_handler.handle_request())


def main():
    server = Server()
    print(str.format("http server started on {}:{}", HOST, PORT))

    processes = []
    for i in range(CPU_LIMIT):
        p = Process(target=server.start)
        processes.append(p)
        p.start()

    try:
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        for process in processes:
            process.terminate()
        server.server_socket.close()


if __name__ == '__main__':
    main()
