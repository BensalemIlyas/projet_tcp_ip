import socket, threading, os
from utils import receive_data, send_data
import pickle
import sys
import time

HOST = "localhost"
HEADER_LENGTH = 10
FORMAT = "utf-8"
PORT = 15555
BUFFER_SIZE = 1024
FILES_DIRECTORY = './fichiers/'
fichiers = os.listdir(FILES_DIRECTORY)


def handle_client(client_socket):

    while True:

        command = receive_data(client_socket)
        if command is False:
            continue

        print(f"command sent by client is {command}")
        match command:
            case "EXIT":
                break
            case 'LIST':
                list_fichiers = ""
                for i, fichier in enumerate(fichiers):
                    list_fichiers += f"{i}: {fichier}\n"
                send_data(client_socket, list_fichiers)

            case 'FILE':
                num_file = receive_data(client_socket)
                print(f"vous avez selectionné le fichier numéro : {num_file}")
                num_file = int(num_file)
                send_data(client_socket, fichiers[num_file])
                # Open the file to be sent
                with open(FILES_DIRECTORY+fichiers[num_file], 'rb') as file:
                    file_data = file.read()
                # Serialize the file data using Pickle
                serialized_data = pickle.dumps(file_data)

                # Send the serialized data
                send_data(client_socket, serialized_data)


    client_socket.close()
    print('Les données ont été envoyées')


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Le serveur écoute sur {HOST}:{PORT}")

        while True:
            client_socket, address = server_socket.accept()
            print("la communication avec le client est établie")
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()


if __name__ == '__main__':
    main()
