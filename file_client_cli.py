import socket
import json
import base64
import logging

# server_address=('0.0.0.0',7777)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        # Look for the response, waiting until socket is done (no more data)
        data_received="" #empty string
        while True:
            #socket does not receive all data at once, data comes in part, need to be concatenated at the end of process
            data = sock.recv(16)
            if data:
                # data is not empty, concat with previous content
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                # no more data, stop the process by break
                break
        # at this point, data_received (string) will contain all data coming from the socket
        # to be able to use the data_received as a dict, need to load it using json.loads()
        hasil = json.loads(data_received.strip())
        logging.warning("data received from server:")
        return hasil
    except Exception as e:
        logging.warning(f"error during data receiving: {str(e)}")
        return False


def remote_list():
    command_str=f"LIST"
    hasil = send_command(command_str)
    if (hasil['status'] == 'OK'):
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Failed\n")
        return False

def remote_get(filename=""):
    command_str=f"GET {filename}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        namafile= hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        fp = open(namafile,'wb+')
        fp.write(isifile)
        fp.close()
        print(f"File {filename} berhasil didapatkan\n")
        return True
    else:
        print("Gagal")
        return False

def remote_upload(filepath=""):
    try:
        filename=filepath.split('/')[-1]
        with open(f"{filepath}",'rb') as fp:
            isifile = base64.b64encode(fp.read()).decode()
        command_str=f"UPLOAD {filename} {isifile}"
        hasil=send_command(command_str)
        if hasil and hasil['status']=='OK':
            print(f"File {filename} berhasil diupload")
        else:
            print("Failed\n")
    except Exception as e:
        logging.warning(f"Error uploading file: {str(e)}")
        return False

def remote_delete(filename=""):
    command_str=f"DELETE {filename}"
    hasil = send_command(command_str)
    if hasil and hasil['status']=='OK':
        print(f"File {filename} berhasil dihapus\n")
        return True
    else:
        print("Failed\n")
        return False
        
def main():
    while True:
        command = input().strip().split(maxsplit=1)
        print(command)
        
        if command[0] == "LIST":
            remote_list()
        elif command[0] == "GET":
            remote_get(command[1])
        elif command[0] == "UPLOAD":
            remote_upload(command[1])
        elif command[0] == "DELETE":
            remote_delete(command[1])
        elif command[0] == "EXIT":
            break
        else:
            print("Invalid syntax")

if __name__=='__main__':
    server_address=('172.16.16.101',7777)
    main()
