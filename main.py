from multiprocessing import Process
from http_handler import *
import asyncio
from config import *


def main_loop(server_socket: socket.socket):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(accept_connection(server_socket))


def create_server_socket() -> socket.socket:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server_socket.bind((HOST, PORT))
    except socket.error as err:
        server_socket.close()
        print(err)

    server_socket.listen()
    server_socket.setblocking(False)
    return server_socket


def main():
    server_socket = create_server_socket()
    print(str.format("http server started on {}:{}", HOST, PORT))

    processes = []
    for i in range(CPU_LIMIT):
        p = Process(target=main_loop, args=(server_socket,))
        processes.append(p)
        p.start()

    try:
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        for process in processes:
            process.terminate()
        server_socket.close()


if __name__ == '__main__':
    main()
