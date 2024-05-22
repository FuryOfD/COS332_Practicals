import os
import socket
import hashlib
import time
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

LOCAL_FILE_PATH = config['DEFAULT']['LocalFilePath']
REMOTE_FILE_PATH = config['DEFAULT']['RemoteFilePath']
SERVER_IP = config['DEFAULT']['ServerIP']
SERVER_PORT = int(config['DEFAULT']['ServerPort'])
SERVER_USERNAME = config['DEFAULT']['Username']
SERVER_PASSWORD = config['DEFAULT']['Password']
POLLING_INTERVAL = int(config['DEFAULT']['PollingInterval'])

def connect_to_ftp_server():
    ftp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ftp_socket.connect((SERVER_IP, SERVER_PORT))
    response = ftp_socket.recv(1024).decode()
    if not response.startswith('220'):
        print('Error connecting to FTP server:', response)
        return None
    return ftp_socket

def login(ftp_socket):
    ftp_socket.sendall(f'USER {SERVER_USERNAME}\r\n'.encode())
    response = ftp_socket.recv(1024).decode()
    if not response.startswith('331'):
        print('Error logging in:', response)
        return False
    ftp_socket.sendall(f'PASS {SERVER_PASSWORD}\r\n'.encode())
    response = ftp_socket.recv(1024).decode()
    if not response.startswith('230'):
        print('Error logging in:', response)
        return False
    return True

def download_file(ftp_socket, file_path):
    ftp_socket.sendall('PASV\r\n'.encode())
    response = ftp_socket.recv(1024).decode()
    
    start = response.find('(') + 1
    end = response.find(')')
    numbers = response[start:end].split(',')
    ip_address = '.'.join(numbers[:4])
    port = (int(numbers[4]) * 256) + int(numbers[5])

    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.connect((ip_address, port))

    ftp_socket.sendall('RETR {}\r\n'.format(file_path).encode())
    response = ftp_socket.recv(1024).decode()
    
    if not response.startswith('150'):
        print('Error downloading file:', response)
        return False
    
    with open(LOCAL_FILE_PATH, 'wb') as local_file:
        while True:
            data = data_socket.recv(1024)
            if not data:
                break
            local_file.write(data)
    response = ftp_socket.recv(1024).decode()
    if not response.startswith('226'):
        print('Error downloading file:', response)
        return False
    return True

def calculate_file_hash(file_path):
    with open(file_path, 'rb') as file:
        file_hash = hashlib.md5()
        while chunk := file.read(4096):
            file_hash.update(chunk)
    return file_hash.hexdigest()

def main():
    ftp_socket = connect_to_ftp_server()
    if not ftp_socket:
        return

    if not login(ftp_socket):
        return

    while True:
        if os.path.exists(LOCAL_FILE_PATH):
            local_file_hash = calculate_file_hash(LOCAL_FILE_PATH)
            good_file_hash = calculate_file_hash(REMOTE_FILE_PATH)
            if local_file_hash != good_file_hash:
                print("Local file has been modified. Restoring from server...")
                if download_file(ftp_socket, REMOTE_FILE_PATH):
                    print("File restored successfully.")
                else:
                    print("Failed to restore file from server.")
            else: print("Local file looks good!")
        else:
            print("Local file is missing. Restoring from server...")
            if download_file(ftp_socket, REMOTE_FILE_PATH):
                print("File restored successfully.")
            else:
                print("Failed to restore file from server.")

        time.sleep(POLLING_INTERVAL) 

if __name__ == "__main__":
    main()

