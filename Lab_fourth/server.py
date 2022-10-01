import socket # Used socket because with socket was comfortable to make connections
import threading # threading module

host = '127.0.0.1' # its equivalent for localhost
port = 12346 # any port in range of 0 and 65535 and not root ports such as 443 or 80
max_listener = 5 # maximum listeners
clients = [] # clients list to send messages and identify as user

# Listener function to send decoded messages
def listener(client, user):
    while True:
        text = client.recv(2048).decode('utf-8')

        if text != '': 
            final_msg = user + ':' + text
            sender_all(final_msg)
        else:
            print(f"The text send from client {user} is invalid")
            break

# Function to encode the text and send it into client
def sender_client(client, text):
    client.sendall(text.encode())

# Grab the decoded text and sending it to all clients
def sender_all(text):
    for user in clients:
        sender_client(user[1], text)

# Handling function to recieve messages and log in client side
def handler(client):
    while True:
        user = client.recv(2048).decode('utf-8')
        if user != '':
            clients.append((user, client))
            prompt_text = host+ ":" + f"{user} connected to the server!"
            sender_all(prompt_text)
            break
        else:
            print("Invalid user")
            break

    threading.Thread(target=listener, args=(client, user, )).start()

# Main function to estabilish connection and create socket
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((host, port)) # Binding the server with our ip address and port
        print(f"Running the server on {host} {port}")
    except:
        print(f"Unable to bind to host {host} and port {port}")
    server.listen(max_listener) # listen for our listener
    while True:
        client, address = server.accept()
        print(f"Connected to the client {address[0]} {address[1]}")
        threading.Thread(target=handler, args=(client, )).start()

# Runner
if __name__ == '__main__':
    main()