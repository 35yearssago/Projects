import asyncio
from datetime import datetime


clients = {}
chat_rooms = {"main": []}
log_file = "chat_log.txt"


def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


async def broadcast(message, room="main", exclude_writer=None):
    for username in chat_rooms.get(room, []):
        _, writer, client_room = clients.get(username, (None, None, None))
        if writer != exclude_writer and client_room == room:
            try:
                writer.write(f"{message}\n".encode("utf-8"))
                await writer.drain()
            except (ConnectionResetError, BrokenPipeError):
                pass


async def handle_client(reader, writer):
    try:

        writer.write("Enter your username: ".encode("utf-8"))
        await writer.drain()
        username = (await reader.read(1024)).decode("utf-8").strip()

        if not username or username in clients:
            writer.write("Username invalid or already in use. Disconnecting...\n".encode("utf-8"))
            await writer.drain()
            return

        clients[username] = (reader, writer, "main")
        chat_rooms["main"].append(username)
        log_message(f"{username} connected from {writer.get_extra_info('peername')}")
        await broadcast(f"{username} has joined the chat!", room="main")

        writer.write(f"Welcome to the chat, {username}! Type '/help' for commands.\n".encode("utf-8"))
        await writer.drain()

        while True:
            data = await reader.read(1024)
            if not data:
                break

            message = data.decode("utf-8").strip()
            if message.startswith("/"):
                await handle_command(username, message, writer)
            else:

                await broadcast(f"{username}: {message}", room=clients[username][2], exclude_writer=writer)

    except (ConnectionResetError, asyncio.IncompleteReadError):
        log_message(f"Connection lost with {username}")
    except Exception as e:
        log_message(f"Error handling client {username}: {e}")
    finally:

        if username in clients:
            _, _, room = clients[username]
            chat_rooms[room].remove(username)
            del clients[username]
            await broadcast(f"{username} has left the chat.", room=room)
            log_message(f"{username} disconnected.")


async def handle_command(username, command, writer):
    global chat_rooms, clients

    args = command.split(" ", 2)
    cmd = args[0]
    current_room = clients[username][2]

    if cmd == "/list":

        user_list = ", ".join(chat_rooms[current_room])
        writer.write(f"Users in this room: {user_list}\n".encode("utf-8"))
        await writer.drain()

    elif cmd.startswith("/msg") and len(args) >= 3:

        target_username = args[1]
        if target_username in clients:
            _, target_writer, _ = clients[target_username]
            private_message = args[2]
            target_writer.write(f"[Private] {username}: {private_message}\n".encode("utf-8"))
            await target_writer.drain()
            writer.write(f"[To {target_username}] {private_message}\n".encode("utf-8"))
            await writer.drain()
        else:
            writer.write("User not found.\n".encode("utf-8"))
            await writer.drain()

    elif cmd.startswith("/join") and len(args) >= 2:

        new_room = args[1]
        if new_room not in chat_rooms:
            chat_rooms[new_room] = []
        chat_rooms[current_room].remove(username)
        chat_rooms[new_room].append(username)
        clients[username] = (clients[username][0], clients[username][1], new_room)
        writer.write(f"You joined room: {new_room}\n".encode("utf-8"))
        await writer.drain()
        await broadcast(f"{username} has joined the room: {new_room}", room=new_room)

    elif cmd == "/rooms":

        rooms = ", ".join(chat_rooms.keys())
        writer.write(f"Available rooms: {rooms}\n".encode("utf-8"))
        await writer.drain()

    elif cmd == "/help":

        help_text = (
            "/list - List users in the current room\n"
            "/msg <username> <message> - Send a private message\n"
            "/join <room_name> - Join a different room\n"
            "/rooms - List all available rooms\n"
        )
        writer.write(help_text.encode("utf-8"))
        await writer.drain()

    else:

        writer.write("Unknown command. Type '/help' for a list of commands.\n".encode("utf-8"))
        await writer.drain()



async def start_server(host="127.0.0.1", port=12345):
    server = await asyncio.start_server(handle_client, host, port)
    print(f"Server started on {host}:{port}")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(start_server())


#TODO username not showing | there are no timestamps