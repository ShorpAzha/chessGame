from time import *

import socket

def client_send(data,host):
    # Configurer le client
    port = 8080
    
    # Etablir la connexion
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Gérer les erreurs
    try:
        client.connect((host, port))
        print("Client connecté !")
        
        while client.recv(1024).decode() != 'sd':
            sleep(0.001)
        client.send(data.encode('utf-8'))
        
    except Exception as e:
        print("Connection au serveur échouée !")
        print(f"l'erreur de connection est: {e}")

    # Fermer la connexion
    client.close()