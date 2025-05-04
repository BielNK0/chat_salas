import socket
import threading

# Estrutura de dados para salas
salas = {}  # {'nome_sala': {'senha': '123', 'clientes': [(conexao, apelido), ...]}}

def tratar_cliente(conexao, endereco):
    try:
        # Espera: sala|senha|apelido
        dados = conexao.recv(1024).decode()
        partes = dados.split("|")
        if len(partes) != 3:
            conexao.send("Formato inválido.".encode())
            conexao.close()
            return

        nome_sala, senha_digitada, apelido = partes

        if nome_sala not in salas:
            # Cria nova sala
            salas[nome_sala] = {"senha": senha_digitada, "clientes": []}
        else:
            # Verifica senha
            if salas[nome_sala]["senha"] != senha_digitada:
                conexao.send("Senha incorreta para a sala.".encode())
                conexao.close()
                return

        # Adiciona cliente à sala
        salas[nome_sala]["clientes"].append((conexao, apelido))
        conexao.send(f"Conectado à sala '{nome_sala}' como {apelido}".encode())
        print(f"[{endereco}] entrou na sala '{nome_sala}' como {apelido}")

        # Loop de mensagens
        while True:
            msg = conexao.recv(1024).decode()
            if not msg:
                break

            mensagem_final = f"{apelido}: {msg}"
            print(f"[{nome_sala}] {mensagem_final}")

            # Envia para todos da sala (exceto o próprio)
            for cliente, nick in salas[nome_sala]["clientes"]:
                if cliente != conexao:
                    try:
                        cliente.send(mensagem_final.encode())
                    except:
                        pass  # Cliente pode estar desconectado

    except Exception as e:
        print(f"[ERRO] {endereco} desconectou: {e}")

    finally:
        # Remove cliente da sala
        try:
            salas[nome_sala]["clientes"] = [
                (c, n) for c, n in salas[nome_sala]["clientes"] if c != conexao
            ]
            if not salas[nome_sala]["clientes"]:
                del salas[nome_sala]  # Remove sala se vazia
        except:
            pass
        conexao.close()

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(("0.0.0.0", 5555))
    servidor.listen()
    print("Servidor iniciado e aguardando conexões...")

    while True:
        conexao, endereco = servidor.accept()
        thread = threading.Thread(target=tratar_cliente, args=(conexao, endereco))
        thread.start()

# Início
iniciar_servidor()
