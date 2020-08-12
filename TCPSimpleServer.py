import asyncio
import logging
from socket import *

def create_tcp_server(loop, address):
    """
    Create new tcp server.
    args:
        loop: asyncio loop or similar.
        address: tuple with host and port.
    """
    def internal_dec(callback):
        """
        Wrap Callback.
        args:
            callback: callback to be executed by the server.
        """
        loop.create_task(tcp_server(loop, address, callback))
        return callback
    return internal_dec

async def tcp_server(loop, address, callback):
    """
    Start tcp server.
    args:
        loop: asyncio loop or similar.
        address: tuple with host and port.
        callback: callback to be executed by the server.
    """
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    sock.setblocking(False)
    while True:
        client, addr = await loop.sock_accept(sock)
        logging.info('Connection from' + str(addr))
        loop.create_task(dicovery_handler(loop, client, addr, callback))


async def dicovery_handler(loop, client, addr, callback):
    """
    Handler triggered when server receive 
    a message.
    args:
        client: addres of the message client.
        loop: asyncio loop or similar.
        callback: callback to be executed by the server.
    """
    with client:
        while True:
            data = await loop.sock_recv(client, 10000)
            if not data:
                break
            callback(data)
    logging.info('Connection closed')
