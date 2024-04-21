import pickle
import socket, threading, sys
from utils import receive_data, send_data

HOST = "localhost"
FORMAT = "utf-8"
PORT = 15555
HEADER_LENGTH = 10
BUFFER_SIZE = 1024
OUTPUT_FILES_DIRECTORY = "./output_fichiers/"




def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))


    while True:
        print("Commands available: LIST, EXIT")
        command = input(">")
        if command.upper().strip() not in {
            "LIST", "EXIT"
        }:
            continue
        send_data(client_socket, command)
        match command:
            case "EXIT":
                client_socket.close()
                break
            case "LIST":

                list_fichiers = receive_data(client_socket)
                if list_fichiers is False:
                    continue
                print(list_fichiers)
                print("Faites votre choix en sélectionnant le numéro correspondant au fichier désiré\n")
                num_file = input(">")
                print(f"Vous avez chosis le fichier numéro: {num_file}")
                send_data(client_socket, "FILE")
                send_data(client_socket, num_file)
                file_name = receive_data(client_socket)
                if file_name is False:
                    continue
                serialized_file = receive_data(client_socket, is_file=True)
                if serialized_file is False:
                    continue
                file_received = pickle.loads(serialized_file)
                with open(OUTPUT_FILES_DIRECTORY+file_name, 'wb') as file:
                    file.write(file_received)




if __name__ == '__main__':
    main()

