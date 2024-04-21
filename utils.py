FORMAT = "utf-8"
HEADER_LENGTH = 10


def receive_data(client_socket, is_file=False):
    try:
        data_header = client_socket.recv(HEADER_LENGTH)
        if not len(data_header):
            return False
        data_length = int(data_header.decode(FORMAT).strip())
        data_returned = client_socket.recv(data_length)
        return data_returned if is_file else data_returned.decode(FORMAT)

    except:
        return False


def send_data(client_socket, data):
    if type(data) is not bytes:
        data = data.encode(FORMAT)
    data_header = f"{len(data):<{HEADER_LENGTH}}".encode(FORMAT)
    client_socket.send(data_header + data)
