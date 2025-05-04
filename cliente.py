import socket
import threading

def receber_mensagens(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            print("\n" + msg)
        except:
            break

ip = input("IP do servidor: ")
porta = int(input("Porta: "))
sala = input("Nome da sala: ")
senha = input("Senha da sala: ")
apelido = input("Seu apelido: ")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip, porta))

# Envia: sala|senha|apelido
sock.send(f"{sala}|{senha}|{apelido}".encode())

resposta = sock.recv(1024).decode()
print(resposta)

# Inicia thread para ouvir mensagens
threading.Thread(target=receber_mensagens, daemon=True, args=(sock,)).start()

while True:
    try:
        msg = input()
        sock.send(msg.encode())
    except:
        break
