import socket
import threading
import uuid
import time
import getpass

PORT = 6000
BUFFER = 4096


board = [' '] * 9
games = {}        
my_id = f"{getpass.getuser()}@198.0.0.1"
connections = {}  
game_info = {}    




def handle_invite(msg, addr):
    sender = msg['FROM']
    gameid = msg['GAMEID']
    symbol = "O"
    connections[sender] = addr

    print(f"\n Game invite from {sender}")
    print("Waiting for opponent's move...")

    game_info.update({
        "gameid": gameid,
        "opponent": sender,
        "symbol": symbol,
        "turn": 2
    })
    games[gameid] = [' '] * 9

def handle_move(msg):
    pos = int(msg['POSITION'])
    sym = msg['SYMBOL']
    gameid = msg['GAMEID']
    games[gameid][pos] = sym
    display_board()
    game_info["turn"] += 1

    result, win_line = check_result(sym, games[gameid])
    if result:
        send_result(gameid, result, sym, win_line)
        print(f"\n🏁 Game Over: {result}")
    else:
        print("Your turn. (Enter a position 0–8)")

def handle_result(msg):
    print("\n Game Over.")
    display_board()

def server_thread():
    while True:
        data, addr = sock.recvfrom(BUFFER)
        msg_str = data.decode()
        msg = parse_message(msg_str)
        msg_type = msg.get("TYPE")
        sender = msg.get("FROM")

        if sender:
            connections[sender] = addr

        if msg_type == "TICTACTOE_INVITE":
            handle_invite(msg, addr)
        elif msg_type == "TICTACTOE_MOVE":
            handle_move(msg)
        elif msg_type == "TICTACTOE_RESULT":
            handle_result(msg)


def display_board():
    b = games[game_info['gameid']]
    print("\n")
    print(f" {b[0]} | {b[1]} | {b[2]}")
    print("---|---|---")
    print(f" {b[3]} | {b[4]} | {b[5]}")
    print("---|---|---")
    print(f" {b[6]} | {b[7]} | {b[8]}\n")

def check_result(symbol, b):
    wins = [(0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)]
    for a, b1, c in wins:
        if b[a] == b[b1] == b[c] == symbol:
            return "WIN", [a, b1, c]
    if all(cell != ' ' for cell in b):
        return "DRAW", []
    return None, []



def send_invite(opponent_id, opponent_ip):
    gameid = f"g{uuid.uuid4().hex[:3]}"
    token = create_token()
    symbol = "X"
    msg = f"""TYPE: TICTACTOE_INVITE
FROM: {my_id}
TO: {opponent_id}
GAMEID: {gameid}
MESSAGE_ID: {uuid.uuid4().hex}
SYMBOL: {symbol}
TIMESTAMP: {int(time.time())}
TOKEN: {token}"""

    opponent_addr = (opponent_ip, PORT)
    connections[opponent_id] = opponent_addr
    send_message(msg, opponent_addr)

    game_info.update({
        "gameid": gameid,
        "opponent": opponent_id,
        "symbol": symbol,
        "turn": 1
    })
    games[gameid] = [' '] * 9
    print("Invite sent. You are X. Your move.")

def send_move(pos):
    token = create_token()
    gameid = game_info["gameid"]
    msg = f"""TYPE: TICTACTOE_MOVE
FROM: {my_id}
TO: {game_info['opponent']}
GAMEID: {gameid}
MESSAGE_ID: {uuid.uuid4().hex}
POSITION: {pos}
SYMBOL: {game_info['symbol']}
TURN: {game_info['turn']}
TOKEN: {token}"""
    send_to_user(msg, game_info["opponent"])

def send_result(gameid, result, symbol, win_line):
    msg = f"""TYPE: TICTACTOE_RESULT
FROM: {my_id}
TO: {game_info['opponent']}
GAMEID: {gameid}
MESSAGE_ID: {uuid.uuid4().hex}
RESULT: {result}
SYMBOL: {symbol}
WINNING_LINE: {','.join(map(str, win_line))}
TIMESTAMP: {int(time.time())}"""
    send_to_user(msg, game_info["opponent"])

