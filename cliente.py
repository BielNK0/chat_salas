import socket
import threading

def receber_mensagens(sock):
    while True:
        try:
            mensagem = sock.recv(1024).decode()
            print(mensagem)
        except:
            print("Conexão encerrada.")
            break

ip_servidor = input("IP do servidor: ")
sala = input("Nome da sala: ")

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((ip_servidor, 5555))

cliente.send(sala.encode())

thread = threading.Thread(target=receber_mensagens, args=(cliente,))
thread.start()

while True:
    msg = input()
    if msg.lower() == "/sair":
        cliente.close()
        break
    cliente.send(msg.encode())
