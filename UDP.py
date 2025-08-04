# udp_peer.py
import socket
import threading
import time
import Messages

# === CONFIGURATION ===
PORT = 50999
BUFFER_SIZE = 4096
PEER_IP = "192.168.1.52" # Replace with the actual peer IP address
DEFAULT_TTL = 3600  # 1 hour default

# === USER INPUTS ===
name = input("Enter your display name: ");
status = input("Enter your status: ");
verbose = threading.Event()  # Verbose mode flag

# === UDP SOCKET SETUP ===
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Allow address reuse
sock.bind(("0.0.0.0", PORT)) # Bind to all interfaces on the specified port
print(f"Successfully bound to port {PORT}")

# === PING MESSAGE ===
def broadcast_ping(name, status):
    ip_address = socket.gethostbyname(socket.gethostname())  # Get local IP

    while True:
        if verbose.is_set():
            msg = Messages.verboseProfMessage(
                    display_name=name,
                    ip_address=ip_address,
                    status=status,
                    av_type="image/png",
                    av_encoding="base64",
                    av_data="iVBORw0KGgoAAAANSUhEUgAAAAUA...")  # Truncated sample
        else: msg = Messages.simpleProfMessage( # remove if not needed
                    display_name=name,
                    status=status)
        
        ping = Messages.pingMessage(display_name=name, ip_address=ip_address)
        sock.sendto(msg.encode(), (PEER_IP, PORT))
        sock.sendto(ping.encode(), (PEER_IP, PORT))
        time.sleep(300) # wait for 5 minutes
        
# === RECEIVE LOOP ===
def receive_messages(verbose):
    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        message = data.decode()
        print(f"\n{message}\n")
        
        # Auto-reply ACK if MESSAGE_ID is found
        message_lines = message.strip().splitlines()
        msg_type = None
        message_id = None

        for line in message_lines:
            if line.startswith("TYPE:"):
                msg_type = line.split(":", 1)[1].strip()
            elif line.startswith("MESSAGE_ID:"):
                message_id = line.split(":", 1)[1].strip()

        # Automatically ACK messages (DM, POST, etc.)
        if message_id and msg_type != "ACK":
            ack = Messages.ackMessage({message_id})
            if verbose.is_set():
                sock.sendto(ack.encode(), addr)



# === SEND LOOP ===
def send_messages(name, status, verbose):
    ip_address = socket.gethostbyname(socket.gethostname())  # Get local IP
    ttl = DEFAULT_TTL  # Default TTL
    while True: 
        command = input("Enter command (--help for options): ")
        match command:
            case "--help":
                print("Available commands:\n--help,\n--exit,\n--verbose,\n--ttl\nprofile,\npost,\ndm")
            case "--verbose":
                if verbose.is_set():
                    verbose.clear() 
                    print("Verbose mode disabled.")
                else: 
                    verbose.set()
                    print("Verbose mode enabled.")
            case "--ttl": 
                getTTL = input(f"Enter TTL in seconds (default = {DEFAULT_TTL}): ").strip()
                ttl = int(getTTL) if getTTL.isdigit() else DEFAULT_TTL
            case "profile":
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
                print("Profile Message sent.")
            case "post":
                content = input("Enter your post content: ")
                if (not verbose):
                    msg = Messages.simplePostMessage(
                        display_name=name, 
                        content=content,
                        av_type="image/png",
                        av_encoding="base64",
                        av_data="iVBORw0KGgoAAAANSUhEUgAAAAUA...")
                else:
                    msg = Messages.verbosePostMessage(
                        display_name=name,
                        ip_address=ip_address,
                        ttl=ttl,
                        content=content,
                        av_type="image/png",
                        av_encoding="base64",
                        av_data="iVBORw0KGgoAAAANSUhEUgAAAAUA..."
                    )
                sock.sendto(msg.encode(), (PEER_IP, PORT))
                print("Post message sent.")
            case "dm":
                recName = input("Enter recipient's display name: ")
                message = input("Enter your message: ")
                userID = f"{recName}@{PEER_IP}"
                if (not verbose):
                    msg = Messages.simpleDMMessage(sender=name, message=message)
                else:
                    msg = Messages.verboseDMMessage(
                        sender=name,
                        ip_address=ip_address,
                        userID=userID,
                        message=message,
                        ttl=ttl
                    )
                sock.sendto(msg.encode(), (PEER_IP, PORT))
                print("Direct message sent.")
            case "--exit":
                print("Exiting...")
                sock.close()
                return


# === RUN THREADS ===
recv_thread = threading.Thread(target=receive_messages, args=(verbose,), daemon=True)
recv_thread.start()
ping_thread = threading.Thread(target=broadcast_ping, args=(name, status,), daemon=True)
ping_thread.start()

send_messages(name, status, verbose)  # Runs in main thread
