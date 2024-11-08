import socket

#configurer le serveur

hostname = socket.gethostname()
host = socket.gethostbyname(hostname)
port = 8080

def server_start():

    loop=True

    #Etablir la connection
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    print(f"En attente de connection sur {port}...")

    while loop == True:
        server.listen()
        conn,addr = server.accept()
        print(f"Connection établie avec {addr}")
        
        conn.send('sd'.encode('utf-8'))
        data = conn.recv(1024).decode()
        print(data)
        
        conn.close()
    print('Server shutdown')
    server.close()
