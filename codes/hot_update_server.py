import multiprocessing
from multiprocessing.reduction import recv_handle, send_handle
import socket


def server_hot_update(in_p, out_p):
    out_p.close()
    while True:
        fd = recv_handle(in_p)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, fileno=fd) as client:
            while True:
                msg = client.recv(1024)
                if msg.decode().isnumeric():
                    client.send(str(int(msg) + 2).encode())
                elif msg.decode() == 'update':
                    client.send(b'success')


def server(address, in_p, out_p, worker_pid):
    in_p.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    s.bind(address)
    s.listen(1)
    client, addr = s.accept()
    while True:
        msg = client.recv(1024)
        if msg.decode().isnumeric():
            client.send(str(int(msg) + 1).encode())
        elif msg.decode() == 'update':
            client.send(b'success')
            send_handle(out_p, client.fileno(), worker_pid)
            client.close()
            break


if __name__ == '__main__':
    c1, c2 = multiprocessing.Pipe()
    worker_p = multiprocessing.Process(target=server_hot_update, args=(c1, c2))
    worker_p.start()

    server_p = multiprocessing.Process(target=server,
                                       args=(('127.0.0.1', 15000), c1, c2, worker_p.pid))
    server_p.start()

    c1.close()
    c2.close()
"""
yingbingying@huawei.com

"""
