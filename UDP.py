# udp_peer.py
import socket
import threading

# === CONFIGURATION ===
PORT = 50999
BUFFER_SIZE = 4096
PEER_IP = "127.0.0.1"  # Change to actual peer IP for real use

# === UDP SOCKET SETUP ===
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", PORT))
print(f"✅ Bound to port {PORT} — ready to send and receive.")

# === PROFILE MESSAGE FORMAT ===
def create_profile_message(user_id, ip_address, av_type, av_encoding, av_data):
    return f"""TYPE: PROFILE
USER_ID: {user_id}@{ip_address}
DISPLAY_NAME: Group 9
STATUS: Online
AVATAR_TYPE: {av_type}
AVATAR_ENCODING: {av_encoding}
AVATAR_DATA: {av_data}
"""

# === RECEIVE LOOP ===
def receive_messages():
    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        print(f"\n📩 Received from {addr}:\n{data.decode()}\n")

# === SEND LOOP ===
def send_messages():
    ip_address = socket.gethostbyname(socket.gethostname())  # Get local IP
    while True:
        input("🔼 Press Enter to send PROFILE... ")
        msg = create_profile_message(
            user_id="user123",
            ip_address=ip_address,
            av_type="image/png",
            av_encoding="base64",
            av_data="iVBORw0KGgoAAAANSUhEUgAAAAUA..."  # Truncated sample
        )
        sock.sendto(msg.encode(), (PEER_IP, PORT))
        print("✅ Message sent.")

# === RUN THREADS ===
recv_thread = threading.Thread(target=receive_messages, daemon=True)
recv_thread.start()

send_messages()  # Runs in main thread
