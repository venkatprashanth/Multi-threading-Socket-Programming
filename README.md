# Multi-threading-Socket-Programming

Requirments
1. Python 3.x
2. Full Support for Linux

Features
1. program that will spawn multiple node objects and threads, as well as a server object and worker threads. 
2. The server will use a listening socket to allow nodes to connect to it, and spawn workerthreads as needed to allow inter-node communication. 
3. The nodes will open a file, and send data to other nodes via the server. 
4. The nodes will save all data that was sent to them in the form of output files.

Packages Installation
1. pip install tabulate
2. git clone https://github.com/venkatprashanth/Multi-threading-Socket-Programming.git

Source Code Execution
1. Server Code: Python3 server.py
2. Client Code: Python3 client.py

Change the path of the storage as per your system dir
# Path to store the client generated node files
in_path = "/home/prashanth/CN_Ass1/input_node_files"

# Path to store the client received node files
out_path = "/home/prashanth/CN_Ass1/output_node_files"

Client and Port Mapped Table
![Port_client](https://user-images.githubusercontent.com/45161178/192128887-e86d977e-4843-448a-9833-f648b614adf0.png)
