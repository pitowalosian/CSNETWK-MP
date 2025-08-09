import socket
import base64
import os
import time
import uuid
import threading
import getpass

CHUNK_SIZE = 256
LISTEN_PORT = 5005

file_contexts = {}


def send_file_offer(sock, my_id, receiver_id, receiver_ip, filename):
    filesize = os.path.getsize(filename)
    filetype = "image/jpeg" if filename.endswith(".jpg") else "application/octet-stream"
    fileid = uuid.uuid4().hex
    timestamp = int(time.time())
    token = create_token(my_id)

    offer_msg = f"""TYPE: FILE_OFFER
FROM: {my_id}
TO: {receiver_id}
FILENAME: {filename}
FILESIZE: {filesize}
FILETYPE: {filetype}
FILEID: {fileid}
DESCRIPTION: Vacation snapshot
TIMESTAMP: {timestamp}
TOKEN: {token}"""

    sock.sendto(offer_msg.encode(), (receiver_ip, LISTEN_PORT))
    print(f"User {my_id.split('@')[0]} is sending a file. Waiting for acceptance...")

    sock.settimeout(10)
    try:
        data, _ = sock.recvfrom(4096)
        if data.decode().strip().upper() == "ACCEPT":
            return fileid
    except socket.timeout:
        print("No response from receiver.")
    return None

def send_file_chunks(sock, my_id, receiver_id, receiver_ip, filename, fileid):
    with open(filename, "rb") as f:
        content = f.read()
        total_chunks = (len(content) + CHUNK_SIZE - 1) // CHUNK_SIZE
        token = create_token(my_id)

        for i in range(total_chunks):
            chunk_data = content[i * CHUNK_SIZE: (i + 1) * CHUNK_SIZE]
            b64_data = base64.b64encode(chunk_data).decode()

            chunk_msg = f"""TYPE: FILE_CHUNK
FROM: {my_id}
TO: {receiver_id}
FILEID: {fileid}
CHUNK_INDEX: {i}
TOTAL_CHUNKS: {total_chunks}
CHUNK_SIZE: {CHUNK_SIZE}
TOKEN: {token}
DATA: {b64_data}"""

            sock.sendto(chunk_msg.encode(), (receiver_ip, LISTEN_PORT))
            time.sleep(0.05)

        print(f"File transfer of {filename} is complete")

def receiver_loop(my_id, sock):
    while True:
        try:
            data, addr = sock.recvfrom(65536)
            msg = data.decode()
            if msg.startswith("TYPE: FILE_OFFER"):
                meta = parse_message(msg)
                sender = meta['FROM']
                fileid = meta['FILEID']
                filename = meta['FILENAME']
                print(f"User {sender.split('@')[0]} is sending you a file. Do you accept? (yes/no)")
                answer = input().strip().lower()
                if answer == "yes":
                    sock.sendto(b"ACCEPT", addr)
                    file_contexts[fileid] = {
                        'filename': filename,
                        'chunks': {},
                        'total': None,
                        'from': sender
                    }
                else:
                    print("File offer ignored.")
            elif msg.startswith("TYPE: FILE_CHUNK"):
                meta = parse_message(msg)
                fileid = meta['FILEID']
                if fileid not in file_contexts:
                    continue

                chunk_index = int(meta['CHUNK_INDEX'])
                total_chunks = int(meta['TOTAL_CHUNKS'])
                chunk_data = base64.b64decode(meta['DATA'])

                ctx = file_contexts[fileid]
                ctx['chunks'][chunk_index] = chunk_data
                ctx['total'] = total_chunks

                if len(ctx['chunks']) == ctx['total']:
                    sorted_chunks = [ctx['chunks'][i] for i in range(ctx['total'])]
                    with open("received_" + ctx['filename'], "wb") as f:
                        for chunk in sorted_chunks:
                            f.write(chunk)
                    print(f"File transfer of {ctx['filename']} is complete")
                    send_file_received(sock, my_id, ctx['from'], fileid, addr)
            elif msg.startswith("TYPE: FILE_RECEIVED"):
                pass  # No output for FILE_RECEIVED
        except Exception as e:
            print("Error:", e)

def send_file_received(sock, receiver_id, sender_id, fileid, sender_addr):
    timestamp = int(time.time())
    received_msg = f"""TYPE: FILE_RECEIVED
FROM: {receiver_id}
TO: {sender_id}
FILEID: {fileid}
STATUS: COMPLETE
TIMESTAMP: {timestamp}"""
    sock.sendto(received_msg.encode(), sender_addr)

def sender_loop(sock, my_id):
    while True:
        cmd = input("\nType 'send' to send a file or 'exit' to quit: ").strip().lower()
        if cmd == "send":
            receiver_id = input("Enter receiver ID (e.g., bob@192.168.1.12): ").strip()
            receiver_ip = receiver_id.split("@")[1]
            filename = input("Enter filename to send (e.g., photo.jpg): ").strip()

            if not os.path.exists(filename):
                print("File not found.")
                continue

            fileid = send_file_offer(sock, my_id, receiver_id, receiver_ip, filename)
            if fileid:
                send_file_chunks(sock, my_id, receiver_id, receiver_ip, filename, fileid)
        elif cmd == "exit":
            break
