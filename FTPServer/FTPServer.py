#!/usr/bin/python3

# FTPServer

from pyftpdlib.authorizers import DummyAuthorizer   #type: ignore
from pyftpdlib.handlers import FTPHandler           #type: ignore
from pyftpdlib.servers import FTPServer             #type: ignore
import argparse



def start(user,passwd,host = '127.0.0.1') -> None :
    
    EXTERNAL_IP = host
    PASV_PORTS = range(60000, 65535)

    authorizer = DummyAuthorizer()
    authorizer.add_user(user, passwd, "File", perm='w')  # only file upload is permitted

    handler = FTPHandler
    handler.authorizer = authorizer

    # Set the passive mode ports and external IP
    handler.passive_ports = PASV_PORTS
    handler.masquerade_address = EXTERNAL_IP

    server = FTPServer(('', 2121), handler)
    server.serve_forever()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FTP Server')
    parser.add_argument('-u', '--user', required = True, dest = 'user', help = 'Username for FTP user')
    parser.add_argument('-p', '--pass', required = True, dest = 'password', help = 'Password for FTP user')
    parser.add_argument('--host', help = 'Hostname/IP of the FTP Server')
    args = parser.parse_args()
    
    start(args.user, args.password, args.host)

