#Author - Nicklas Knudson

import socket
import sys
from thread import *
import os
from os import listdir
from os.path import isfile, join
import time


def getWord(data, pos):
    words = []
    for word in data.split():
        words.append(word)
    return words[pos]

def clientThread(conn, addr):
    #Send a 'Hello' Message to the client
    HOST = str(addr[0])
    PORT = 30020
    connect_message = 'You are connected to the server. Operable commands: [list], [get] <filename>, or [exit].'
    conn.send(connect_message)

    this_path = os.path.dirname(os.path.abspath(__file__))
    only_files = [ f for f in listdir(this_path)if isfile(join(this_path,f))]
    files_minus_server = []
    for file in only_files:
        if file == 'ftserver.py':
            continue
        else:
            files_minus_server.append(file)

    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Infinite loop
    while True:
        data = conn.recv(1024)
        if data:
            first_word = getWord(data, 0)
            if first_word == 'list':
                try:
                    data_socket.sendall(str(str_files))
                except:
                    data_socket.settimeout(2)
                    data_socket.connect((HOST, PORT))
                    #list directory contents
                    print ('Getting directory contents')
                    str_files = str(files_minus_server).strip('[]')
                    data_socket.sendall(str(str_files))

            elif first_word == 'get':
                #initiate file transfer
                second_word = getWord(data, 1)
                file_check = False
                for files in only_files:
                    if files == second_word:
                        #File is present in directory
                        try:
                            data_socket.sendall('Sending File.')
                        except:
                            data_socket.settimeout(2)
                            data_socket.connect((HOST, PORT))
                            data_socket.sendall('Sending File.')

                        file_check = True

                        #File Transfer
                        with open(second_word, 'rb') as f:
                            while True:
                                fileData = f.read()
                                if fileData == '':
                                    break
                                data_socket.sendall(fileData)

                        #close the connection
                        f.close()
                        time.sleep(0.8)
                        data_socket.sendall('EOFEOFEOFEOFEOFX')
                        time.sleep(0.8)

                if file_check == False:
                    try:
                        data_socket.sendall('File not found. Try again.')
                    except:
                        data_socket.settimeout(2)
                        data_socket.connect((HOST, PORT))
                        data_socket.sendall('File not found. Try again.')

            elif first_word == 'exit':
                #Close the connection
                conn_closing_msg = 'Exit command received, closing connection.'
                print(str(conn_closing_msg))
                conn.sendall(conn_closing_msg)
                conn.close()
                return
            elif first_word:
                #invalid command
                invalid_command = 'Inoperable command. Operable commands: [list], [get] <filename>, or [exit].'
                conn.sendall(invalid_command)
        if not data:
            break

    #No data, connection broken
    print('Client has disconnected')
    data_socket.close()
    conn.close()



def main():
    PORT = 30021
    HOST = ''

    #Attempt to create the socket
    try:
        s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s_socket.bind((HOST, PORT))
        s_socket.listen(10)

        #Try to identify and broadcast host IP address
        try:
            server_ip = socket.gethostbyname(socket.gethostname())
        except socket.error, msg:
            print('Failed to get host server IP using socket.gethostbyname(localhost)')

    except socket.error, msg:
        print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error Message : ' + msg[1])
        sys.exit()

    print('Server established on Port: ' + str(PORT) + ' and IP: ' + str(server_ip))

    while 1:
        conn, addr = s_socket.accept()
        print('Connected to ' + addr[0])
        start_new_thread(clientThread, (conn, addr))

    #Close the socket when finished
    s_socket.close()

if __name__ == "__main__":
    main()




