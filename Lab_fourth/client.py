import socket # Used socket because with socket was comfortable to make connections
import threading # threading module

host = '127.0.0.1' # its equivalent for localhost
port = 12346 # any port in range of 0 and 65535 and not root ports such as 443 or 80

# Request function to create username and enter into the server
def requester(client):
    user = input("Enter the username: ")
    if user!='':
        client.sendall(user.encode())
    else:
        print("Error creating username")
        exit()

    threading.Thread(target=listener,args=(client, )).start()
    sender(client)

# Listener function to send decoded messages to client 
def listener(client):
    while True:
        text = client.recv(2048).decode('utf-8')
        if text!='':
            user = text.split(":")[0] # Spliting the messages where [host:] or [user:]
            res = text.split(":")[1] # Message splitted then <something> : <message>
            print(f"\n[{user}] {res}")    
        else:
            print("No message!")
            break

# Sender function to send message to server then to the client
def sender(client):
    while True:
        text = input("Enter the message you want: ")
        if text!='':
            client.sendall(text.encode())
        else:
            print("No message!")
            exit()

# Main function where creating client socket and establisih connections with server side
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creating socket
    try:
        client.connect((host,port)) # Estabilish the conneciton with server
        print("Connected to the server")
    except:
        print("Problems with server, no connection")

    requester(client)

# Runner
if __name__=="__main__":
    main()