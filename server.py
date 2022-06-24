#Importar librarias adicionais
import datetime
import socket
import threading

#Defenir ip e porta do servidor
#host = '192.168.229.85'
host = '127.0.0.1'
port = 25888

#Criar um socket para o servidor e coloca-lo à procura de conexões
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

#Constantes
FORMAT = "'utf-8'"
BUFF = 4096


#Variaveis e Listas
clientes = []
nomes = []


#Enviar mensagem para todos os clientes ativos
def transmitir(mensagem):
    for cliente in clientes:
        cliente.send(mensagem)

#Função para transferir data entre o cliente e o servidor
def lidar(cliente):
    #Receber o nome de utilizador introduzido pelo cliente que se conecta e validar para que não haja repetidos
    try:
        while True:
            nome_utilizador = cliente.recv(BUFF).decode(FORMAT)
            estado_nome = True
            for nome in nomes:
                if nome_utilizador == nome:
                    cliente.send("utijaexistenosistem1928".encode(FORMAT))
                    estado_nome = False
                    break
            if estado_nome == True:
                break
        
        print(f"{nome_utilizador} entrou no chat!")
        transmitir(f"{nome_utilizador} entrou no chat!".encode(FORMAT))
        msg_inicial(cliente, nome_utilizador)
        nomes.append(nome_utilizador)
        clientes.append(cliente)
    except:
        cliente.close()
        return
    #Receber as mensagens do cliente e caso o mesmo se desconecte, remover da lista de clientes
    while True:
        try:
            mensagem = cliente.recv(BUFF).decode(FORMAT)
            mensagens(mensagem, cliente)
        except:
            index = clientes.index(cliente)
            nome_utilizador = nomes[index]
            clientes.remove(cliente)
            nomes.remove(nome_utilizador)
            cliente.close()
            transmitir(f"{nome_utilizador} saiu do chat!".encode(FORMAT))
            print(f"{nome_utilizador} saiu do chat!")
            break


#Receber diversos clientes e criar uma thread da função lidar para cada um
def receber():
    while True:
        cliente, address = server.accept()
        thread = threading.Thread(target=lidar, args=(cliente,))
        thread.start()


#Função para receber a mensagem do utilizador e validar para caso utilize um dos comando disponivel
def mensagens(mensagem, cliente):
    index = clientes.index(cliente)
    nome_utilizador = nomes[index]
    nome_encontrado = False
    data = datetime.datetime.now()

    if mensagem[0] == "/":
        if len(mensagem.split()) > 1:
            msg = mensagem.split(maxsplit=1)
            destinatario = msg[0].replace("/", "")
            if destinatario == nome_utilizador:
                cliente.send(f"Não é possivel enviar mensagem para si próprio.".encode(FORMAT))
            else:
                for nome in nomes:
                    if nome == destinatario:
                        i = nomes.index(nome)
                        dest_final = clientes[i]
                        dest_final.send(f"Privado de {nome_utilizador}: {msg[1]}".encode(FORMAT))
                        cliente.send(f"Privado enviado para {nome}: {msg[1]}".encode(FORMAT))
                        historico_privado = open('historico_privado.txt', 'a')
                        historico_privado.write(data.strftime("%d-%m-%Y %H:%M:%S") + f" De {nome_utilizador} para {nome}: {msg[1]} \n")
                        historico_privado.close()
                        nome_encontrado = True
                if nome_encontrado == False:
                    cliente.send(f"Utilizador não encontrado".encode(FORMAT))
        else:
            if mensagem == "/ajuda":
                ajuda(cliente)
            elif mensagem == "/lista":
                lista(cliente)
            else:
                cliente.send(f"Comando errado, tente novamente.".encode(FORMAT))
    else:
        transmitir(f"{nome_utilizador}: {mensagem}".encode(FORMAT))
        historico_publico = open('historico_publico.txt', 'a')
        historico_publico.write(data.strftime("%d-%m-%Y %H:%M:%S") + f" {nome_utilizador}: {mensagem} \n")
        historico_publico.close()

#Função para mostrar os comandos disponiveis e a sua função
def msg_inicial(cliente, nome_utilizador):
    msg = f"""
-----------------------------------------------------------------
Bem-Vindo ao chat {nome_utilizador}!

Para enviar mensagens basta escrever o que deseja e premir enter.
Para enviar mensagem privada utilize '/nome_utilizador mensagem'.
Pra mostrar a lista de utilizador online utilize '/lista'.

Se necessitar de ajuda utilize '/ajuda'.
------------------------------------------------------------------
"""
    cliente.send(msg.encode(FORMAT))
#Função para mostrar os comandos disponiveis e a sua função
def ajuda(cliente):
    msg = """
---------------------------------------------------------------------------------------------------
Utilize o comando '/nome_do_utilizador mensagem' para enviar mensagem apenas para aquele utilizador.
Exemplo: Ao utilizar o comando '/davidvilarinho Olá', se existir um utilizador online
com o nome 'davidvilarinho', este irá receber uma mensagem privada a dizer 'Olá'.
        
Utilize o comando '/lista' para mostrar a lista de clientes ativos no momento.

Utilize o comando '/ajuda' caso necessite de rever algo aqui presente novamente.
---------------------------------------------------------------------------------------------------
"""
    cliente.send(msg.encode(FORMAT))

#Função para mostrar a lista de clientes ativos
def lista(cliente):
    msg = ''
    for n in range(len(nomes)):
        if n == 0:
            msg += f"{nomes[n]}"
        else:
            msg += f"\n{nomes[n]}"
    msg_final = f"""-----------------------------
Lista de Utilizadores Online

{msg}
-----------------------------"""

    cliente.send(msg_final.encode(FORMAT))
    
print("Server On....")
#Iniciar thread para receber clientes e iniciar o menu no servidor
receber_thread = threading.Thread(target=receber)
receber_thread.start()