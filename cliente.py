#Importar librarias adicionais
import socket
import threading

#Constantes
FORMAT = "'utf-8'"
BUFF = 4096

#Iniciar o socket e conectar ao servidor através do ip e da porta
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('127.0.0.1', 25888))


#Receber o nome do utilizador e enviar para o servidor
while True:
    while True:
        try:
            nome_cliente = input("Insira o seu nome sem espaços: ")
            if (' ' in nome_cliente) == False:
                break
        except:
            print("Erro.")
            break
        else:
            continue
    cliente.send(nome_cliente.encode(FORMAT))
    m = cliente.recv(BUFF).decode(FORMAT)
    if m != "utijaexistenosistem1928":
        print(m)
        break
    print("Nome de utilizador já em uso, escolha outro.")

#Receber mensagens do servidor
def receber():
    while True:
        try:
            mensagem = cliente.recv(BUFF).decode(FORMAT)
            print(mensagem)
        except:
            print("Erro.")
            cliente.close()
            break

#Enviar mensagens para o servidor
def escrever():
    while True:
        mensagem = input()
        cliente.send(mensagem.encode(FORMAT))



#Iniciar um thread para a função receber mensagens e outra para a função de enviar
receber_thread = threading.Thread(target=receber)
receber_thread.start()

escrever_thread = threading.Thread(target=escrever)
escrever_thread.start()