from time import *

import socket

def client_start(data,host):
    # Configurer le client
    port = 8080
    
    # Etablir la connexion
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Gérer les erreurs
    try:
        client.connect((host, port))
        print("Client connecté !")
        sleep(0.5)
        while client.recv(64,22).decode() != 'Can send':
            sleep(0.001)
        print(client.recv(64,22).decode())
        client.send(data.encode('utf-8'),22)
    except Exception as e:
        print("Connection au serveur échouée !")
        print(f"l'erreur de connection est: {e}")

    # Fermer la connexion
    client.close()

