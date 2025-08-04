import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except:
        return "127.0.0.1"
    finally:
        s.close()

user_id = "user123"  # Example user ID
ip_address = "<ip_address>"  # Replace with the actual IP address
av_type = "image/png"  # Example avatar type
av_encoding = "base64"  # Example avatar encoding
av_data = "iVBORw0KGgoAAAANSUhEUgAAAAUA..."  # Example base64 encoded avatar data

profile_message = f"""TYPE: PROFILE
USER_ID: {user_id}@{ip_address}
DISPLAY_NAME: Group 9S
STATUS: Online
AVATAR_TYPE: {av_type}
AVATAR_ENCODING: {av_encoding}
AVATAR_DATA: {av_data}
"""