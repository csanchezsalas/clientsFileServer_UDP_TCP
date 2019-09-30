"""
TECNOLÓGICO DE COSTA RICA
CAMPUS TECNOLÓGICO LOCAL SAN CARLOS

CHRISTIAN SÁNCHEZ SALAS

TAREA PROGRAMADA - CURSO REDES - PROTOCOLO IP/(TCP - UDP)

II SEMESTRE
SEPTIEMBRE, 2019"""

from socket import *
import os
import sys

"""TCP CLIENT
PARAMETERS: HOST SERVER, PORT, FLAG (-d,-u,-l), FILE NAME
IT ALLOWS THE CLIENT TO COMMUNICATE VIA TCP TO DOWNLOAD, LIST AND UPLOAD FILES FROM/TO THE SERVER"""


def client_tcp(ip_address, port, to_do, n_file):

    # THIS TRIES TO MAKE THE CONNECTION VIA SOCKETS

    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((ip_address, port))

    except error:
        print("CONNECTION FAILED!\n")
        return

    # to_do: DOWNLOAD (-d), UPLOAD (-u), LIST (-l)
    # DOWNLOAD
    if to_do == '-d' or to_do == '-D':

        try:
            s.send(bytes(to_do, "utf8"))
            mssg = str(s.recv(1024).decode('ascii'))
            print(mssg)
            data = n_file  # "test_img.jpg"
            s.send(bytes(data, "utf8"))  # sends filename
            file_bytes = s.recv(1024)
            file_bytes_parsed = str(file_bytes.decode('ascii'))
            if file_bytes_parsed == "ERR":  # if not then it contains the file size
                print("File does not exist\n")
            else:
                file_size = int(file_bytes_parsed)

                f = open(".\\downloads\\"+data, 'wb')
                to_write = s.recv(1024)
                total_recv = len(to_write)
                f.write(to_write)
                while total_recv < file_size:
                    to_write = s.recv(1024)
                    total_recv += len(to_write)
                    f.write(to_write)
                    print("{0:.2f}".format((total_recv/float(file_size))*100)+"% Done")
                print("Download complete!\n")

            s.close()
        except error:
            print("DOWNLOAD FAILED\n")
    # UPLOAD
    elif to_do == '-u' or to_do == '-U':
        try:
            s.send(bytes(to_do, "utf8"))
            mssg = str(s.recv(1024).decode('ascii'))
            print(mssg)

            data = n_file  # "new_test_img.jpg"
            arr = os.listdir('./files_to_upload')
            data_size = str(os.path.getsize('.\\files_to_upload\\' + data))
            print("File size: " + data_size)
            s.send(bytes(data, "utf8"))
            response = s.recv(1024)
            response = str(response.decode('ascii'))
            print(response)
            s.send(bytes(data_size, "utf8"))
            if arr.count(data) > 0:  # this checks if file to upload exists
                with open('.\\files_to_upload\\' + data, 'rb') as f:
                    bytes_to_send = f.read(1024)
                    s.send(bytes_to_send)
                    while True:
                        upload_status = s.recv(1024)
                        upload_status = str(upload_status.decode('ascii'))

                        if upload_status == "UPLOADING":
                            bytes_to_send = f.read(1024)
                            s.send(bytes_to_send)
                        else:

                            break
                s.close()

            else:
                print("FILE TO UPLOAD DOES NOT EXIST\n")
            # print_lock.release()
            s.close()
        except error:
            print("UPLOAD FAILED!\n")
    # LIST
    elif to_do == '-l':
        s.send(bytes(to_do, "utf8"))
        # mssg = str(s.recv(1024).decode('ascii'))
        print("\nTHANKS FOR ACCESSING TO THE FILE_SERVER!!\nTHE FOLLOWING FILES ARE AVAILABLE FOR "
              "DOWNLOADING:")
        while True:
            try:

                # item_file = ""
                item = s.recv(1024)
                item_file = str(item.decode('ascii'))
                if item_file.find("DONE") > 0:
                    print(item_file.replace("DONE", '\n'))
                    break
                else:
                    print(item_file)
            except error:
                print("ERROR WHILE PRINTING FILE LIST FROM THE SERVER\n")
        s.close()
    else:
        print("COMMAND UNKNOWN, PLEASE USE '-d' || '-u' || '-l' INSTEAD\nBYE! ^_^")
        # return


"""UDP CLIENT
PARAMETERS: HOST SERVER, PORT, FLAG (-d,-u,-l), FILE NAME
IT ALLOWS THE CLIENT TO COMMUNICATE VIA TCP TO DOWNLOAD, LIST AND UPLOAD FILES FROM/TO THE SERVER"""
def client_udp(ip_address, port, to_do, n_file):
    # host = '192.168.56.1'
    # port = 12345
    try:
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect((ip_address, port))

    except error:
        print("CONNECTION FAILED!\n")
        return

    s.sendto(bytes(to_do, "utf8"), (ip_address, port))  # sending what to_do to the server_udp
    # to_do: DOWNLOAD (-d), UPLOAD (-u), LIST (-l)
    # LIST
    if to_do == '-l' or to_do == '-L':
        while True:
            try:
                d = s.recvfrom(1024)
                data = d[0]
                if str(data.decode('ascii')) == "DONE":
                    break
                print(str(data.decode('ascii')))
            except error:
                print('CONNECTION FAILED!\n')
        s.close()
    # DOWNLOAD
    elif to_do == '-d' or to_do == '-D':
        try:
            # s.sendto(bytes(to_do, "utf8"), (ip_address, port))
            mssg = s.recvfrom(1024)
            mssg_data = mssg[0]
            addr = mssg[1]
            print(mssg_data)
            data = n_file  # "test_img.jpg"
            s.sendto(bytes(data, "utf8"), addr)  # sends filename
            file_bytes = s.recvfrom(1024)
            file_bytes_data = file_bytes[0]
            addr = file_bytes[1]
            file_bytes_parsed = str(file_bytes_data.decode('ascii'))
            if file_bytes_parsed == "ERR":  # if not then it contains the file size
                print("File does not exist\n")
            else:
                file_size = int(file_bytes_parsed)

                f = open(".\\downloads\\" + data, 'wb')
                to_write = s.recvfrom(1024)
                to_write_data = to_write[0]
                addr = to_write[1]
                total_recv = len(to_write_data)
                f.write(to_write_data)
                while total_recv < file_size:
                    to_write = s.recvfrom(1024)
                    to_write_data = to_write[0]
                    addr = to_write[1]
                    total_recv += len(to_write_data)
                    f.write(to_write_data)
                    print("{0:.2f}".format((total_recv / float(file_size)) * 100) + "% Done")
                print("Download complete!\n")

            s.close()
        except error:
            print("DOWNLOAD FAILED\n")
    # UPLOAD
    elif to_do == '-u' or to_do == '-U':
        try:

            mssg = s.recvfrom(1024)
            mssg_data = mssg[0]
            addr = mssg[1]
            print(mssg_data)

            data = n_file  # "new_test_img.jpg"
            arr = os.listdir('./files_to_upload')
            data_size = str(os.path.getsize('.\\files_to_upload\\' + data))
            print("File size: " + data_size)
            s.sendto(bytes(data, "utf8"), addr)
            response = s.recvfrom(1024)
            response_data = response[0]
            addr = response[1]
            response_parsed = str(response_data.decode('ascii'))
            print(response_parsed)
            s.sendto(bytes(data_size, "utf8"), addr)
            if arr.count(data) > 0:  # this checks if file to upload exists
                with open('.\\files_to_upload\\' + data, 'rb') as f:
                    bytes_to_send = f.read(1024)
                    s.sendto(bytes_to_send, addr)
                    while True:
                        upload_status = s.recvfrom(1024)
                        upload_status_data = upload_status[0]
                        addr = upload_status[1]
                        upload_status_parsed = str(upload_status_data.decode('ascii'))

                        if upload_status_parsed == "UPLOADING":
                            bytes_to_send = f.read(1024)
                            s.sendto(bytes_to_send, addr)
                        else:

                            break
                s.close()

            else:
                print("FILE TO UPLOAD DOES NOT EXIST\n")
            # print_lock.release()
            s.close()
        except error:
            print("UPLOAD FAILED!\n")
    else:
        print("COMMAND UNKNOWN, PLEASE USE '-d' || '-u' || '-l' INSTEAD\nBYE! ^_^")

    s.close()

    return 0


if __name__ == '__main__':

    # to run this program please go to cmd and insert:
    # tcp/udp ip_adress port_number -u/-d/-l filename
    # def client_tcp(program, ip_adress, port, to_do, n_file):

    program = sys.argv[1]
    ip_address = sys.argv[2]
    port = int(sys.argv[3])
    to_do = sys.argv[4]
    n_file = sys.argv[5]
    if program == "tcp" or program == "TCP":
        client_tcp(ip_address, port, to_do, n_file)

    elif program == "udp" or program == "UDP":
        client_udp(ip_address, port, to_do, n_file)
    else:
        print("WRONG program INPUT\nPLEASE CHOOSE ONE OF THE FOLLOWING 'tcp\\udp' ")
