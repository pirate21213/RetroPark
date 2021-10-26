"""
This script is from https://www.thepythoncode.com/code/send-receive-files-using-sockets-python
Client that sends the file (uploads)
"""
import socket
import tqdm
import os
import argparse

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024


def send_file(filename, host, port):
    # get the file size
    filesize = os.path.getsize(filename)
    # create the client socket
    s = socket.socket()
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")

    # send the filename and filesize
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())

    # start sending the file
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in
            # busy networks
            s.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))

    # close the socket
    s.close()


def receive_file(save_path):
    # device's IP address
    SERVER_HOST = "0.0.0.0"
    SERVER_PORT = 5001

    # create the server socket
    # TCP socket
    s = socket.socket()
    # bind the socket to our local address
    s.bind((SERVER_HOST, SERVER_PORT))
    # enabling our server to accept connections
    # 5 here is the number of unaccepted connections that
    # the system will allow before refusing new connections
    s.listen(5)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
    # accept connection if there is any
    client_socket, address = s.accept()
    # if below code is executed, that means the sender is connected
    print(f"[+] {address} is connected.")

    # receive the file infos
    # receive using client socket, not server socket
    received = client_socket.recv(BUFFER_SIZE).decode()
    print("Received...")
    filename, filesize = received.split(SEPARATOR)
    print("filename is {}, filesize is {}".format(filename, filesize))

    # Create path if not existent
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # remove absolute path if there is
    filename = os.path.basename(filename)
    print("base filename is {}".format(filename))
    filename = os.path.join(save_path, filename)
    print("saving file to {}".format(filename))
    # convert to integer
    filesize = int(filesize)

    # start receiving the file from the socket
    # and writing to the file stream
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    print("Opening file locally at {}".format(filename))
    with open(filename, "wb") as f:
        while True:
            # read 1024 bytes from the socket (receive)
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                # nothing is received
                # file transmitting is done
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))
            # print("Filename: ".format(filename))
        f.flush()
    # close the client socket
    client_socket.close()
    # close the server socket
    s.close()
    return True


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Simple File Sender")
    parser.add_argument("file", help="File name to send")
    parser.add_argument("host", help="The host/IP address of the receiver")
    parser.add_argument("-p", "--port", help="Port to use, default is 5001", default=5001)
    args = parser.parse_args()
    file = args.file
    host = args.host
    port = args.port
    send_file(file, host, port)
