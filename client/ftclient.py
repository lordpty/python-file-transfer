#Author - Nicklas Knudson

import socket
import sys

def prompt():
    sys.stdout.write('\n>>')

def getWord(data, pos):
    words = []
    for word in data.split():
        words.append(word)
    try:
        return words[pos]
    except:
        return -1

def main():
    #Get command line arguments. If none, exit.
    if (len(sys.argv) < 3):
        print 'Usage: python ftclient.py <hostname> <port>'
        sys.exit()

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    HOST_2 = ''
    PORT_2 = 30020

    #Create the socket
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c_socket.settimeout(2)

    #Attempt to connect to the host
    try:
        c_socket.connect((HOST,PORT))
    except:
        print 'Unable to establish a connection'
        sys.exit()

    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    data_socket.bind((HOST_2, PORT_2))
    data_socket.listen(10)

    #Set up a receive loop
    while 1:
        #write the server introduction message
        data = c_socket.recv(4096)
        if not data:
            print 'Disconnected from the server'
            sys.exit()
        else:
            sys.stdout.write(data)
            prompt()

        while 1:
            msg_all = sys.stdin.readline()
            msg = getWord(msg_all, 0)

            if msg == 'exit':
                exit_flag = 1
                try:
                    c_socket.sendall(msg)
                    new_data = c_socket.recv(4096)
                    print str(new_data)
                    exit_flag = 0
                except:
                    print 'Message failed to send. Terminating Script.'
                    sys.exit()

                if exit_flag == 0:
                    print 'Terminating script. Thanks for stopping by.'
                    sys.exit()

            elif msg == 'list':
                try:
                    c_socket.sendall(msg)
                    #Code file receive loop here
                    try:
                        new_data = conn.recv(1024)
                    except:
                        conn, addr = data_socket.accept()
                        new_data = conn.recv(4096)
                    print str(new_data)
                    prompt()
                except:
                    print 'Message failed to send'
                    sys.exit()

            elif msg == 'get':
                file_name = getWord(msg_all, 1)
                if (file_name == -1):
                    print '[get] usage: get <filename>'
                    prompt()
                else:
                    try:
                        c_socket.sendall(msg_all)
                        #Code file receive loop here
                        try:
                            new_data = conn.recv(1024)
                        except:
                            conn, addr = data_socket.accept()
                            new_data = conn.recv(1024)
                        print str(new_data)
                        if new_data == 'Sending File.':
                            downFile = open(file_name, 'wb')
                            while True:
                                file_data = conn.recv(1024)
                                while file_data:
                                    if file_data.endswith("EOFEOFEOFEOFEOFX"):
                                        write_data = file_data[:-16]
                                        downFile.write(write_data)
                                        break
                                    else:
                                        downFile.write(file_data)
                                        file_data = conn.recv(1024)
                                break
                            #Close the file and prompt the user
                            downFile.close()
                            print 'The file [%s] has been received.' % file_name
                        prompt()
                    except:
                        print 'Message failed to send'
                        sys.exit()

            elif msg:
                try:
                    c_socket.sendall(msg)
                    #Code file receive loop here
                    new_data = c_socket.recv(4096)
                    print str(new_data)
                    prompt()
                except:
                    print 'Message failed to send'

if __name__ == "__main__":
    main()



