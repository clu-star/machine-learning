import socket
import sys
import glob
from thread import *

HOST = ""
PORT = 10080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error code: ' + str(msg[0]) + ' Message: ' + msg[1]
    sys.exit()

s.listen(10) # accept up to 10 connections

def clientthread(conn):
    conn.send('Welcome to Diagnosum, please send your PNG\n')

    counter = len(glob.glob1('received_images/',"*.png"))
    i=counter+1
    print(i)
    f = open('received_images/ri'+ str(i)+".png",'wb') #open in binary
    i=i+1

    while (True):       
    # receive and write the file
        buf = conn.recv(1024)
        while (buf):
            f.write(buf)
            buf = conn.recv(1024)
	    if not buf: break
    f.close()

    # process received image

    # send response JSON

    sc.close()

while 1:
    conn, addr = s.accept()
    print addr

    start_new_thread(clientthread ,(conn,))

s.close()
