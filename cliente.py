import socket

# Configurações do servidor TCP
SERVER_TCP_HOST = 'localhost'
SERVER_TCP_PORT = 8888

# Configurações do servidor UDP
SERVER_UDP_HOST = 'localhost'
SERVER_UDP_PORT = 8889

# Crie um socket TCP
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Crie um socket UDP
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Conecte-se ao servidor TCP
tcp.connect((SERVER_TCP_HOST, SERVER_TCP_PORT))

# Conecte-se ao servidor UDP
udp.connect((SERVER_UDP_HOST, SERVER_UDP_PORT))

modoCadastro = False  # Variável para acompanhar se estamos no modo de cadastro

while True:
    data = tcp.recv(1024).decode('utf-8')
    if data.startswith("Digite seu login: "):
        login = input(data)
        tcp.send(login.encode('utf-8'))
    elif data.startswith("Digite sua senha: "):
        senha = input(data)
        tcp.send(senha.encode('utf-8'))
    elif data == "Login Successful!":
        print("Login bem-sucedido!")
        
    elif data == "Login Failed!":
        print("Login falhou. Tente novamente ou cadastre-se.")
        modoCadastro = True  # Ative o modo de cadastro
        
    elif modoCadastro:
        # Se estivermos no modo de cadastro, esperamos receber os prompts do servidor e fornecer as informações
        if data == "Digite seu nome: ":
            nome = input(data)
            tcp.send(nome.encode('utf-8'))
        elif data == "Digite seu email: ":
            email = input(data)
            tcp.send(email.encode('utf-8'))
        elif data == "Digite seu telefone: ":
            telefone = input(data)
            tcp.send(telefone.encode('utf-8'))
        elif data == "CADASTRO_CONCLUIDO":
            print("Cadastro concluído com sucesso!")
            modoCadastro = False  # Desativar o modo de cadastro
    elif data == "Interesse financeiro: ":
        while True:
            interesse = input(data)
            udp.send(interesse.encode('utf-8'))
            
            response, _ = udp.recvfrom(1024)
            print(response.decode('utf-8'))  # Exibir a cotação recebida do servidor


