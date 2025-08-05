# udp_peer.py
import socket
import threading
import time
import Messages

# === CONFIGURATION ===
PORT = 50999
BUFFER_SIZE = 4096
DEFAULT_TTL = 3600  # 1 hour default

# === USER INPUTS ===
name = input("Enter your display name: ");
status = input("Enter your status: ");
verbose = threading.Event()  # Verbose mode flag
peers = {} # store peer data 
peers_mess = {} # store message data 

# === UDP SOCKET SETUP ===
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Allow address reuse
sock.bind(("0.0.0.0", PORT)) # Bind to all interfaces on the specified port
print(f"Successfully bound to port {PORT}")

# === Send to all peers ===
def sendToAllPeers(message):
    for user_id, info, in peers.items():
        peer_ip = info["ip"]
        try:
            sock.sendto(message.encode(), (peer_ip, PORT))
        except Exception as e:
            print(f"Failed to send to {peer_ip}: {e}\n")

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
        sendToAllPeers(msg)
        sendToAllPeers(ping)
        time.sleep(300) # wait for 5 minutes
        
# === RECEIVE LOOP ===
def receive_messages(verbose):
    ip_address = socket.gethostbyname(socket.gethostname())  # Get local IP
    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        message = data.decode()
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
            from_disp = None

            for line in message_lines:
                if line.startswith("FROM: "):
                    from_disp = line.split(":", 1)[1].strip()
            if from_disp:
                if verbose.is_set():
                    msg = Messages.verboseFollowMessage(
                        follower=from_disp,
                        userID=name,
                        ip_address=ip_address,
                        ttl=DEFAULT_TTL
                    )
                else: msg = Messages.simpleFollowMessage(from_disp)
            print(msg)
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
            case "--peers":
                print("\n=== Known Peers ===")
                for user_id, info in peers.items():
                    print(f"{info['display_name']} ({user_id}) - {info.get('status', '')}\n")

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
                    status=status,
                    av_type="image/png",
                    av_encoding="base64",
                    av_data="iVBORw0KGgoAAAANSUhEUgAAAAUA..."  # Truncated sample
                )
                else: msg = Messages.simpleProfMessage(display_name=name, status=status)
                sendToAllPeers(msg)
                print("Profile Message sent.")
            case "post":
                content = input("Enter your post content: ")
                if verbose.is_set():
                    msg = Messages.verbosePostMessage(
                        display_name=name,
                        ip_address=ip_address,
                        ttl=ttl,
                        content=content,
                        av_type="image/png",
                        av_encoding="base64",
                        av_data="iVBORw0KGgoAAAANSUhEUgAAAAUA..."
                    )
                else:
                    msg = Messages.simplePostMessage(
                        display_name=name, 
                        content=content,
                        av_type="image/png",
                        av_encoding="base64",
                        av_data="iVBORw0KGgoAAAANSUhEUgAAAAUA...")
                sendToAllPeers(msg)
                print("Post message sent.")
            case "dm":
                recName = input("Enter recipient's display name: ")
                message = input("Enter your message: ")
                recipient = None
                for user_id, info, in peers.items():
                    if info["display_name"] == recName:
                        recipient = info
                        userID = user_id
                        return
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
                    print("Direct message sent.\n")
                else: print("No user found.\n")
            case "follow":
                targetFollow = input("Enter display name to follow: ")
                followed = None
                for user_id, info, in peers.items():
                    if info["display_name"] == recName:
                        followed = info
                        userID = user_id
                        return
                if followed:
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
                    print(f"You are now following {targetFollow}\n")
                else: print("No user found.\n")

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
