import socket
 
myname = socket.getfqdn(socket.gethostname())
myaddr = socket.gethostbyname(myname)

print(myname, myaddr)
print(myaddr[:3])