import socket
import psycopg2

# Configurações para o servidor TCP
TCP_HOST = 'localhost'
TCP_PORT = 8888

# Configurações para o servidor UDP
UDP_HOST = 'localhost'
UDP_PORT = 8889

# Configuração do socket TCP
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.bind((TCP_HOST, TCP_PORT))
tcp.listen(5)
print(f"Servidor TCP aguardando conexões em {TCP_HOST}:{TCP_PORT}")

# Configuração do socket UDP
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind((UDP_HOST, UDP_PORT))
print(f"Servidor UDP aguardando conexões em {UDP_HOST}:{UDP_PORT}")

def conectarBanco():
    conn = psycopg2.connect(host="localhost",database="distribuidos", user="postgres", password="postgres", port= "5432")
    return conn

def validarLogin(login, senha):
    conn = conectarBanco()
    cur = conn.cursor()
    cur.execute("SELECT * FROM login WHERE login = %s AND senha = %s", (login, senha))
    rows = cur.fetchall()
    if len(rows) > 0:
        return True
    else:
        return False
    
def cadastrarUsuario(login, senha, nome, email, telefone):
    conn = conectarBanco()
    cur = conn.cursor()
    login = login
    senha = senha
    cur.execute("insert into login (login, senha) values (%s, %s)", (login, senha))
    cur.execute("INSERT INTO usuarios (login, nome, email, telefone) VALUES (%s, %s, %s, %s)", (login, nome, email, telefone))
    conn.commit()
    cur.close()
    conn.close()

# Função para lidar com as transações de alta confiabilidade via TCP
def conexaoTCP(client):
    try:
        # Solicitar credenciais de login e senha
        client.send("Digite seu login: ".encode('utf-8'))
        login = client.recv(1024).decode('utf-8')
        client.send("Digite sua senha: ".encode('utf-8'))
        senha = client.recv(1024).decode('utf-8')

        # Verificar credenciais de login
        if validarLogin(login, senha):
            client.send("Login Successful!".encode('utf-8'))
        elif not validarLogin(login, senha):
            client.send("Login Failed!".encode('utf-8'))
            # Se a validação de login falhar, solicitar informações de cadastro
            client.send("Digite seu nome: ".encode('utf-8'))
            nome = client.recv(1024).decode('utf-8')

            client.send("Digite seu email: ".encode('utf-8'))
            email = client.recv(1024).decode('utf-8')

            client.send("Digite seu telefone: ".encode('utf-8'))
            telefone = client.recv(1024).decode('utf-8')

            print(f"Usuário {login} solicitou cadastro")
            cadastrarUsuario(login, senha, nome, email, telefone)
            print(f"Usuário {login} cadastrado com sucesso!")
            
            client.send("CADASTRO_CONCLUIDO".encode('utf-8'))
        client.send("Interesse financeiro: ".encode('utf-8'))

            
        
        while True:
            data = client.recv(1024).decode('utf-8')
            if not data:
                break
    except ConnectionResetError:
        print("Conexão TCP encerrada pelo cliente")
    
    except Exception as e:
        print(f"Erro inesperado: {e}")
        
    finally:
        client.close()

# Função para lidar com o streaming de dados financeiros via UDP
def conexaoUDP():
    while True:
        data, addr = udp.recvfrom(1024)
        
        interesse = data.decode('utf-8')
        print(f"Interesse financeiro: {interesse}")
        
        if interesse == "Dólar":
            cotacao = "5.50"
            resposta = f"A cotação do dólar é {cotacao}"
            udp.sendto(resposta.encode('utf-8'), addr)

# Iniciar thread para lidar com o streaming de dados UDP
import threading
udp_thread = threading.Thread(target=conexaoUDP)
udp_thread.start()

# Aguardar conexões TCP e lidar com as transações de alta confiabilidade
while True:
    client_sock, addr = tcp.accept()
    print(f"Conexão TCP de {addr}")
    conexaoTCP(client_sock)
