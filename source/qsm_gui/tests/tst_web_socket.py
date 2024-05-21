# coding:utf-8
import socket
import base64
import hashlib


# WebSocket 握手请求
def create_handshake_request(host, port, path):
    key = base64.b64encode("some_random_key")
    request = (
        "GET {} HTTP/1.1\r\n"
        "Host: {}:{}\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        "Sec-WebSocket-Key: {}\r\n"
        "Sec-WebSocket-Version: 13\r\n\r\n"
    ).format(path, host, port, key)
    return request


# 发送 WebSocket 数据帧
def send_websocket_message(sock, message):
    encoded_message = message.encode('utf-8')
    message_length = len(encoded_message)

    # 创建 WebSocket 帧头
    frame_header = bytearray()
    frame_header.append(129)  # 10000001: FIN, Text Frame

    if message_length <= 125:
        frame_header.append(message_length)
    elif message_length <= 65535:
        frame_header.append(126)
        frame_header.extend(message_length.to_bytes(2, byteorder='big'))
    else:
        frame_header.append(127)
        frame_header.extend(message_length.to_bytes(8, byteorder='big'))

    # 发送帧头和消息
    sock.sendall(bytes(frame_header)+encoded_message)


# 接收 WebSocket 数据帧
def receive_websocket_message(sock):
    response = sock.recv(1024)
    if response:
        print("Received: ", response)


# 连接到 WebSocket 服务器并发送消息
def connect_and_send(host, port, path, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    # 发送 WebSocket 握手请求
    handshake_request = create_handshake_request(host, port, path)
    sock.sendall(handshake_request)

    # 接收服务器握手响应
    response = sock.recv(1024)
    if b"101 Switching Protocols" in response:
        print("Handshake successful")

        # 发送消息
        send_websocket_message(sock, message)

        # 接收服务器响应
        receive_websocket_message(sock)

    sock.close()


if __name__ == '__main__':
    host = 'localhost'
    port = 12345
    path = '/'
    message = 'Hello, Server!'

    connect_and_send(host, port, path, message)

