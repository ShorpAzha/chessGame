## importing socket module
import socket
## getting the hostname by socket.gethostname() method
hostname = socket.gethostname()
## getting the IP address using socket.gethostbyname() method
ip_address = socket.gethostbyname(hostname)
## printing the hostname and ip_address
print(f"Hostname: {hostname}")
print(f"IP Address: {ip_address}")

from time import *

def kronos_v8():
    now=monotonic()
    h=int(now//(60**2))
    m=int((now-h*60**2)//60)
    s=int((now-m*60-h*60**2)//1)
    return f'Il est {h} heures, {m} minutes et {s} secondes'

print(kronos_v8())