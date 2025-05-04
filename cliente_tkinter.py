import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

class ClienteChat:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat com Salas - Cliente")
        self.sock = None
        self.conectado = False

        # Entrada para IP e porta
        tk.Label(root, text="IP do Servidor:").grid(row=0, column=0)
        self.entry_ip = tk.Entry(root)
        self.entry_ip.insert(0, "127.0.0.1")
        self.entry_ip.grid(row=0, column=1)

        tk.Label(root, text="Porta:").grid(row=1, column=0)
        self.entry_porta = tk.Entry(root)
        self.entry_porta.insert(0, "5555")
        self.entry_porta.grid(row=1, column=1)

        # Entrada para Sala, Senha e Apelido
        tk.Label(root, text="Sala:").grid(row=2, column=0)
        self.entry_sala = tk.Entry(root)
        self.entry_sala.insert(0, "geral")
        self.entry_sala.grid(row=2, column=1)

        tk.Label(root, text="Senha da Sala:").grid(row=3, column=0)
        self.entry_senha = tk.Entry(root, show="*")
        self.entry_senha.grid(row=3, column=1)

        tk.Label(root, text="Seu Apelido:").grid(row=4, column=0)
        self.entry_apelido = tk.Entry(root)
        self.entry_apelido.insert(0, "Convidado")
        self.entry_apelido.grid(row=4, column=1)

        self.btn_conectar = tk.Button(root, text="Conectar", command=self.conectar)
        self.btn_conectar.grid(row=5, column=0, columnspan=2, pady=5)

        # Área de chat
        self.chat_area = scrolledtext.ScrolledText(root, state="disabled", width=50, height=20)
        self.chat_area.grid(row=6, column=0, columnspan=2)

        # Campo de mensagem
        self.entry_mensagem = tk.Entry(root, width=40)
        self.entry_mensagem.grid(row=7, column=0)

        self.btn_enviar = tk.Button(root, text="Enviar", command=self.enviar_mensagem)
        self.btn_enviar.grid(row=7, column=1)

    def conectar(self):
        try:
            ip = self.entry_ip.get()
            porta = int(self.entry_porta.get())
            sala = self.entry_sala.get()
            senha = self.entry_senha.get()
            apelido = self.entry_apelido.get()

            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((ip, porta))

            # Envia sala|senha|apelido
            dados = f"{sala}|{senha}|{apelido}"
            self.sock.send(dados.encode())

            # Aguarda possível resposta
            resposta = self.sock.recv(1024).decode()
            if "Senha incorreta" in resposta:
                messagebox.showerror("Erro", resposta)
                self.sock.close()
                return

            self.conectado = True
            self.adicionar_chat(resposta)

            threading.Thread(target=self.receber_mensagem, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Erro de conexão", str(e))

    def receber_mensagem(self):
        while self.conectado:
            try:
                msg = self.sock.recv(1024).decode()
                self.adicionar_chat(msg)
            except:
                break

    def enviar_mensagem(self):
        msg = self.entry_mensagem.get()
        if msg and self.conectado:
            try:
                self.sock.send(msg.encode())
                self.entry_mensagem.delete(0, tk.END)
            except:
                self.adicionar_chat("Erro ao enviar mensagem.")

    def adicionar_chat(self, texto):
        self.chat_area.configure(state="normal")
        self.chat_area.insert(tk.END, texto + "\n")
        self.chat_area.configure(state="disabled")
        self.chat_area.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ClienteChat(root)
    root.mainloop()
