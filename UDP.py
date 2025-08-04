import socket
import Messages

user_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

peer_address = ('<peer>', 50999) # Replace with the actual peer address and port

message = Messages.profile_message
user_socket.sendto(message.encode(), peer_address)

data, peer = user_socket.recvfrom(1024)  # Buffer size is 1024 bytes
print(f"Received message: {data.decode()} from {peer}")

user_socket.close()

#get local IP address
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)