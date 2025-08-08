# udp_peer.py
import socket
import threading
import time
import Messages

# === CONFIGURATION ===
PORT = 50999
BUFFER_SIZE = 4096
PEER_IP = "10.50.168.225" # Replace with the actual peer IP address
DEFAULT_TTL = 3600  # 1 hour default

# === USER INPUTS ===
name = input("Enter your display name: ")
status = input("Enter your status: ")
verbose = threading.Event()  # Verbose mode flag
peers = {} # store peer data 
followers = {}
peers_mess = {} # store message data 

# === UDP SOCKET SETUP ===
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Allow address reuse
sock.bind(("0.0.0.0", PORT)) # Bind to all interfaces on the specified port
print(f"Successfully bound to port {PORT}")

# === PING MESSAGE ===
def broadcast_ping(name, verbose):
    ip_address = socket.gethostbyname(socket.gethostname())  # Get local IP

    while True:
        if verbose.is_set():
            ping = Messages.pingMessage(display_name=name, ip_address=ip_address)
            for user_id, info in peers.items():
                    sock.sendto(ping.encode(), (info["ip"], PORT))
            time.sleep(20) # wait for 5 minutes
        

# === RECEIVE LOOP ===
def receive_messages(verbose):
    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        message = data.decode().strip()
        print(f"{message}\n")

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
            ack = Messages.ackMessage(message_id)
            if verbose.is_set():
                sock.sendto(ack.encode(), addr)

        # Take note of known peers
        if msg_type == "PROFILE":
            user_id = None
            display_name = None
            status = None

            for line in message_lines:
                if line.startswith("USER_ID:"):
                    user_id = line.split(":", 1)[1].strip()
                elif line.startswith("DISPLAY_NAME:"):
                    display_name = line.split(":", 1)[1].strip()
                elif line.startswith("STATUS:"):
                    status = line.split(":", 1)[1].strip()
            
            if user_id and display_name:
                peers[user_id] = {
                    "display_name": display_name,
                    "status": status,
                    "ip": addr[0]
                }

        # Stores known peers messages
        if msg_type in {"POST", "DM"}:
            sender_id = None
            for line in message_lines:
                if line.startswith("FROM:"):
                    sender_id = line.split(":", 1)[1].strip()

            if sender_id:
                peers_mess.setdefault(sender_id, []).append(message)

        if msg_type == "FOLLOW":
            follower = None
            for line in message_lines:
                if line.startswith("FROM"):
                    follower = line.split(":", 1)[1].strip()

            if follower:
                followers[follower] = {
                    "user_id": follower,
                    "ip": addr[0]
                }



# === SEND LOOP ===
def send_messages(name, status, verbose):
    ip_address = socket.gethostbyname(socket.gethostname())  # Get local IP
    ttl = DEFAULT_TTL  # Default TTL
    while True: 
        command = input("\nEnter command (--help for options): ")
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
            case "--peers":
                print("\n=== Known Peers ===")
                for user_id, info in peers.items():
                    print(f"{info['display_name']} ({user_id}) - {info.get('status', '')}")

                    msgs = peers_mess.get(user_id, [])
                    print(f"  Messages from {info['display_name']} ({len(msgs)}):")
                    for msg in msgs:
                        print("    ---")
                        print("    " + "\n    ".join(msg.strip().splitlines()))
                print("====================\n")
            case "profile":
                if verbose.is_set():
                    msg = Messages.verboseProfMessage(
                    display_name=name,
                    ip_address=ip_address,
                    status=status
                )
                else: msg = Messages.simpleProfMessage(display_name=name, status=status)
                
                sock.sendto(msg.encode(), ('<broadcast>', PORT))
                print("\nTYPE: ACK\nSTATUS: RECEIVED")
            case "post":
                content = input("Enter your post content: ")
                if verbose.is_set():
                    msg = Messages.verbosePostMessage(
                        display_name=name,
                        ip_address=ip_address,
                        ttl=ttl,
                        content=content
                    )
                else:
                    msg = Messages.simplePostMessage(
                        display_name=name, 
                        content=content)
                for user_id, info in followers.items():
                    sock.sendto(msg.encode(), (info["ip"], PORT))
            case "dm":
                recName = input("Enter recipient's display name: ")
                message = input("Enter your message: ")
                recipient = None
                for user_id, info in peers.items():
                    if info["display_name"] == recName:
                        recipient = info
                        userID = user_id
                if recipient:
                    peer_ip = recipient["ip"]        
                    if verbose.is_set():
                        msg = Messages.verboseDMMessage(
                            sender=name,
                            ip_address=ip_address,
                            userID=userID,
                            message=message,
                            ttl=ttl
                        )
                    else:
                        msg = Messages.simpleDMMessage(sender=name, message=message)
                    sock.sendto(msg.encode(), (peer_ip, PORT))
                else: print("No user found.\n")
            case "follow":
                targetFollow = input("Enter display name to follow: ")
                followed = None
                for user_id, info in peers.items():
                    if info["display_name"] == targetFollow:
                        followed = info
                        userID = user_id
                if followed:
                    peer_ip = followed["ip"]
                    if verbose.is_set():
                        msg = Messages.verboseFollowMessage(
                            follower=name,
                            userID=userID,
                            ip_address=ip_address,
                            ttl=ttl
                        )
                    else:
                        msg = Messages.simpleFollowMessage(name)
                    sock.sendto(msg.encode(), (peer_ip, PORT))
                else: print("No user found.\n")
            case "unfollow":
                targetFollow = input("Enter display name to unfollow: ")
                followed = None
                for user_id, info in peers.items():
                    if info["display_name"] == targetFollow:
                        followed = info
                        userID = user_id
                if followed:
                    peer_ip = followed["ip"]
                    if verbose.is_set():
                        msg = Messages.unfollowVerboseMessage(
                            follower=name,
                            userID=userID,
                            ip_address=ip_address,
                            ttl=ttl
                        )
                    else:
                        msg = Messages.unfollowSimpleMessage(name)
                    sock.sendto(msg.encode(), (peer_ip, PORT))
                else: print("No user found.\n")
            case "--exit":
                print("Exiting...")
                sock.close()
                return


# === RUN THREADS ===
recv_thread = threading.Thread(target=receive_messages, args=(verbose,), daemon=True)
recv_thread.start()
ping_thread = threading.Thread(target=broadcast_ping, args=(name, verbose,), daemon=True)
ping_thread.start()

send_messages(name, status, verbose)  # Runs in main thread
