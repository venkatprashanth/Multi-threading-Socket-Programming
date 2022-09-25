"""Node Class clients will connect to the server on startup
It will open any number of nodes to connect to the server
It will generate the input files to send to the server
It will also receive the data from server and store in the output files
"""

import sys
import threading
import socket
from socket import *

# Local IP address
serverHost =  "127.0.1.1" #Local IP address

# Server port
serverPort = 50009        

# Character encoding for sending over the socket
FORMAT = "utf-8"

# Variable to store the number of threads
threads = []

# Path to store the client generated node files
in_path = "/home/prashanth/CN_Ass1/input_node_files"

# Path to store the client received node files
out_path = "/home/prashanth/CN_Ass1/output_node_files"

# This function is used to generate client sending files
# Create a text file with node name and write the data
# Input : Thread name
# Output : File stored path 
def create_input_files(node_name):
    final_path = in_path + "/" + "node" + str(node_name) + ".txt"
    try:
        with open(final_path, 'a') as f:
            f.write("ABCDEFG\n")
            f.write ("1234567\n")
            f.write("This data will be sent to the node")
    except FileNotFoundError:
        print("File Not Found:",final_path)
    
    f.close()
    return final_path

# This function is used to store the received data from the server
# Data will be stored in respective output text files with node name
# Input : Received data and node name
def write_output(data_recv,node_name):
    final_path = out_path + "/" + "node" + str(node_name) + ".txt"
    data_recv = str(data_recv)
    try:
        f = open(final_path,"a")
        f.write(data_recv)
        f.write("\n")
    except FileNotFoundError:
        print("Output File Not found")

# This function is used to build the packet as per the frame format
# Input: Node name, Final path and Index
# Output : Returns the packet with specified format
def build_pkt(node_name,final_path,index):
    lines = []
    data_out = 0
    try:
        f = open(final_path,'r')
        lines = f.readlines()
    except FileNotFoundError:
        print("File Not Found",final_path)
    f.close()
    src = "node-"+node_name
    dest = int(node_name)+index
    data_out = lines[index-1]
    data_size = len(data_out)
    if index == 3:
        dest = dest + 1
    if data_size == 0:
        pkt = src+","+str(dest)+","+str(data_size)
    else:
        pkt = src+","+str(dest)+","+str(data_size)+","+data_out
    return pkt

# Worker threads to generate number of nodes
# This also acts a Node class clients it initiates
# As per the input argument between 0 to 255
# It makes an socket connection over the TCP/IP
# It initiates the socket connection the server
# It receives and sends the data over the socket
# It sends and receives the data from the server
# It also neglects the unnecesary data
def worker():
    sock_obj = socket(AF_INET, SOCK_STREAM)
    sock_obj.connect((serverHost, serverPort))
    thread_name = threading.currentThread().getName()
    thread_name = thread_name.split("-")
    print("Current Node is:",thread_name[1])
    file_path = create_input_files(thread_name[1])

    # Count to store the packets as per the frame format
    count = 0

    while True:
        count = count + 1
        if count == 4:
            count = 0
        i = count
        data_send = build_pkt(thread_name[1],file_path,i)
        print("data_send",data_send)
        sock_obj.send(data_send.encode(FORMAT))
        data_recv = sock_obj.recv(1024)
        data_recv = data_recv.decode(FORMAT)
        print('Received Data is:', data_recv)
        if ((data_recv != "NULL") or (len(data_recv) <= 0)):
            write_output(data_recv,thread_name[1])

    sock_obj.send(DISCONNECT_MSG.encode(FORMAT))
    sock_obj.close()

# This functions is main class 
# It creates takes the node inputs as command line arguments
# It creates the n number of threads
# It joins the threads and exits the code
def main():
    num_of_threads = int(sys.argv[1])
    # thread generation block
    for t in range(num_of_threads):
        th = threading.Thread(target=worker)
        th.start()
        print(f"[ACTIVE CONNECTIONS1] {threading.activeCount() - 1}")

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()