# udp_peer.py
import socket
import threading
import Messages

# === CONFIGURATION ===
PORT = 50999
BUFFER_SIZE = 4096
PEER_IP = "192.168.1.52" # Replace with the actual peer IP address

# === UDP SOCKET SETUP ===
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", PORT)) # Bind to all interfaces on the specified port
print(f"Successfully bound to port {PORT}")

# === RECEIVE LOOP ===
def receive_messages():
    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        print(f"\nReceived from {addr}:\n{data.decode()}\n")

# === USER INPUTS ===
name = input("Enter your display name: ");
status = input("Enter your status: ");
verbose = False  # Verbose mode flag

# === SEND LOOP ===
def send_messages(name, status):
    ip_address = socket.gethostbyname(socket.gethostname())  # Get local IP
    while True: 
        command = input("Enter command (--help for options): ")
        match command:
            case "--help":
                print("Available commands:\n--help,\n--exit,\n--verbose,\n--profile,\n--post,\n--dm")
            case "--verbose":
                verbose = True;
                print("Verbose mode enabled.")
            case "--profile":
                if (not verbose):
                    msg = Messages.simpleProfMessage(display_name=name, status=status)
                else: msg = Messages.verboseProfMessage(
                    display_name=name,
                    ip_address=ip_address,
                    status=status,
                    av_type="image/png",
                    av_encoding="base64",
                    av_data="iVBORw0KGgoAAAANSUhEUgAAAAUA..."  # Truncated sample
                )
                sock.sendto(msg.encode(), (PEER_IP, PORT))
                print("Message sent.")
            case "--exit":
                print("Exiting...")
                sock.close()
                return

# === RUN THREADS ===
recv_thread = threading.Thread(target=receive_messages, args=(verbose,), daemon=True)
recv_thread.start()

send_messages(name, status)  # Runs in main thread
