import socket
import threading

salas = {}

def tratar_cliente(conexao, endereco):
    try:
        dados = conexao.recv(1024).decode()
        partes = dados.split("|")
        if len(partes) != 3:
            conexao.send("Formato inválido.".encode())
            conexao.close()
            return

        nome_sala, senha_digitada, apelido = partes

        if nome_sala not in salas:
            salas[nome_sala] = {"senha": senha_digitada, "clientes": []}
        else:
            if salas[nome_sala]["senha"] != senha_digitada:
                conexao.send("Senha incorreta.".encode())
                conexao.close()
                return

        salas[nome_sala]["clientes"].append((conexao, apelido))
        conexao.send(f"Conectado à sala '{nome_sala}' como {apelido}".encode())
        print(f"[{endereco}] entrou na sala '{nome_sala}' como {apelido}")

        while True:
            msg = conexao.recv(1024).decode()
            if not msg:
                break

            mensagem_final = f"{apelido}: {msg}"
            print(f"[{nome_sala}] {mensagem_final}")

            # Enviar para todos, inclusive remetente
            for cliente, _ in salas[nome_sala]["clientes"]:
                try:
                    cliente.send(mensagem_final.encode())
                except:
                    pass

    except Exception as e:
        print(f"[ERRO] {endereco} desconectou: {e}")
    finally:
        try:
            salas[nome_sala]["clientes"] = [
                (c, n) for c, n in salas[nome_sala]["clientes"] if c != conexao
            ]
            if not salas[nome_sala]["clientes"]:
                del salas[nome_sala]
        except:
            pass
        conexao.close()

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(("0.0.0.0", 5555))
    servidor.listen()
    print("Servidor iniciado...")

    while True:
        conexao, endereco = servidor.accept()
        threading.Thread(target=tratar_cliente, args=(conexao, endereco)).start()

iniciar_servidor()
