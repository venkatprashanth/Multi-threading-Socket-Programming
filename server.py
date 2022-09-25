"""This module serves as server class
It will listen and connects to the nodes over the socket
It will have a global buffer to store different nodes data
Sends the data back to the nodes
The module also keep track of the port and it's respective clients
"""

import socket
import threading
from threading import Thread
from tabulate import tabulate
import json
import queue
import sys

# Local IP address
IP = socket.gethostbyname(socket.gethostname())

# Initial Port Number
PORT = 50009

# Socket Address   
ADDR = (IP, PORT)

# Size of the buffer to receive the socket data
SIZE = 1024

# Characters Encode Data for sending over the socket
FORMAT = "utf-8"

# Disconnect string message
DISCONNECT_MSG = "!DISCONNECT"

# Number of threads to generate depending on the input nodes
threads = []

# Table to hold the ports and client names
myTable = []

# Table Headers names
head = ["Client","Port"]

# Initializing a Queue
q = queue.Queue()

# Find the duplicate data and remove them
# Place the port and client in the table, if it is not present
# returns true if present else false
# Input: Port value
def find_data(port):
    if port in myTable:
        val = True
    else:
        val = False
    if port[0] == "!DISCONNECT":
        val = True
    return val

# Add port and client to the table for every client 
# Connected to the server
# It will parse the string from the received msg 
# and parse the addr value for port for adding it to the table
# Add the node name and port
# Input : Received Message and socket addr
# Print the table
def add_table_data(msg,addr):

    # List for storing port and node name
    list_data = []
    raw_msg = msg

    #split the received data with delimight string comma
    msg = msg.split(",")

    # Parse the port from the socket address
    port = str(addr[1])

    # Parse the node name from the received message
    client = str(msg[0])

    # Append client to the list
    list_data.append(client)

    # Append port to the list
    list_data.append(port)

    # Check the duplicate data if not present 
    # Add it to the table
    if(find_data(list_data)):
        print("Client Data Present in the table")
    else:
        if ((len(list_data[1]) > 0) and (raw_msg != "NULL")):
            myTable.append(list_data)

    print(tabulate(myTable, headers = head, tablefmt = "grid"))
    print("Size of the table",len(myTable))


# This function is similar to the server class
# It handles the client class (Nodes)
# It receives the data from the socket 
# Received data will be pushed to the queues
# It gets the data from the queue and compares with the port
# if the received port matches with the queue got data port
# It sends the data and wait for next available node
# Input: Socket Connection, Address and number of nodes
def handle_client(conn, addr,num_of_threads):

    # Connected variable is used to signal the socket
    # to close the socket and exit the thread
    connected = True
    while connected:
        try:

            msg = conn.recv(SIZE).decode(FORMAT)

            # recevied msg should not be equal to NULL
            if msg != "NULL":

                # add port and client to the table
                add_table_data(msg,addr)

                # if received msg is equal to disconnet
                # Close the socket and exit the thread
                if msg == DISCONNECT_MSG:
                    connected = False
                    break
                else:
                    q.put(msg)

                # Parse the recevied msg and get the node number
                data_parse = msg.split(",")
                data_parse = data_parse[0].split("-")
                data_parse = data_parse[1]

                # This will be used to peek into the queue without poping it.
                # This variable will be used to compare with current node number
                qu_peek = q.queue[0]
                data_comp = qu_peek.split(",")
                data_comp = data_comp[1]
                
                # Compare the node number and msg sending node number
                # if matches pop the data from the queue and send to the respective client
                if data_comp == data_parse:
                    msg = q.get()
                elif((data_comp > str(num_of_threads))):
                    msg = q.get()
                    msg = "NULL"
                else:
                    msg = "NULL"
            else:
                add_table_data(msg,addr)
                msg = "NULL"
            conn.send(msg.encode(FORMAT))

            # Signal the task as done
            q.task_done()
        
        # Raise error if any exception
        except Exception as e:
            print("Raised Error Exception:",e)

    conn.send(DISCONNECT_MSG.encode(FORMAT))
    conn.close()

# This functions is main class 
# It creates takes the node inputs as command line arguments
# It creates the n number of threads
# It joins the threads and exits the code
def main():

    print("[STARTING] Server is starting...")
    # Takes the node value as an command line argument
    num_of_threads = int(sys.argv[1])
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()

    for t in range(num_of_threads):
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr, num_of_threads))
        thread.start()
        threads.append(thread)

    # wait for the queue to finish
    q.join()

    # wait for threads to finish
    for thread in threads:
        thread.join()



if __name__ == "__main__":
    main()